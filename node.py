from sortedcontainers import SortedDict, SortedList

class Node:
    def __init__(self, order):
        self.order = order
        self.key_pointer_map = SortedDict() # key=int; pointer=SortedList() for leaf & left child Node for internal
        self.partitions = []
        self.last_child_node = None
        self.parent = None
        self.next_leaf_node = None
        self.leaf = False
    
    # inserts a key-pointer pair into the node
    def insert_at_leaf(self, key, pointer):
        if(key in self.key_pointer_map.keys()): # Key exists 
            if(pointer not in self.key_pointer_map.get(key)): # Pointer not in list
                self.key_pointer_map.get(key).add(pointer)
        else: # Key does not exist 
            self.key_pointer_map[key] = SortedList([pointer])
        # self.create_partitions()  # could technically make partitions on each insert, but paper uses an explicit method to handle it in bulk
    
    # creates partitions within the node by grouping contiguous keys with the same set of pointers
    def create_node_partitions(self):
        self.partitions.clear() # clear existing partitions
        keys = list(self.key_pointer_map.keys()) # get all keys
        if keys:
            # take the first key and iteratively compare it until finding a key that doesnt match
            # then create a partition with the start key, end key, and pointer list
            start_key = keys[0] 
            current_pointer_list = SortedList(self.key_pointer_map[start_key])
            for i in range(1, len(keys)):
                key = keys[i]
                pointer_list = SortedList(self.key_pointer_map[key])
                if pointer_list != current_pointer_list:
                    self.partitions.append((start_key, keys[i-1], current_pointer_list))
                    if keys[i-1] + 1 != key:
                        self.partitions.append((keys[i-1] + 1, key - 1, SortedList([])))
                    start_key = key
                    current_pointer_list = pointer_list
            self.partitions.append((start_key, keys[-1], current_pointer_list))