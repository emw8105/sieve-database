# Modified version of Geeks for Geeks B+ tree

from sortedcontainers import SortedDict, SortedList

class Node:
    def __init__(self, order):
        self.order = order
        self.key_value_map = SortedDict() # key=int; value=SortedList()
        self.leaf = False
    
    def insert_at_leaf(self, key, value):
        if(key in self.key_value_map.keys()): # Key exists 
            if(value not in self.key_value_map.get(key)): # Value not in list
                self.key_value_map.get(key).add(value) 
        else: # Key does not exist 
            self.key_value_map[key] = SortedList([value])
                

class Bp_Tree:
    def __init__(self, order):
        self.root = Node(order)
        self.root.leaf = True

    
#testing
test_dict = SortedDict()
print(test_dict.keys())
test_dict = SortedDict({'b': SortedList([85, 80, 75]), 'e': [2, 1]})
test_dict.update({'d': [1], 'c': [32, 30]})
#print(test_dict)
#test_dict.popitem(index=0) #removal
print(test_dict)
#test_dict['c'] = 30 (this overrides so don't use this)
#test_dict.update({'d': 4}) this overrides too so don't use this

