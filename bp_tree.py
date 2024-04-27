# Modified version of Geeks for Geeks B+ tree

import queue as q
import math
from sortedcontainers import SortedDict
from node import Node

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



    ### PRINT METHODS FOR DEBUGGING ###
    def print_all_partitions(self):
        node = self.get_leftmost_node()
        i = 0
        while node is not None:
            print(f"Node {i}:")
            for start_key, end_key, pointer_list in node.partitions:
                print(f"  Partition: start_key={start_key}, end_key={end_key}, pointer_list={pointer_list}")
            node = node.next_leaf_node
            i += 1
    
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