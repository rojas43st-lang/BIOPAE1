import os
import traceback
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import psycopg
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


# =========================================================
# CREAR APLICACIÓN
# =========================================================

app = FastAPI()


# =========================================================
# ARCHIVOS ESTÁTICOS Y PLANTILLAS
# =========================================================

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)

templates = Jinja2Templates(directory="templates")


# =========================================================
# CONEXIÓN A NEON
# =========================================================

DATABASE_URL = os.getenv("DATABASE_URL")

ZONA_HORARIA = ZoneInfo("America/Bogota")

# Tiempo de reutilización del QR.
TIEMPO_REUTILIZACION_HORAS = 15

# Cantidades que deben quedar disponibles al comenzar un nuevo día.
CANTIDAD_INICIAL_VASO = 50
CANTIDAD_INICIAL_ALMUERZO = 80


def obtener_conexion():
    if not DATABASE_URL:
        raise Exception("No se encontró DATABASE_URL")

    conn = psycopg.connect(DATABASE_URL)

    # Asegura que CURRENT_DATE y CURRENT_TIME de PostgreSQL
    # correspondan a la hora de Colombia.
    with conn.cursor() as cur:
        cur.execute("SET TIME ZONE 'America/Bogota'")

    return conn


def asegurar_reinicio_diario(conn):
    """
    Reinicia las cantidades una vez cuando comienza un nuevo día.

    La primera vez que se usa esta función crea el control del día
    pero NO cambia las cantidades actuales. A partir del día siguiente,
    sí restablece vaso de leche y almuerzo a sus cantidades iniciales.
    """

    with conn.cursor() as cur:

        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS pae_control_diario (
                id INTEGER PRIMARY KEY,
                fecha_ultimo_reinicio DATE NOT NULL
            )
            """
        )

        hoy = datetime.now(ZONA_HORARIA).date()

        cur.execute(
            """
            SELECT fecha_ultimo_reinicio
            FROM pae_control_diario
            WHERE id = 1
            """
        )

        control = cur.fetchone()

        if control is None:
            cur.execute(
                """
                INSERT INTO pae_control_diario (
                    id,
                    fecha_ultimo_reinicio
                )
                VALUES (1, %s)
                """,
                (hoy,)
            )

            conn.commit()
            return

        ultima_fecha = control[0]

        if ultima_fecha != hoy:

            cur.execute(
                """
                UPDATE alimentos
                SET cantidad = CASE
                    WHEN id = 1 THEN %s
                    WHEN id = 2 THEN %s
                    ELSE cantidad
                END
                WHERE id IN (1, 2)
                """,
                (
                    CANTIDAD_INICIAL_VASO,
                    CANTIDAD_INICIAL_ALMUERZO
                )
            )

            cur.execute(
                """
                UPDATE pae_control_diario
                SET fecha_ultimo_reinicio = %s
                WHERE id = 1
                """,
                (hoy,)
            )

            conn.commit()


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
                    "resultado": resultado[0]
                }

    except Exception as e:
        traceback.print_exc()
        return {
            "conexion": "error",
            "detalle": str(e)
        }




# =========================================================
# INICIO DE SESIÓN (HTMX)
# =========================================================

@app.post("/login", response_class=HTMLResponse)
async def iniciar_sesion(
    usuario: str = Form(...),
    contrasena: str = Form(...)
):
    admin_usuario = os.getenv("ADMIN_USER")
    admin_contrasena = os.getenv("ADMIN_PASSWORD")

    if not admin_usuario or not admin_contrasena:
        return HTMLResponse(
            '<p role="alert">Faltan las credenciales del administrador en .env.</p>',
            status_code=500
        )

    if usuario == admin_usuario and contrasena == admin_contrasena:
        return HTMLResponse(
            content="",
            headers={"HX-Redirect": "/menu"}
        )

    return HTMLResponse(
        '<p role="alert">Usuario o contraseña incorrectos.</p>',
        status_code=401
    )


# =========================================================
# PÁGINAS
# =========================================================

@app.get("/", response_class=HTMLResponse)
async def inicio(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"request": request}
    )


@app.get("/menu", response_class=HTMLResponse)
async def menu(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="menu.html",
        context={"request": request}
    )


@app.get("/vaso", response_class=HTMLResponse)
async def vaso(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="vaso.html",
        context={"request": request}
    )


@app.get("/almuerzo", response_class=HTMLResponse)
async def almuerzo(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="almuerzo.html",
        context={"request": request}
    )


@app.get("/scanner", response_class=HTMLResponse)
async def scanner(request: Request):
    alimento_id = request.query_params.get("alimento")

    if alimento_id not in ["1", "2"]:
        alimento_id = "1"

    return templates.TemplateResponse(
        request=request,
        name="scanner.html",
        context={
            "request": request,
            "alimento_id": alimento_id
        }
    )




# =========================================================
# FRAGMENTOS HTML PARA HTMX
# =========================================================

@app.get("/fragmentos/alimentos/{alimento_id}/cantidad", response_class=HTMLResponse)
async def fragmento_cantidad_alimento(request: Request, alimento_id: int):
    if alimento_id not in (1, 2):
        return HTMLResponse(
            '<p class="mensaje-error">Alimento no válido.</p>',
            status_code=400
        )

    try:
        with obtener_conexion() as conn:
            asegurar_reinicio_diario(conn)
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT nombre, cantidad, activo
                    FROM alimentos
                    WHERE id = %s
                    """,
                    (alimento_id,)
                )
                alimento = cur.fetchone()

        if alimento is None:
            return HTMLResponse(
                '<p class="mensaje-error">Alimento no encontrado.</p>',
                status_code=404
            )

        nombre, cantidad, activo = alimento
        if not activo:
            return HTMLResponse(
                '<p class="mensaje-error">Este alimento está inactivo.</p>',
                status_code=400
            )

        return templates.TemplateResponse(
            request=request,
            name="partials/cantidad_alimento.html",
            context={
                "request": request,
                "nombre": nombre,
                "cantidad": cantidad,
                "alimento_id": alimento_id,
            }
        )
    except Exception:
        traceback.print_exc()
        return HTMLResponse(
            '<p class="mensaje-error">No se pudo consultar la cantidad. Verifica la conexión con la base de datos.</p>',
            status_code=500
        )


