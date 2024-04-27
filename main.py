from bp_tree import Bp_Tree
from dataset_parser import parse_dataset
import time


### SETUP AND DATA INSERTION ###
# create a B+ tree
record_len = 40
bplustree = Bp_Tree(record_len)

# parse the dataset files and insert the viewcounts into the B+ tree
dataset_files = ['datasets/Filtered_Wikipedia_Dataset_000000.txt', 
                 'datasets/Filtered_Wikipedia_Dataset_010000.txt', 
                 'datasets/Filtered_Wikipedia_Dataset_020000.txt', 
                 'datasets/Filtered_Wikipedia_Dataset_030000.txt']

# enumerate over the dataset files, provides both the index of each file (i.e. block_index) and the file itself.
for block_index, dataset_file in enumerate(dataset_files):
    print(f"Processing block {block_index} from file {dataset_file}...")
    for record in parse_dataset(dataset_file):
        language, page_name, viewcount, size, timestamp = record
        bplustree.insert(int(viewcount), block_index)
    print(f"Finished processing block {block_index}.")

bplustree.partition_tree()


### TESTING ###
key_to_search = int(input("Enter a key to search for: "))  # get user input for test key
start_time = time.time()  # start the stopwatch for benchmarking query time
leaf_node = bplustree.search(key_to_search)
search_end_time = time.time()  # stop the stopwatch after the search

with open('query_output.txt', 'w') as f:  # open the output file in write mode
    record_start_time = time.time()  # start the stopwatch for the record searching
    record_count = 0  # initialize the record counter
    if leaf_node is not None:
        block_indices = leaf_node.key_pointer_map.get(key_to_search)
        if block_indices is not None:
            # for each block index associated with the key, parse the corresponding dataset file and print the rows with the key
            for block_index in block_indices:
                dataset_file = dataset_files[block_index]
                for record in parse_dataset(dataset_file):
                    language, page_name, viewcount, size, timestamp = record
                    if int(viewcount) == key_to_search:
                        print(record, file=f)  # print the record to the output file
                        record_count += 1  # increment the record counter
        else:
            print(f"Key {key_to_search} not found in the B+ tree.")
    else:
        print(f"Key {key_to_search} not found in the B+ tree.")

record_end_time = time.time()  # stop the stopwatch after the record searching
print("Query complete, results of query printed to query_output.txt.")
print(f"Tree search time: {format(search_end_time - start_time, '.10f')} seconds")  # print the tree search time
print(f"Record return time: {format(record_end_time - record_start_time, '.10f')} seconds")  # print the record search time
print(f"Number of records found: {record_count}")  # print the number of records found

print("\nPartition Information:")
bplustree.print_all_partitions()

# # print the B+ tree with all its keys and pointers
# bplustree.print_tree(bplustree.root)