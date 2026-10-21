
import os
import traceback
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

import psycopg
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

load_dotenv()

# =========================================================
# APLICACIÓN Y CONFIGURACIÓN
# =========================================================

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

DATABASE_URL = os.getenv("DATABASE_URL")
ZONA_HORARIA = ZoneInfo("America/Bogota")
TIEMPO_REUTILIZACION_HORAS = 15

# Cantidades iniciales de cada día.
CANTIDAD_INICIAL_VASO = 50
CANTIDAD_INICIAL_ALMUERZO = 80

# IDs actuales en Neon:
# 1 = Vaso de leche
# 2 = Almuerzo
ALIMENTOS_DIARIOS = (
    (1, CANTIDAD_INICIAL_VASO),
    (2, CANTIDAD_INICIAL_ALMUERZO),
)


# =========================================================
# CONEXIÓN A NEON
# =========================================================

def obtener_conexion():
    if not DATABASE_URL:
        raise RuntimeError(
            "No se encontró la variable de entorno DATABASE_URL"
        )

    conn = psycopg.connect(DATABASE_URL)

    with conn.cursor() as cur:
        cur.execute("SET TIME ZONE 'America/Bogota'")

    return conn


# =========================================================
# CREAR LOS CUPOS DEL DÍA
# =========================================================

def asegurar_cupos_diarios(conn):
    """
    Crea los cupos diarios si no existen.
    No reinicia cantidades que ya hayan sido utilizadas.
    """

    with conn.cursor() as cur:
        # Evita duplicados si llegan solicitudes simultáneas.
        cur.execute("SELECT pg_advisory_xact_lock(6412026)")

        cur.execute("SELECT CURRENT_DATE")
        hoy = cur.fetchone()[0]

        for alimento_id, cantidad_inicial in ALIMENTOS_DIARIOS:
            cur.execute(
                """
                SELECT id
                FROM cupos_diarios
                WHERE alimento_id = %s
                  AND fecha = %s
                LIMIT 1
                """,
                (alimento_id, hoy),
            )

            if cur.fetchone() is None:
                cur.execute(
                    """
                    INSERT INTO cupos_diarios (
                        alimento_id,
                        fecha,
                        cantidad_disponible,
                        cantidad_entregada
                    )
                    VALUES (%s, %s, %s, 0)
                    """,
                    (alimento_id, hoy, cantidad_inicial),
                )


# =========================================================
# CONSULTAR EL CUPO ACTUAL DE UN ALIMENTO
# =========================================================

def consultar_cupo_actual(cur, alimento_id, bloquear=False):
    bloqueo = "FOR UPDATE OF cd" if bloquear else ""

    cur.execute(
        f"""
        SELECT
            a.id,
            a.nombre,
            a.activo,
            cd.id AS cupo_diario_id,
            cd.cantidad_disponible,
            cd.cantidad_entregada,
            cd.fecha
        FROM alimentos AS a
        JOIN cupos_diarios AS cd
            ON cd.alimento_id = a.id
           AND cd.fecha = CURRENT_DATE
        WHERE a.id = %s
        {bloqueo}
        """,
        (alimento_id,),
    )

    return cur.fetchone()


# =========================================================
# PRUEBA DE CONEXIÓN
# =========================================================

@app.get("/api/db-test")
async def db_test():
    try:
        with obtener_conexion() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1")
                resultado = cur.fetchone()

        return {
            "conexion": "ok",
            "resultado": resultado[0],
        }

    except Exception as e:
        traceback.print_exc()

        return JSONResponse(
            status_code=500,
            content={
                "conexion": "error",
                "detalle": str(e),
            },
        )


# =========================================================
# PÁGINAS
# =========================================================

@app.get("/", response_class=HTMLResponse)
async def inicio(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"request": request},
    )


@app.get("/menu", response_class=HTMLResponse)
async def menu(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="menu.html",
        context={"request": request},
    )


@app.get("/vaso", response_class=HTMLResponse)
async def vaso(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="vaso.html",
        context={"request": request},
    )


@app.get("/almuerzo", response_class=HTMLResponse)
async def almuerzo(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="almuerzo.html",
        context={"request": request},
    )


@app.get("/scanner", response_class=HTMLResponse)
async def scanner(request: Request):
    alimento_id = request.query_params.get("alimento")

    if alimento_id not in ("1", "2"):
        alimento_id = "1"

    return templates.TemplateResponse(
        request=request,
        name="scanner.html",
        context={
            "request": request,
            "alimento_id": alimento_id,
        },
    )


# =========================================================
# CONSULTAR ALIMENTO Y CANTIDAD DISPONIBLE
# =========================================================

