import os
import pandas as pd

# Obtener la ruta absoluta de la carpeta donde se encuentra este script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Definir la carpeta "downloads" como subcarpeta de BASE_DIR
DOWNLOAD_FOLDER = os.path.join(BASE_DIR, "downloads")


def extract_columns_and_save(folder):
    """
    Extrae las columnas CENTRAL, Peaje filiales ENDE US$/MWh y PROMEDIO US$/MWh
    de cada archivo .xlsx y guarda en un nuevo archivo.
    """
    for file in os.listdir(folder):
        if file.endswith(".xlsx"):
            filepath = os.path.join(folder, file)
            try:
                # Leer el archivo Excel
                df = pd.read_excel(filepath)

                # Seleccionar columnas específicas por índice
                df = df.iloc[:, [0, 1, 5, 18, 21]]

                # Renombrar columnas
                df.columns = [
                    "CENTRAL",
                    "Energía",
                    "Potencia Firme Remunerada",
                    "Peaje filiales ENDE US$/MWh",
                    "PROMEDIO US$/MWh"
                ]

                # Guardar archivo con las columnas extraídas
                output_file = os.path.join(folder, f"extracted_{file}")
                df.to_excel(output_file, index=False)
                print(f"✅ Archivo {file} procesado y guardado como {output_file}.")
            except Exception as e:
                print(f"❌ Error al procesar {file}: {e}")


if __name__ == "__main__":
    extract_columns_and_save(DOWNLOAD_FOLDER)