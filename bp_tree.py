# Modified version of Geeks for Geeks B+ tree

import queue as q
import math
import time
from sortedcontainers import SortedDict, SortedList
from dataset_parser import check_viewcount, parse_dataset

class Node:
    def __init__(self, order):
        self.order = order
        self.key_pointer_map = SortedDict() # key=int; pointer=SortedList() for leaf & left child Node for internal
        self.partitions = []
        self.last_child_node = None
        self.parent = None
        self.next_leaf_node = None
        self.leaf = False
    
    def insert_at_leaf(self, key, pointer):
        if(key in self.key_pointer_map.keys()): # Key exists 
            if(pointer not in self.key_pointer_map.get(key)): # Pointer not in list
                self.key_pointer_map.get(key).add(pointer)
        else: # Key does not exist 
            self.key_pointer_map[key] = SortedList([pointer])
        # self.create_partitions()  # could technically make partitions on each insert, but paper uses an explicit method to handle it in bulk
    
    def create_node_partitions(self):
        self.partitions = []
        keys = list(self.key_pointer_map.keys())
        if keys:
            start_key = keys[0]
            current_pointer_list = self.key_pointer_map[start_key]
            for key in keys[1:]:
                pointer_list = self.key_pointer_map[key]
                if pointer_list != current_pointer_list:
                    self.partitions.append((start_key, key, current_pointer_list))
                    start_key = key
                    current_pointer_list = pointer_list
            # Add the last partition
            self.partitions.append((start_key, None, current_pointer_list))


    def print_partitions(self):
        for start_key, end_key, pointers in self.partitions:
            print(f"Start Key: {start_key}, End Key: {end_key}, Blocks: {pointers}")

class Bp_Tree:
    def __init__(self, order):
        self.root = Node(order)
        self.root.leaf = True

    def insert(self, key, pointer):
        old_node = self.search(key)
        old_node.insert_at_leaf(key, pointer)
        
        # Reshape tree due to overflow 
        if(len(old_node.key_pointer_map.keys()) == old_node.order):
            new_node = Node(old_node.order)
            new_node.leaf = True
            new_node.parent = old_node.parent
            mid = int(math.ceil((old_node.order - 1) / 2))
            new_node.key_pointer_map = SortedDict(old_node.key_pointer_map.items()[mid:])
            new_node.next_leaf_node = old_node.next_leaf_node  
            old_node.key_pointer_map = SortedDict(old_node.key_pointer_map.items()[:mid])
            old_node.next_leaf_node = new_node
            self.insert_in_parent(old_node, new_node.key_pointer_map.keys()[0], new_node)

    # Return leaf node for the given key
    def search(self, key):
        current_node = self.root
        while not current_node.leaf:
            if not current_node.partitions:
                # Old method
                child_index = current_node.key_pointer_map.bisect_right(key)
                if child_index == len(current_node.key_pointer_map):
                    current_node = current_node.last_child_node
                else:
                    next_key = current_node.key_pointer_map.keys()[child_index]
                    current_node = current_node.key_pointer_map.get(next_key)
            else:
                # New method
                for start_key, end_key, pointers in current_node.partitions:
                    if start_key <= key <= end_key:
                        current_node = pointers[0]
                        break
                else:
                    current_node = current_node.last_child_node
        return current_node

    # Return true if mapping exists; false otherwise
    def find(self, key, pointer):
        node_map = self.search(key).key_pointer_map
        if ((node_map.__contains__(key)) and (pointer in node_map.get(key))):
            return True
        else:
            return False
        
    def insert_in_parent(self, left, key, right):
        if(self.root == left):
            
            root_node = Node(left.order)
            root_node.key_pointer_map[key] = left
            root_node.last_child_node = right
            self.root = root_node
            left.parent = root_node
            right.parent = root_node
            return
        
        parent_node = left.parent

        child_nodes = list(parent_node.key_pointer_map.values())
        child_nodes.append(parent_node.last_child_node)
        for i in range(len(child_nodes)):
            if(child_nodes[i] == left):
                parent_node.key_pointer_map[key] = child_nodes[i]
                
                if(i == (len(child_nodes) - 1)):
                    parent_node.last_child_node = right
                else:
                    next_i_key = parent_node.key_pointer_map.keys()[i+1]
                    parent_node.key_pointer_map[next_i_key] = right
                
                if(len(parent_node.key_pointer_map.keys()) + 1 > parent_node.order):
                    parent_right = Node(parent_node.order)
                    parent_right.parent = parent_node.parent
                    mid = int(math.ceil((parent_node.order - 1) / 2)) 
                    parent_right.key_pointer_map = SortedDict(parent_node.key_pointer_map.items()[mid + 1:])
                    parent_right.last_child_node = parent_node.last_child_node
                    value_ = parent_node.key_pointer_map.keys()[mid]
                    
                    parent_node.key_pointer_map = SortedDict(parent_node.key_pointer_map.items()[:mid + 1])
                    if(mid != 0):
                        parent_node.last_child_node = parent_node.key_pointer_map.values()[mid]
                        parent_node.key_pointer_map.popitem()

                    for p in parent_node.key_pointer_map.values():
                        p.parent = parent_node
                    for p in parent_right.key_pointer_map.values():
                        p.parent = parent_right
                    
                    print("Parential overflow, splitting into: " + str(parent_node.key_pointer_map.keys()) + " and " + str(parent_right.key_pointer_map.keys()))
                    
                    self.insert_in_parent(parent_node, value_, parent_right)

    def get_leftmost_node(self):
        node = self.root
        while not node.leaf:
            node = node.key_pointer_map.peekitem(0)[1]  # Get the first child node
        return node
    
    def partition_tree(self):
        # Start from the leftmost leaf node
        current_node = self.root
        while not current_node.leaf:
            current_node = current_node.key_pointer_map.values()[0]

        # Traverse the tree and partition each node
        while current_node is not None:
            current_node.create_node_partitions()
            current_node = current_node.next_leaf_node

    def print_all_partitions(self):
        node = self.get_leftmost_node()
        while node is not None:
            for start_key, end_key, pointer_list in node.partitions:
                print(f"  Partition: start_key={start_key}, end_key={end_key}, pointer_list={pointer_list}")
            node = node.next_leaf_node
    
    def print_all_key_pointer_maps(self):
        node = self.get_leftmost_node()
        while node is not None:
            print(f"Node {node}:")
            for key, pointer_list in node.key_pointer_map.items():
                print(f"  Key: {key}, Pointer List: {pointer_list}")
            node = node.next_leaf_node

    # Return leaf array
    def leaf_array(self):
        current_leaf = self.root
        while(not current_leaf.leaf):
            current_leaf = current_leaf.key_pointer_map.values()[0]
        
        leaf_array = []
        while(current_leaf is not None):
            for i, item in enumerate(list(current_leaf.key_pointer_map.items())):
                leaf_array.append(item)
            current_leaf = current_leaf.next_leaf_node
        return leaf_array

    # prints the values of all keys with their corresponding pointers in the B+ tree
    def print_tree(self, node):
        if node is None:
            return

        # Print keys and pointers of the current node
        for key, pointers in node.key_pointer_map.items():
            print(f"Key: {key}, Pointers: {pointers}")

        # If the node is not a leaf, recursively print its child nodes
        if not node.leaf:
            for child_node in node.key_pointer_map.values():
                self.print_tree(child_node)

        # Print the last child node if it exists
        if node.last_child_node is not None:
            self.print_tree(node.last_child_node)


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