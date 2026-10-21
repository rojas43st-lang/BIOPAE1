
import os
import re
from pathlib import Path

import psycopg
import qrcode
from dotenv import load_dotenv

# Cargar las variables de entorno
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

DATABASE_URL = os.getenv("DATABASE_URL")

CARPETA_QR = BASE_DIR / "codigos_qr"


def obtener_estudiantes():
    if not DATABASE_URL:
        raise RuntimeError(
            "No se encontró DATABASE_URL en el archivo .env"
        )

    consulta = """
        SELECT id, documento, nombre, apellido
        FROM estudiantes
        WHERE activo = TRUE
        ORDER BY id;
    """

    with psycopg.connect(
        DATABASE_URL,
        connect_timeout=15
    ) as conexion:
        with conexion.cursor() as cursor:
            cursor.execute(consulta)
            filas = cursor.fetchall()

    return filas


def generar_qr(estudiante_id):
    # El ID debe ser numérico porque así lo espera scanner.html
    codigo = str(estudiante_id)

    if not codigo.isdigit():
        raise ValueError(
            f"ID de estudiante no válido: {codigo}"
        )

    CARPETA_QR.mkdir(
        parents=True,
        exist_ok=True
    )

    imagen_qr = qrcode.make(codigo)

    ruta = CARPETA_QR / f"estudiante_{codigo}.png"
    imagen_qr.save(ruta)

    return ruta


def main():
    try:
        estudiantes = obtener_estudiantes()

        if not estudiantes:
            print("No hay estudiantes activos en Neon.")
            return

        print(f"Estudiantes encontrados: {len(estudiantes)}")

        for estudiante_id, documento, nombre, apellido in estudiantes:
            ruta = generar_qr(estudiante_id)

            print(
                f"ID: {estudiante_id} | "
                f"Estudiante: {nombre} {apellido} | "
                f"QR: {ruta}"
            )

        print("\nGeneración finalizada.")
        print(f"Carpeta: {CARPETA_QR}")

    except Exception as error:
        print(f"Error generando los QR: {error}")


if __name__ == "__main__":
    main()

