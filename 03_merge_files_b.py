import os
import re
from datetime import datetime
import pandas as pd

# Ruta de la carpeta de descargas
base_dir = os.path.dirname(os.path.abspath(__file__))
download_folder = os.path.join(base_dir, "downloads")


def extract_month_year(filename):
    """Extrae el mes y año (MMYY) del nombre del archivo usando regex."""
    match = re.search(r'_(\d{4})\.xlsx$', filename)
    if match:
        return datetime.strptime(match.group(1), "%m%y")
    else:
        raise ValueError(f"No se pudo extraer MMYY de: {filename}")


def rename_columns(df, month_year):
    """Renombra columnas de forma dinámica según el número real de columnas."""
    col_count = len(df.columns)
    default_cols = ["CENTRAL"]
    possible_names = [
        f"Precio Energía US$/MWh {month_year.strftime('%m%y')}",
        f"Ingresos Energía US$ {month_year.strftime('%m%y')}",
        f"Precio Potencia US$/kW {month_year.strftime('%m%y')}",
        f"Ingreso Potencia US$ {month_year.strftime('%m%y')}",
        f"Ingreso Total US$ {month_year.strftime('%m%y')}"
    ]
    new_col_names = default_cols + possible_names[:col_count - 1]
    return new_col_names


def merge_extracted_files(folder):
    """Fusiona todos los archivos extraídos respetando el orden cronológico."""
    data_frames = []

    for file in os.listdir(folder):
        if re.match(r"^extracted_2_.*_(\d{4})\.xlsx$", file):
            filepath = os.path.join(folder, file)
            try:
                month_year = extract_month_year(file)
                df = pd.read_excel(filepath)

                # Renombrar columnas según mes y año
                df.columns = rename_columns(df, month_year)

                # Filtrar filas vacías o con "TOTAL"
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
    output_file = os.path.join(folder, "merged_data_b.xlsx")
    merged_df.to_excel(output_file, index=False)
    print(f"✅ Archivo fusionado guardado en: {output_file}")


# Ejecutar fusión
merge_extracted_files(download_folder)

