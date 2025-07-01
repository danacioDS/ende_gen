# importador_cndc.py

import os
import requests
import zipfile
from datetime import datetime, timedelta

# Obtener la ruta absoluta de la carpeta donde se encuentra este script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOWNLOAD_FOLDER = os.path.join(BASE_DIR, "downloads")

# Crear la carpeta "downloads" si no existe
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)


def generate_urls(start_date, end_date):
    """Genera una lista de URLs en función del rango de fechas especificado."""
    base_url = "https://www.cndc.bo/media/archivos/estadistica_mensual/c_iny_"
    urls = []
    current_date = start_date

    while current_date <= end_date:
        month_year = current_date.strftime("%m%y")  # Formato MMYY
        urls.append(f"{base_url}{month_year}.zip")
        current_date += timedelta(days=31)
        current_date = current_date.replace(day=1)

    return urls


def download_and_extract(url):
    """Descarga y extrae un archivo ZIP desde una URL."""
    filename = url.split("/")[-1]
    filepath = os.path.join(DOWNLOAD_FOLDER, filename)

    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(filepath, "wb") as file:
            file.write(response.content)
        print(f"Descargado: {filename}")

        with zipfile.ZipFile(filepath, "r") as zip_ref:
            zip_ref.extractall(DOWNLOAD_FOLDER)
            print(f"Extraído: {filename}")
            print("Archivos extraídos:", zip_ref.namelist())

        os.remove(filepath)
    else:
        print(f"Error al descargar {filename}. Código: {response.status_code}")


if __name__ == "__main__":
    # Definir rango de fechas para la generación automática de URLs
    start_date = datetime(2020, 1, 1)
    end_date = datetime.today()

    # Generar URLs dinámicamente y procesarlas
    urls = generate_urls(start_date, end_date)
    for url in urls:
        download_and_extract(url)