@app.get("/api/alimentos/{alimento_id}")
async def consultar_alimento(alimento_id: int):
    try:
        with obtener_conexion() as conn:
            asegurar_cupos_diarios(conn)

            with conn.cursor() as cur:
                alimento = consultar_cupo_actual(
                    cur,
                    alimento_id,
                )

                if alimento is None:
                    return JSONResponse(
                        status_code=404,
                        content={
                            "ok": False,
                            "mensaje": "Alimento no encontrado.",
                        },
                    )

                cantidad = alimento[4] or 0
                entregada = alimento[5] or 0

                return {
                    "ok": True,
                    "id": alimento[0],
                    "nombre": alimento[1],
                    "activo": alimento[2],
                    "cantidad": cantidad,
                    "cantidad_disponible": cantidad,
                    "cantidad_entregada": entregada,
                    "cupo_diario_id": alimento[3],
                    "fecha": str(alimento[6]),
                }

    except Exception as e:
        traceback.print_exc()

        return JSONResponse(
            status_code=500,
            content={
                "ok": False,
                "mensaje": "Error consultando alimento.",
                "detalle": str(e),
            },
        )


# =========================================================
# ESCANEO QR Y REGISTRO DE ENTREGA
# =========================================================

@app.post("/api/escaneo")
async def escaneo_qr(data: dict):
    estudiante_id = data.get("estudiante_id")
    alimento_id = data.get("alimento_id")

    if estudiante_id is None or alimento_id is None:
        return JSONResponse(
            status_code=400,
            content={
                "ok": False,
                "mensaje": "Faltan datos del escaneo.",
            },
        )

    try:
        estudiante_id = int(estudiante_id)
        alimento_id = int(alimento_id)

    except (ValueError, TypeError):
        return JSONResponse(
            status_code=400,
            content={
                "ok": False,
                "mensaje": "El ID recibido no es válido.",
            },
        )

    if alimento_id not in (1, 2):
        return JSONResponse(
            status_code=400,
            content={
                "ok": False,
                "mensaje": "El alimento seleccionado no es válido.",
            },
        )

    try:
        with obtener_conexion() as conn:
            asegurar_cupos_diarios(conn)

            with conn.cursor() as cur:

                # 1. Buscar estudiante activo.
                cur.execute(
                    """
                    SELECT id, nombre, apellido
                    FROM estudiantes
                    WHERE id = %s
                      AND activo = TRUE
                    """,
                    (estudiante_id,),
                )

                estudiante = cur.fetchone()

                if estudiante is None:
                    return JSONResponse(
                        status_code=404,
                        content={
                            "ok": False,
                            "mensaje": (
                                "El estudiante no existe "
                                "o está inactivo."
                            ),
                        },
                    )

                # 2. Verificar el bloqueo de reutilización del QR.
                cur.execute(
                    """
                    SELECT fecha, hora
                    FROM entregas
                    WHERE estudiante_id = %s
                    ORDER BY fecha DESC, hora DESC
                    LIMIT 1
                    """,
                    (estudiante_id,),
                )

                ultima_entrega = cur.fetchone()

                ahora = datetime.now(
                    ZONA_HORARIA
                ).replace(tzinfo=None)

                if ultima_entrega:
                    ultima_fecha_hora = datetime.combine(
                        ultima_entrega[0],
                        ultima_entrega[1],
                    )

                    siguiente_uso = (
                        ultima_fecha_hora
                        + timedelta(
                            hours=TIEMPO_REUTILIZACION_HORAS
                        )
                    )

                    if ahora < siguiente_uso:
                        restante = siguiente_uso - ahora
                        segundos = max(
                            0,
                            int(restante.total_seconds()),
                        )

                        return JSONResponse(
                            status_code=409,
                            content={
                                "ok": False,
                                "motivo": "qr_bloqueado",
                                "mensaje": (
                                    f"{estudiante[1]} "
                                    f"{estudiante[2]} "
                                    "no puede reutilizar "
                                    "el código QR todavía."
                                ),
                                "horas_restantes": segundos // 3600,
                                "minutos_restantes": (
                                    segundos % 3600
                                ) // 60,
                                "proximo_uso": (
                                    siguiente_uso.isoformat()
                                ),
                            },
                        )

                # 3. Buscar y bloquear el cupo de hoy.
                cupo = consultar_cupo_actual(
                    cur,
                    alimento_id,
                    bloquear=True,
                )

                if cupo is None:
                    return JSONResponse(
                        status_code=404,
                        content={
                            "ok": False,
                            "mensaje": "El alimento no existe.",
                        },
                    )

                if not cupo[2]:
                    return JSONResponse(
                        status_code=400,
                        content={
                            "ok": False,
                            "mensaje": "El alimento está inactivo.",
                        },
                    )

                cupo_diario_id = cupo[3]
                cantidad_disponible = cupo[4]
                alimento_nombre = cupo[1]

                if (
                    cupo_diario_id is None
                    or cantidad_disponible is None
                ):
                    return JSONResponse(
                        status_code=500,
                        content={
                            "ok": False,
                            "mensaje": (
                                "No se encontró el cupo "
                                "diario del alimento."
                            ),
                        },
                    )

                if cantidad_disponible <= 0:
                    return JSONResponse(
                        status_code=400,
                        content={
                            "ok": False,
                            "mensaje": (
                                f"No quedan {alimento_nombre} "
                                "disponibles."
                            ),
                        },
                    )

                # 4. Descontar una unidad y actualizar el contador.
                cur.execute(
                    """
                    UPDATE cupos_diarios
                    SET cantidad_disponible =
                            cantidad_disponible - 1,
                        cantidad_entregada =
                            COALESCE(cantidad_entregada, 0) + 1
                    WHERE id = %s
                      AND cantidad_disponible > 0
                    RETURNING
                        cantidad_disponible,
                        cantidad_entregada
                    """,
                    (cupo_diario_id,),
                )

                actualizado = cur.fetchone()

                if actualizado is None:
                    return JSONResponse(
                        status_code=409,
                        content={
                            "ok": False,
                            "mensaje": (
                                "No fue posible actualizar "
                                "el cupo. Vuelve a consultar."
                            ),
                        },
                    )

                cantidad_restante = actualizado[0]
                ahora_bd = datetime.now(ZONA_HORARIA)

                # 5. Registrar la entrega vinculada al cupo diario.
                cur.execute(
                    """
                    INSERT INTO entregas (
                        estudiante_id,
                        alimento_id,
                        cupo_diario_id,
                        fecha,
                        hora,
                        tipo_entrega,
                        estado,
                        observacion
                    )
                    VALUES (
                        %s, %s, %s, %s, %s,
                        'normal',
                        'entregado',
                        %s
                    )
                    """,
                    (
                        estudiante_id,
                        alimento_id,
                        cupo_diario_id,
                        ahora_bd.date(),
                        ahora_bd.time().replace(tzinfo=None),
                        "Entrega realizada mediante código QR",
                    ),
                )

                siguiente_uso = (
                    ahora_bd.replace(tzinfo=None)
                    + timedelta(
                        hours=TIEMPO_REUTILIZACION_HORAS
                    )
                )

                return {
                    "ok": True,
                    "mensaje": "Entrega registrada correctamente.",
                    "estudiante_id": estudiante[0],
                    "estudiante": (
                        f"{estudiante[1]} {estudiante[2]}"
                    ),
                    "alimento_id": alimento_id,
                    "alimento": alimento_nombre,
                    "cantidad_restante": cantidad_restante,
                    "cantidad_entregada": actualizado[1],
                    "cupo_diario_id": cupo_diario_id,
                    "qr_reutilizable_en_horas": (
                        TIEMPO_REUTILIZACION_HORAS
                    ),
                    "proximo_uso_qr": siguiente_uso.isoformat(),
                }

    except Exception as e:
        traceback.print_exc()

        return JSONResponse(
            status_code=500,
            content={
                "ok": False,
                "mensaje": "Error al procesar el escaneo.",
                "detalle": str(e),
            },
        )


