# converts a text file into a csv file by splitting each line by a tab (this is for extracting weather.csv)
# used to extract data from: https://stateclimatologist.web.illinois.edu/data/champaign-urbana/

import csv

# Input and output file paths
input_file_path = 'input_data/weather_data_raw.txt'  # Replace with your text file's name
output_file_path = 'input_data/full_weather_data_2023.csv'  # Replace with your desired CSV file name

# Open the input text file
with open(input_file_path, 'r') as infile:
    # Read all lines from the file
    lines = infile.readlines()

    # Get column names from the second line
    column_names = lines[0].strip().split(', ')  # Strip and split by tab
    print(column_names)

    # Get data starting from the third line
    data_lines = lines[1:]

# for line in data_lines:

month = "01"

# Write to a CSV file
with open(output_file_path, 'w', newline='') as outfile:
    csv_writer = csv.writer(outfile)

    # Write column names as the header row
    csv_writer.writerow(column_names)

    # Write the remaining rows of data
    for line in data_lines:
        ls = line.strip().split('\t')
        print(ls)
        ls[1] = f"2023-{int(ls[0]):02d}-{int(ls[1]):02d}"
        csv_writer.writerow(ls)  # Strip and split by tab

print(f"Text file has been successfully converted to {output_file_path}")
