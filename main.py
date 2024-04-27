from concurrent.futures import ThreadPoolExecutor
import concurrent.futures
from bp_tree import Bp_Tree
from dataset_parser import parse_dataset, search_block
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

# partition the B+ tree
print("Partitioning and Segmenting the B+ tree...")
bplustree.partition_tree()


### TESTING ###
key_to_search = int(input("Enter a key to search for: "))  # get user input for test key
start_time = time.time()  # start the stopwatch for benchmarking query time
leaf_node = bplustree.search(key_to_search)

buffered_records = []
buffer_size = 100

with open('query_output.txt', 'w') as f:  # open the output file in write mode
    record_count = 0  # initialize the record counter
    if leaf_node is not None:
        block_indices = leaf_node.key_pointer_map.get(key_to_search)
        if block_indices is not None:
            with ThreadPoolExecutor(max_workers=5) as executor:  # adjust max_workers based on your requirements
                future_to_block_index = {executor.submit(search_block, block_index, key_to_search, dataset_files): block_index for block_index in block_indices}
                for future in concurrent.futures.as_completed(future_to_block_index):
                    block_index = future_to_block_index[future]
                    try:
                        records = future.result()
                    except Exception as exc:
                        print(f'Block {block_index} generated an exception: {exc}')
                    else:
                        for record in records:
                            buffered_records.append(record)  # add the records to the buffer
                            record_count += 1  # increment the record counter
                            if len(buffered_records) >= buffer_size:
                                for record in buffered_records:
                                    print(record, file=f)  # print the records in the buffer to the output file
                                buffered_records.clear()  # clear the buffer
        else:
            print(f"Key {key_to_search} not found in the B+ tree.")
    else:
        print(f"Key {key_to_search} not found in the B+ tree.")

    # print any remaining records in the buffer
    for record in buffered_records:
        print(record, file=f)

end_time = time.time()  # stop the stopwatch after the record searching
print("Query complete, results of query printed to query_output.txt.")
print(f"Total return time: {format(end_time - start_time, '.10f')} seconds")  # print the total return time
print(f"Number of records found: {record_count}")  # print the number of records found

# # print the partitions of the B+ tree
# print("\nPartition Information:")
# bplustree.print_all_partitions()

# # print the B+ tree with all its keys and pointers
# bplustree.print_tree(bplustree.root)