# =========================================================
# CONSULTAR ENTREGAS
# =========================================================

@app.get("/api/entregas")
async def consultar_entregas(fecha: str = None):
    try:
        with obtener_conexion() as conn:
            with conn.cursor() as cur:

                if fecha:
                    cur.execute(
                        """
                        SELECT
                            e.id,
                            e.estudiante_id,
                            est.nombre,
                            est.apellido,
                            e.alimento_id,
                            a.nombre,
                            e.fecha,
                            e.hora,
                            e.estado,
                            e.observacion
                        FROM entregas AS e
                        JOIN estudiantes AS est
                            ON est.id = e.estudiante_id
                        JOIN alimentos AS a
                            ON a.id = e.alimento_id
                        WHERE e.fecha = %s
                        ORDER BY e.hora DESC
                        """,
                        (fecha,),
                    )

                else:
                    cur.execute(
                        """
                        SELECT
                            e.id,
                            e.estudiante_id,
                            est.nombre,
                            est.apellido,
                            e.alimento_id,
                            a.nombre,
                            e.fecha,
                            e.hora,
                            e.estado,
                            e.observacion
                        FROM entregas AS e
                        JOIN estudiantes AS est
                            ON est.id = e.estudiante_id
                        JOIN alimentos AS a
                            ON a.id = e.alimento_id
                        WHERE e.fecha = CURRENT_DATE
                        ORDER BY e.hora DESC
                        """
                    )

                entregas = cur.fetchall()

                resultado = [
                    {
                        "id": fila[0],
                        "estudiante_id": fila[1],
                        "nombre": fila[2],
                        "apellido": fila[3],
                        "alimento_id": fila[4],
                        "alimento": fila[5],
                        "fecha": str(fila[6]),
                        "hora": str(fila[7]),
                        "estado": fila[8],
                        "observacion": fila[9],
                    }
                    for fila in entregas
                ]

                return {
                    "ok": True,
                    "total": len(resultado),
                    "entregas": resultado,
                }

    except Exception as e:
        traceback.print_exc()

        return JSONResponse(
            status_code=500,
            content={
                "ok": False,
                "mensaje": "Error consultando las entregas.",
                "detalle": str(e),
            },
        )


