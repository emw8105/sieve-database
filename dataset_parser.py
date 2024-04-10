import os


def filter_data(input_file, output_file, stamp):
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    filtered_lines = []
    print(f"Filtering data for timestamp: {stamp}")
    for line in lines:
        columns = line.strip().split(' ')
        if columns[0].startswith('en') and '%' not in columns[1] and columns[2] != '1':
            line_with_timestamp = f"{line.strip()} {stamp}\n"
            filtered_lines.append(line_with_timestamp)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.writelines(filtered_lines)

if __name__ == "__main__":
    current_directory = os.getcwd()  # get the current working directory
    timestamps = ["000000", "010000", "020000", "030000"]

    for timestamp in timestamps:
        input_file = os.path.join(current_directory, f"pagecounts-20160701-{timestamp}.txt") # ensure that the file is in the same directory as this script
        output_file = os.path.join(current_directory, f"Filtered_dataset_{timestamp}.txt")
        filter_data(input_file, output_file, timestamp)
