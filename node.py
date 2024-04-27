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
    
    def insert_at_leaf(self, key, pointer):
        if(key in self.key_pointer_map.keys()): # Key exists 
            if(pointer not in self.key_pointer_map.get(key)): # Pointer not in list
                self.key_pointer_map.get(key).add(pointer)
        else: # Key does not exist 
            self.key_pointer_map[key] = SortedList([pointer])
        # self.create_partitions()  # could technically make partitions on each insert, but paper uses an explicit method to handle it in bulk
    
    def create_node_partitions(self):
        self.partitions.clear()
        keys = list(self.key_pointer_map.keys())
        if keys:
            start_key = keys[0]
            current_pointer_list = self.key_pointer_map[start_key]
            for i in range(1, len(keys)):
                key = keys[i]
                pointer_list = self.key_pointer_map[key]
                if pointer_list != current_pointer_list:
                    self.partitions.append((start_key, keys[i-1], current_pointer_list))
                    start_key = key
                    current_pointer_list = pointer_list
            self.partitions.append((start_key, keys[-1], current_pointer_list))