# =========================================================
# OBTENER DETALLE DE ALIMENTO
# =========================================================

@app.get("/api/alimentos/{alimento_id}/detalle")
def obtener_alimento(alimento_id: int):
    try:
        with obtener_conexion() as conn:
            asegurar_cupos_diarios(conn)

            with conn.cursor() as cur:
                alimento = consultar_cupo_actual(
                    cur,
                    alimento_id,
                )

                if alimento is None:
                    return JSONResponse(
                        status_code=404,
                        content={
                            "ok": False,
                            "mensaje": "Alimento no encontrado.",
                        },
                    )

                cantidad = alimento[4] or 0
                entregada = alimento[5] or 0

                return {
                    "ok": True,
                    "id": alimento[0],
                    "nombre": alimento[1],
                    "activo": alimento[2],
                    "cantidad": cantidad,
                    "cantidad_disponible": cantidad,
                    "cantidad_entregada": entregada,
                    "cupo_diario_id": alimento[3],
                    "fecha": str(alimento[6]),
                }

    except Exception as e:
        traceback.print_exc()

        return JSONResponse(
            status_code=500,
            content={
                "ok": False,
                "mensaje": "Error al consultar alimento.",
                "detalle": str(e),
            },
        )


# =========================================================
# DESCONTAR ALIMENTO (AJUSTE MANUAL)
# =========================================================

@app.post("/api/alimentos/{alimento_id}/descontar")
def descontar_alimento(alimento_id: int):
    try:
        with obtener_conexion() as conn:
            asegurar_cupos_diarios(conn)

            with conn.cursor() as cur:
                alimento = consultar_cupo_actual(
                    cur,
                    alimento_id,
                    bloquear=True,
                )

                if alimento is None:
                    return JSONResponse(
                        status_code=404,
                        content={
                            "ok": False,
                            "mensaje": "Alimento no encontrado.",
                        },
                    )

                if not alimento[2]:
                    return JSONResponse(
                        status_code=400,
                        content={
                            "ok": False,
                            "mensaje": (
                                f"{alimento[1]} está inactivo."
                            ),
                        },
                    )

                cupo_id = alimento[3]
                cantidad = alimento[4]

                if cupo_id is None or cantidad is None:
                    return JSONResponse(
                        status_code=404,
                        content={
                            "ok": False,
                            "mensaje": "No existe un cupo para hoy.",
                        },
                    )

                if cantidad <= 0:
                    return JSONResponse(
                        status_code=400,
                        content={
                            "ok": False,
                            "mensaje": (
                                f"No quedan {alimento[1].lower()} "
                                "disponibles."
                            ),
                        },
                    )

                cur.execute(
                    """
                    UPDATE cupos_diarios
                    SET cantidad_disponible =
                            cantidad_disponible - 1,
                        cantidad_entregada =
                            COALESCE(cantidad_entregada, 0) + 1
                    WHERE id = %s
                      AND cantidad_disponible > 0
                    RETURNING
                        cantidad_disponible,
                        cantidad_entregada
                    """,
                    (cupo_id,),
                )

                resultado = cur.fetchone()

                if resultado is None:
                    return JSONResponse(
                        status_code=409,
                        content={
                            "ok": False,
                            "mensaje": (
                                "No fue posible descontar el cupo."
                            ),
                        },
                    )

                return {
                    "ok": True,
                    "id": alimento_id,
                    "nombre": alimento[1],
                    "cantidad_anterior": cantidad,
                    "cantidad": resultado[0],
                    "cantidad_disponible": resultado[0],
                    "cantidad_entregada": resultado[1],
                    "cupo_diario_id": cupo_id,
                }

    except Exception as e:
        traceback.print_exc()

        return JSONResponse(
            status_code=500,
            content={
                "ok": False,
                "mensaje": "Error al descontar alimento.",
                "detalle": str(e),
            },
        )
