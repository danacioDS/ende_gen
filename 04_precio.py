import pandas as pd
import os
from datetime import datetime, timedelta

# ----------------------------
# 1. Definir rutas de entrada y salida
# ----------------------------

# Ruta de entrada (archivo Excel)
download_folder = r"C:\Users\daniel.canedo\ende.ai\ende_gen\downloads"
input_file = os.path.join(download_folder, "merged_data.xlsx")

# Ruta de salida (carpeta data)
output_folder = r"C:\Users\daniel.canedo\ende.ai\ende_gen\ende_iny\data"
os.makedirs(output_folder, exist_ok=True)  # Crear carpeta si no existe

# ----------------------------
# 2. Cargar el archivo Excel
# ----------------------------
if not os.path.exists(input_file):
    raise FileNotFoundError(f"El archivo {input_file} no fue encontrado. Por favor verifique la ruta.")

try:
    df = pd.read_excel(input_file)
except Exception as e:
    print(f"Error al leer el archivo Excel: {e}")
    raise

# ----------------------------
# 3. Crear DataFrame de datos
# ----------------------------
data = {
    "CoD": [1996, 1996, 2018, 2019, 2014, 2016, 1996, 2009, 2014, 2016, 1996, 2015, 2017, 2018, 1996, 1996, 2012, 1996, 1999, 1996, 1996, 2000, 2001, 1998, 1999, 1999, 2017, 2007, 2010, 2019, 2014, 2015, 2011, 2017, 2017, 2019, 2019, 2021, 2021, 2021, 2022, 2019],
    "CENTRAL": ["Corani", "Santa Isabel", "San José I", "San José II", "Qollpana (Fase I)", "Qollpana (Fase II)", "Guaracachi", "Santa Cruz", "Santa Cruz (Unagro)", "Santa Cruz (EASBA)", "Aranjuez", "San Jacinto", "Yunchara", "Uyuni", "Valle Hermoso", "Carrasco", "C. El Alto", "Zongo", "Huaji (Zongo)", "Cumbre", "Miguillas", "Bulo Bulo (CECBB)", "Yura (ERESA)", "Taquesi", "Kanata en Arocagua", "Kanata en Valle Hermoso", "Guabirá/IAGSA", "Quehata", "Entre Ríos", "Entre Ríos II", "Del Sur", "Warnes", "C. Moxos", "Misicuni en Arocagua", "Misicuni en Valle Hermoso", "Solar Oruro (Fase I)", "Solar Oruro (Fase II)", "Eólica Warnes", "Eólica San Julián", "Eólica El Dorado", "Aguaí Energia", "Aguai (Autoproductor)"],
    "Tecnología": ["Hidro", "Hidro", "Hidro", "Hidro", "Eólica", "Eólica", "Termo", "Termo", "Biomasa", "Biomasa", "Termo", "Hidro", "Solar", "Solar", "Termo", "Termo", "Termo", "Hidro", "Hidro", "Hidro", "Hidro", "Termo", "Hidro", "Hidro", "Hidro", "Hidro", "Biomasa", "Hidro", "Termo", "Termo", "Termo", "Termo", "Termo", "Hidro", "Hidro", "Solar", "Solar", "Eólica", "Eólica", "Eólica", "Biomasa", "Biomasa"],
    "MW": [65.25, 91.11, 55, 69, 3, 24, 345.95, 41.95, 35, 5, 35.19, 7.6, 5, 60.06, 116.6, 133.36, 50.19, 62.68, 62.68, 62.68, 21.11, 135.45, 19.04, 89.19, 3.77, 3.77, 26, 1.97, 263.385, 263.385, 505.83, 570.57, 5.7, 60, 60, 50.01, 50.01, 14.4, 39.6, 54, 58.61, 10]
}

data = pd.DataFrame(data)

# ----------------------------
# 4. Unir datos con el Excel cargado
# ----------------------------
merge = data.merge(df, on="CENTRAL")

# ----------------------------
# 5. Generar columnas disponibles
# ----------------------------
def generate_column_names(prefix):
    """Genera nombres de columnas desde enero 2020 hasta el mes más reciente disponible."""
    start_date = datetime(2020, 1, 1)
    today = datetime.today()
    
    months = []
    current_date = start_date
    while current_date.year < today.year or (current_date.year == today.year and current_date.month < today.month):
        months.append(f"{prefix} US$/MWh {current_date.strftime('%m%y')}")
        current_date += timedelta(days=31)  # Avanza al siguiente mes
    
    return months

def generate_column_energia(prefix):
    """Genera nombres de columnas desde enero 2020 hasta el mes más reciente disponible."""
    start_date = datetime(2020, 1, 1)
    today = datetime.today()
    
    months = []
    current_date = start_date
    while current_date.year < today.year or (current_date.year == today.year and current_date.month < today.month):
        months.append(f"{prefix} kWh {current_date.strftime('%m%y')}")
        current_date += timedelta(days=31)  # Avanza al siguiente mes
    
    return months

# Generar nombres de columnas
subset_potencia = ["CoD", "CENTRAL", "Tecnología", "MW"] + generate_column_names("Potencia Firme")
subset_peaje = ["CoD", "CENTRAL", "Tecnología", "MW"] + generate_column_names("Peaje filiales ENDE")
subset_precio = ["CoD", "CENTRAL", "Tecnología", "MW"] + generate_column_names("PROMEDIO")
subset_energia = ["CoD", "CENTRAL", "Tecnología"] + generate_column_energia("Energía")

# ----------------------------
# 6. Filtrar columnas existentes
# ----------------------------
subset_potencia = [col for col in subset_potencia if col in merge.columns]
subset_energia = [col for col in subset_energia if col in merge.columns]
subset_peaje = [col for col in subset_peaje if col in merge.columns]
subset_precio = [col for col in subset_precio if col in merge.columns]

# ----------------------------
# 7. Guardar resultados
# ----------------------------
try:
    potencia = merge[subset_potencia]
    potencia.to_csv(os.path.join(output_folder, "potencia.csv"), index=False)

    energia = merge[subset_energia]
    energia.to_csv(os.path.join(output_folder, "energia.csv"), index=False)

    precio = merge[subset_precio]
    precio.to_csv(os.path.join(output_folder, "precio.csv"), index=False)

    peaje = merge[subset_peaje]
    peaje.to_csv(os.path.join(output_folder, "peaje.csv"), index=False)

    print(f"Archivos generados correctamente en: {output_folder}")
    print(f"- potencia.csv\n- energia.csv\n- precio.csv\n- peaje.csv")
    
except Exception as e:
    print(f"Error al guardar los archivos: {e}")
    raise