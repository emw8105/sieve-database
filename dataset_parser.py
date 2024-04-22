import os

# Function used to filter the Wikipedia dataset to remove any entries that are not in English or have a viewcount of 1
def filter_wiki_data(input_file, output_file, stamp):
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
    datasets_directory = os.path.join(current_directory, "datasets")  # create a new directory called datasets
    os.makedirs(datasets_directory, exist_ok=True) 

    timestamps = ["000000", "010000", "020000", "030000"] # various timestamps for different instances of the dataset

    for timestamp in timestamps:
        input_file = os.path.join(current_directory, f"pagecounts-20160701-{timestamp}.txt") # ensure that the file is in the same directory as this script
        output_file = os.path.join(datasets_directory, f"Filtered_Wikipedia_Dataset_{timestamp}.txt")
        filter_wiki_data(input_file, output_file, timestamp)

# Function to parse the dataset files to extract the values and return it to be inserted into the B+ tree
def parse_dataset(dataset_file):
    with open(dataset_file, 'r') as file:
        for line in file:
            parts = line.strip().split(' ')
            if len(parts) == 5:
                language, page_name, viewcount, size, timestamp = parts
                yield language, page_name, int(viewcount), int(size), timestamp

# Function to check for rows with a specific viewcount in the dataset for testing purposes to compare with the B+ tree's search results
def check_viewcount(files, value, max_rows=10):
    rows = []
    for file in files:
        with open(file, 'r') as f:
            for line in f:
                columns = line.split()
                if len(columns) >= 3 and columns[2] == str(value):
                    rows.append(columns)
                    if len(rows) >= max_rows:
                        return rows
    return rows