import os
from datetime import datetime

import pandas as pd

# Ruta de la carpeta de descargas
base_dir = os.path.dirname(os.path.abspath(__file__))
download_folder = os.path.join(base_dir, "downloads")


def extract_month_year(filename):
    """Extrae el mes y año del nombre del archivo."""
    month_year = filename.split("_")[3].split(".")[0]
    return datetime.strptime(month_year, "%m%y")


def rename_columns(df, month_year):
    """Renombra columnas de forma dinámica según el número real de columnas."""
    col_count = len(df.columns)
    default_cols = ["CENTRAL"]
    possible_names = [
        f"Energía kWh {month_year.strftime('%m%y')}",
        f"Potencia Firme Remunerada kW {month_year.strftime('%m%y')}",
        f"Peaje filiales ENDE US$/MWh {month_year.strftime('%m%y')}",
        f"PROMEDIO US$/MWh {month_year.strftime('%m%y')}"
    ]
    new_col_names = default_cols + possible_names[:col_count - 1]
    return new_col_names


def merge_extracted_files(folder):
    """Fusiona todos los archivos extraídos respetando el orden cronológico."""
    data_frames = []

    for file in os.listdir(folder):
        if file.startswith("extracted_") and file.endswith(".xlsx"):
            filepath = os.path.join(folder, file)
            try:
                df = pd.read_excel(filepath)
                month_year = extract_month_year(file)

                # Renombrar columnas con el número exacto de columnas
                df.columns = rename_columns(df, month_year)

                # Filtrar filas vacías o totales
                df = df.dropna(subset=['CENTRAL'])
                df = df[~df['CENTRAL'].str.contains("TOTAL", na=False)]

                data_frames.append((month_year, df))
                print(f"✅ {file} procesado correctamente.")
            except Exception as e:
                print(f"❌ Error al procesar {file}: {e}")

    if not data_frames:
        print("⚠️ No se encontraron archivos válidos.")
        return

    # Ordenar y fusionar
    data_frames.sort(key=lambda x: x[0])
    merged_df = data_frames[0][1]

    for _, df in data_frames[1:]:
        merged_df = merged_df.merge(df, on="CENTRAL", how="outer")

    merged_df = merged_df.dropna(how="all")
    output_file = os.path.join(folder, "merged_data.xlsx")
    merged_df.to_excel(output_file, index=False)
    print(f"✅ Archivo fusionado guardado en: {output_file}")


# Ejecutar fusión
merge_extracted_files(download_folder)


