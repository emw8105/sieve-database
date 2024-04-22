# Modified version of Geeks for Geeks B+ tree

import math
from sortedcontainers import SortedDict, SortedList
from dataset_parser import parse_dataset

class Node:
    def __init__(self, order):
        self.order = order
        self.key_pointer_map = SortedDict() # key=int; pointer=SortedList() for leaf & left child Node for internal
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

        while(not current_node.leaf):
            child_index = current_node.key_pointer_map.bisect_right(key)
            if(child_index == len(current_node.key_pointer_map)):
                current_node = current_node.last_child_node
            else:
                next_key = current_node.key_pointer_map.keys()[child_index]
                current_node = current_node.key_pointer_map.get(next_key)
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



# create a B+ tree
record_len = 4
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



# TESTING
key_to_search = 10  # replace with desired test key, in this case will print all records in the tree with viewcount = 10
block_indices = bplustree.search(key_to_search).key_pointer_map.get(key_to_search)

# for each block index associated with the key, parse the corresponding dataset file and print the rows with the key
for block_index in block_indices:
    dataset_file = dataset_files[block_index]
    for record in parse_dataset(dataset_file):
        language, page_name, viewcount, size, timestamp = record
        if int(viewcount) == key_to_search:
            print(record)

leaf_array = bplustree.leaf_array()