import pandas as pd

# Load the Excel file
xlsx_file = 'weather-almanac-2023.xlsx'
df = pd.read_excel(xlsx_file)

# Save as a CSV file
csv_file = 'weather-almanac-2023.csv'
df.to_csv(csv_file, index=False)

print(f"File converted successfully and saved as {csv_file}")