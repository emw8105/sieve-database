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
            


            '''
            node1.values = old_node.values[mid + 1:]
            node1.keys = old_node.keys[mid + 1:]
            node1.nextKey = old_node.nextKey
            old_node.values = old_node.values[:mid + 1]
            old_node.keys = old_node.keys[:mid + 1]
            old_node.nextKey = node1
            self.insert_in_parent(old_node, node1.values[0], node1)
            '''
    
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

    
#testing
test_dict = SortedDict()
print(test_dict.keys())
test_dict = SortedDict({'b': SortedList([85, 80, 75]), 'e': [2, 1]})
test_dict.update({'d': [1], 'c': [32, 30], 'm': Node(5)})
#print(test_dict)
#test_dict.popitem(index=0) #removal
print(test_dict)
#test_dict['c'] = 30 (this overrides so don't use this)
#test_dict.update({'d': 4}) this overrides too so don't use this
print(test_dict.bisect_right('f'))
