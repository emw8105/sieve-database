# Modified version of Geeks for Geeks B+ tree

import math
from sortedcontainers import SortedDict, SortedList

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
            mid = int(math.ceil(old_node.order / 2)) - 1
            new_node.key_pointer_map = SortedDict(old_node.key_pointer_map.items()[mid + 1:])
            new_node.next_leaf_node = old_node.next_leaf_node  
            old_node.key_pointer_map = SortedDict(old_node.key_pointer_map.items()[:mid + 1])
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
                current_node = current_node.key_pointer_map.get(key)
        return current_node

    # Return true if mapping exists; false otherwise
    def find(self, key, value):
        node_map = self.search(key).key_pointer_map
        if ((node_map.__contains__(key)) and (value in node_map.get(key))):
            return True
        else:
            return False
        
    #def insert_in_parent(self, n, value, ndash):



    
#testing
test_dict = SortedDict({'b': SortedList([85, 80, 75]), 'e': [2, 1]})
test_dict.update({'d': [1], 'c': [32, 30], 'm': Node(5)})
#print(test_dict)
#test_dict.popitem(index=0) #removal
print(test_dict)
#test_dict['c'] = 30 (this overrides so don't use this)
#test_dict.update({'d': 4}) this overrides too so don't use this
#print(test_dict.bisect_right('f'))

#selected_items = [(key, test_dict.get(key)) for key in test_dict.keys()[1:]]
#test_dict_2 = SortedDict(selected_items)

#test_dict_2 = SortedDict(test_dict.items()[2:]) get certain ones
print(test_dict.keys()[0])