# =========================================================
# CONSULTAR ALIMENTO
# =========================================================

@app.get("/api/alimentos/{alimento_id}")
async def consultar_alimento(alimento_id: int):
    try:
        with obtener_conexion() as conn:

            asegurar_reinicio_diario(conn)

            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT id, nombre, cantidad, activo
                    FROM alimentos
                    WHERE id = %s
                    """,
                    (alimento_id,)
                )

                alimento = cur.fetchone()

                if alimento is None:
                    return JSONResponse(
                        status_code=404,
                        content={
                            "ok": False,
                            "mensaje": "Alimento no encontrado."
                        }
                    )

                return {
                    "ok": True,
                    "id": alimento[0],
                    "nombre": alimento[1],
                    "cantidad": alimento[2],
                    "activo": alimento[3]
                }

    except Exception as e:
        traceback.print_exc()
        return JSONResponse(
            status_code=500,
            content={
                "ok": False,
                "mensaje": "Error consultando alimento.",
                "detalle": str(e)
            }
        )


# =========================================================
# ESCANEO QR Y ENTREGA
# =========================================================
#
# El QR del estudiante debe contener su ID.
# Ejemplo:
#     1
#
# El frontend envía:
# {
#     "estudiante_id": 1,
#     "alimento_id": 1
# }
#
# alimento_id = 1 -> Vaso de leche
# alimento_id = 2 -> Almuerzo
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
                "mensaje": "Faltan datos del escaneo."
            }
        )

    try:
        estudiante_id = int(estudiante_id)
        alimento_id = int(alimento_id)
    except (ValueError, TypeError):
        return JSONResponse(
            status_code=400,
            content={
                "ok": False,
                "mensaje": "El ID recibido no es válido."
            }
        )

    if alimento_id not in (1, 2):
        return JSONResponse(
            status_code=400,
            content={
                "ok": False,
                "mensaje": "El alimento seleccionado no es válido."
            }
        )

    try:
        with obtener_conexion() as conn:

            # Reiniciar alimentos si comenzó un nuevo día.
            asegurar_reinicio_diario(conn)

            with conn.cursor() as cur:

                # -------------------------------------------------
                # BUSCAR ESTUDIANTE
                # -------------------------------------------------

                cur.execute(
                    """
                    SELECT id, nombre, apellido
                    FROM estudiantes
                    WHERE id = %s
                    AND activo = TRUE
                    """,
                    (estudiante_id,)
                )

                estudiante = cur.fetchone()

                if estudiante is None:
                    return JSONResponse(
                        status_code=404,
                        content={
                            "ok": False,
                            "mensaje": "El estudiante no existe o está inactivo."
                        }
                    )

                # -------------------------------------------------
                # COMPROBAR BLOQUEO DE 15 HORAS DEL QR
                # -------------------------------------------------

                cur.execute(
                    """
                    SELECT fecha, hora
                    FROM entregas
                    WHERE estudiante_id = %s
                    ORDER BY fecha DESC, hora DESC
                    LIMIT 1
                    """,
                    (estudiante_id,)
                )

                ultima_entrega = cur.fetchone()

                ahora = datetime.now(ZONA_HORARIA).replace(tzinfo=None)

                if ultima_entrega:

                    ultima_fecha = ultima_entrega[0]
                    ultima_hora = ultima_entrega[1]

                    ultima_fecha_hora = datetime.combine(
                        ultima_fecha,
                        ultima_hora
                    )

                    siguiente_uso = (
                        ultima_fecha_hora
                        + timedelta(hours=TIEMPO_REUTILIZACION_HORAS)
                    )

                    if ahora < siguiente_uso:

                        restante = siguiente_uso - ahora
                        segundos = max(
                            0,
                            int(restante.total_seconds())
                        )

                        horas = segundos // 3600
                        minutos = (segundos % 3600) // 60

                        return JSONResponse(
                            status_code=409,
                            content={
                                "ok": False,
                                "motivo": "qr_bloqueado",
                                "mensaje": (
                                    f"{estudiante[1]} {estudiante[2]} "
                                    f"no puede reutilizar el código QR todavía."
                                ),
                                "horas_restantes": horas,
                                "minutos_restantes": minutos,
                                "proximo_uso": siguiente_uso.isoformat()
                            }
                        )

                # -------------------------------------------------
                # BUSCAR ALIMENTO
                # -------------------------------------------------

                cur.execute(
                    """
                    SELECT id, nombre, cantidad
                    FROM alimentos
                    WHERE id = %s
                    AND activo = TRUE
                    FOR UPDATE
                    """,
                    (alimento_id,)
                )

                alimento = cur.fetchone()

                if alimento is None:
                    return JSONResponse(
                        status_code=404,
                        content={
                            "ok": False,
                            "mensaje": "El alimento no existe o está inactivo."
                        }
                    )

                alimento_id_db = alimento[0]
                alimento_nombre = alimento[1]
                cantidad = alimento[2]

                if cantidad <= 0:
                    return JSONResponse(
                        status_code=400,
                        content={
                            "ok": False,
                            "mensaje": f"No quedan {alimento_nombre} disponibles."
                        }
                    )

                # -------------------------------------------------
                # DESCONTAR ALIMENTO
                # -------------------------------------------------

                cur.execute(
                    """
                    UPDATE alimentos
                    SET cantidad = cantidad - 1
                    WHERE id = %s
                    AND cantidad > 0
                    RETURNING cantidad
                    """,
                    (alimento_id_db,)
                )

                resultado = cur.fetchone()

                if resultado is None:
                    return JSONResponse(
                        status_code=400,
                        content={
                            "ok": False,
                            "mensaje": "No fue posible descontar el alimento."
                        }
                    )

                cantidad_restante = resultado[0]

                # -------------------------------------------------
                # REGISTRAR ENTREGA
                # -------------------------------------------------

                ahora_bd = datetime.now(ZONA_HORARIA)

                cur.execute(
                    """
                    INSERT INTO entregas (
                        estudiante_id,
                        alimento_id,
                        fecha,
                        hora,
                        estado,
                        observacion
                    )
                    VALUES (
                        %s,
                        %s,
                        %s,
                        %s,
                        'entregado',
                        'Entrega realizada mediante código QR'
                    )
                    """,
                    (
                        estudiante_id,
                        alimento_id_db,
                        ahora_bd.date(),
                        ahora_bd.time()
                    )
                )

                conn.commit()

                siguiente_uso = (
                    ahora_bd.replace(tzinfo=None)
                    + timedelta(hours=TIEMPO_REUTILIZACION_HORAS)
                )

                return {
                    "ok": True,
                    "mensaje": "Entrega registrada correctamente.",
                    "estudiante_id": estudiante[0],
                    "estudiante": f"{estudiante[1]} {estudiante[2]}",
                    "alimento_id": alimento_id_db,
                    "alimento": alimento_nombre,
                    "cantidad_restante": cantidad_restante,
                    "qr_reutilizable_en_horas": TIEMPO_REUTILIZACION_HORAS,
                    "proximo_uso_qr": siguiente_uso.isoformat()
                }

    except Exception as e:
        traceback.print_exc()

        return JSONResponse(
            status_code=500,
            content={
                "ok": False,
                "mensaje": "Error al procesar el escaneo.",
                "detalle": str(e)
            }
        )


# =========================================================
# CONSULTAR ENTREGAS
# =========================================================

@app.get("/api/entregas")
async def consultar_entregas(fecha: str = None):

    try:
        with obtener_conexion() as conn:
            with conn.cursor() as cur:

                if not fecha:
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
                        FROM entregas e
                        JOIN estudiantes est
                            ON est.id = e.estudiante_id
                        JOIN alimentos a
                            ON a.id = e.alimento_id
                        WHERE e.fecha = CURRENT_DATE
                        ORDER BY e.hora DESC
                        """
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
                        FROM entregas e
                        JOIN estudiantes est
                            ON est.id = e.estudiante_id
                        JOIN alimentos a
                            ON a.id = e.alimento_id
                        WHERE e.fecha = %s
                        ORDER BY e.hora DESC
                        """,
                        (fecha,)
                    )

                entregas = cur.fetchall()

                resultado = []

                for entrega in entregas:
                    resultado.append({
                        "id": entrega[0],
                        "estudiante_id": entrega[1],
                        "nombre": entrega[2],
                        "apellido": entrega[3],
                        "alimento_id": entrega[4],
                        "alimento": entrega[5],
                        "fecha": str(entrega[6]),
                        "hora": str(entrega[7]),
                        "estado": entrega[8],
                        "observacion": entrega[9]
                    })

                return {
                    "ok": True,
                    "total": len(resultado),
                    "entregas": resultado
                }

    except Exception as e:
        traceback.print_exc()
        return JSONResponse(
            status_code=500,
            content={
                "ok": False,
                "mensaje": "Error consultando las entregas.",
                "detalle": str(e)
            }
        )


# =========================================================
# OBTENER ALIMENTO
# =========================================================

@app.get("/api/alimentos/{alimento_id}/detalle")
def obtener_alimento(alimento_id: int):

    try:
        with obtener_conexion() as conn:

            asegurar_reinicio_diario(conn)

            with conn.cursor() as cur:

                cur.execute(
                    """
                    SELECT id, nombre, cantidad, activo
                    FROM alimentos
                    WHERE id = %s
                    """,
                    (alimento_id,)
                )

                alimento = cur.fetchone()

                if alimento is None:
                    return JSONResponse(
                        status_code=404,
                        content={
                            "ok": False,
                            "mensaje": "Alimento no encontrado"
                        }
                    )

                return {
                    "ok": True,
                    "id": alimento[0],
                    "nombre": alimento[1],
                    "cantidad": alimento[2],
                    "activo": alimento[3]
                }

    except Exception as e:
        traceback.print_exc()
        return JSONResponse(
            status_code=500,
            content={
                "ok": False,
                "mensaje": "Error al consultar alimento",
                "detalle": str(e)
            }
        )


# =========================================================
# DESCONTAR ALIMENTO
# =========================================================

@app.post("/api/alimentos/{alimento_id}/descontar")
def descontar_alimento(alimento_id: int):

    try:
        with obtener_conexion() as conn:

            asegurar_reinicio_diario(conn)

            with conn.cursor() as cur:

                cur.execute(
                    """
                    SELECT id, nombre, cantidad, activo
                    FROM alimentos
                    WHERE id = %s
                    FOR UPDATE
                    """,
                    (alimento_id,)
                )

                alimento = cur.fetchone()

                if alimento is None:
                    return JSONResponse(
                        status_code=404,
                        content={
                            "ok": False,
                            "mensaje": "Alimento no encontrado"
                        }
                    )

                cantidad = alimento[2]
                nombre = alimento[1]
                activo = alimento[3]

                if not activo:
                    return JSONResponse(
                        status_code=400,
                        content={
                            "ok": False,
                            "mensaje": f"{nombre} está inactivo"
                        }
                    )

                if cantidad <= 0:
                    return JSONResponse(
                        status_code=400,
                        content={
                            "ok": False,
                            "mensaje": f"No quedan {nombre.lower()} disponibles"
                        }
                    )

                nueva_cantidad = cantidad - 1

                cur.execute(
                    """
                    UPDATE alimentos
                    SET cantidad = %s
                    WHERE id = %s
                    """,
                    (nueva_cantidad, alimento_id)
                )

                conn.commit()

                return {
                    "ok": True,
                    "id": alimento_id,
                    "nombre": nombre,
                    "cantidad_anterior": cantidad,
                    "cantidad": nueva_cantidad
                }

    except Exception as e:
        traceback.print_exc()
        return JSONResponse(
            status_code=500,
            content={
                "ok": False,
                "mensaje": "Error al descontar alimento",
                "detalle": str(e)
            }
        )
