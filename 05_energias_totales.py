import pandas as pd
import os
from datetime import datetime, timedelta

def generate_months_order(df):
    """Generate months order dynamically from the columns in the DataFrame"""
    energy_columns = [col for col in df.columns if col.startswith('Energía kWh')]
    
    # Extract month-year codes from column names
    month_codes = [col.split()[-1] for col in energy_columns]
    
    # Convert to datetime objects for proper sorting
    dates = []
    for code in month_codes:
        try:
            date = datetime.strptime(code, '%m%y')
            dates.append(date)
        except ValueError:
            continue
    
    # Sort dates chronologically
    dates.sort()
    
    # Convert back to month-year codes in the correct order
    months_order = [date.strftime('%m%y') for date in dates]
    
    return months_order

def process_energy_file(input_file, output_folder):
    # Read the input CSV file
    df = pd.read_csv(input_file)
    
    # Generate months order dynamically
    months_order = generate_months_order(df)
    
    # Filter only the energy columns (columns that start with "Energía kWh")
    energy_columns = [f'Energía kWh {month}' for month in months_order 
                     if f'Energía kWh {month}' in df.columns]
    
    # Calculate the sum for each energy column
    totals = df[energy_columns].sum()
    
    # Create a new DataFrame with the totals
    result_df = pd.DataFrame([totals.values], columns=totals.index, index=['TOTALES'])
    
    # Add the CENTRAL column
    result_df.insert(0, 'CENTRAL', 'TOTALES')
    
    # Create output directory if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)
    
    # Save to CSV in the data folder
    output_path = os.path.join(output_folder, 'energias_totales.csv')
    result_df.to_csv(output_path, index=False, float_format='%.1f')
    print(f"File saved as {output_path}")

# Usage - point to the energia.csv in the data folder and output to data folder
input_file = 'ende_iny/data/energia.csv'
output_folder = 'ende_iny/data'
process_energy_file(input_file, output_folder)