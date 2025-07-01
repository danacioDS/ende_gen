import os
from datetime import datetime, timedelta

import pandas as pd


def generate_months_order(df):
    """Generate months order dynamically from the columns in the DataFrame."""
    energy_columns = [col for col in df.columns if col.startswith('PROMEDIO US$/MWh')]

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
    """Process energy CSV file and export average monthly prices."""
    df = pd.read_csv(input_file)

    # Generate months order dynamically
    months_order = generate_months_order(df)

    # Filter only the energy columns
    energy_columns = [
        f'PROMEDIO US$/MWh {month}' for month in months_order
        if f'PROMEDIO US$/MWh {month}' in df.columns
    ]

    # Calculate the mean for each energy column
    totals = df[energy_columns].mean()

    # Create a new DataFrame with the totals
    result_df = pd.DataFrame([totals.values], columns=totals.index, index=['TOTALES'])

    # Add the CENTRAL column
    result_df.insert(0, 'CENTRAL', 'TOTALES')

    # Create output directory if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Save to CSV in the data folder
    output_path = os.path.join(output_folder, 'precios_promedio.csv')
    result_df.to_csv(output_path, index=False, float_format='%.1f')
    print(f"File saved as {output_path}")


# Usage
if __name__ == '__main__':
    input_file = 'ende_iny/data/precio.csv'
    output_folder = 'ende_iny/data'
    process_energy_file(input_file, output_folder)
