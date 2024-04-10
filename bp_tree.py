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
        print("I am child: " + str(self.key_pointer_map.keys()))
                

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

        print("groot")
        print(self.root.key_pointer_map.keys())

        while(not current_node.leaf):
            child_index = current_node.key_pointer_map.bisect_right(key)
            if(child_index == len(current_node.key_pointer_map)):
                current_node = current_node.last_child_node
            else:

                print("key: " + str(key))

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
            
            print("insert in parent when root == left: left is " + str(left.key_pointer_map.keys()) + ", key is " + str(key) + ", right is " + str(right.key_pointer_map.keys()))
            
            root_node = Node(left.order)
            root_node.key_pointer_map[key] = left
            root_node.last_child_node = right
            self.root = root_node
            left.parent = root_node
            right.parent = root_node

            print("my new root node is: " + str(self.root.key_pointer_map.keys()))

            return
        
        parent_node = left.parent

        print("i am the parent: " + str(parent_node.key_pointer_map.keys()))
        print("i am key: " + str(key))

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

                
                print("HEYYYY i am a new parent: " + str(parent_node.key_pointer_map.keys()))
                
                
                if(len(parent_node.key_pointer_map.keys()) + 1 > parent_node.order):
                    parent_right = Node(parent_node.order)
                    parent_right.parent = parent_node.parent
                    mid = int(math.ceil(parent_node.order / 2)) - 1
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
                    
                    print("parential overflow")
                    print("i split into: " + str(parent_node.key_pointer_map.keys()) + " and " + str(parent_right.key_pointer_map.keys()))
                    
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
    
#testing

#test_dict = SortedDict({'b': SortedList([85, 80, 75]), 'e': [2, 1]})
#test_dict.update({'d': [1], 'c': [32, 30], 'm': Node(5)})
#print(test_dict)

#test_dict.popitem(index=0) #removal

#test_dict['c'] = 30 
#print(test_dict)
#(this overrides so don't use this)
#test_dict.update({'d': 4}) this overrides too so don't use this
#print(test_dict.bisect_right('f'))

#selected_items = [(key, test_dict.get(key)) for key in test_dict.keys()[1:]]
#test_dict_2 = SortedDict(selected_items)

#test_dict_2 = SortedDict(test_dict.items()[2:]) get certain ones
#print(test_dict.keys()[0])

#print(test_dict.popitem())

# more testing

def print_tree(tree):
    lst = [tree.root]
    level = [0]

    while(len(lst) != 0):
        x = lst.pop(0)
        lev = level.pop(0)

        print("THIS IS LEVEL: " + str(lev))
        print(x.key_pointer_map.keys())

        if(not x.leaf):
            children = list(x.key_pointer_map.values())
            children.append(x.last_child_node)

            for i, item in enumerate(children):
                lst.append(item)
                level.append(lev+1)


record_len = 3
bplustree = Bp_Tree(record_len)
bplustree.insert(6, 0)
bplustree.insert(16, 5)
bplustree.insert(26, 0)
bplustree.insert(36, 3)
bplustree.insert(46, 0)

print("printing tree: ")
print_tree(bplustree)

leaf_array = bplustree.leaf_array()
print("this is leaf array: " + str(leaf_array))

#if(bplustree.find(6, 34)):
    #print("Found")
#else:
    #print("Not found")