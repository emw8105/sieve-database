# Modified version of Geeks for Geeks B+ tree

import queue as q
import math
from sortedcontainers import SortedDict
from node import Node
import sys

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
        while not current_node.leaf: # traverse to the leaf node and search the partition if it exists, else searches the key map directly
            if not current_node.partitions:
                child_index = current_node.key_pointer_map.bisect_right(key) # find the child index to traverse to
                if child_index == len(current_node.key_pointer_map):
                    current_node = current_node.last_child_node # traverse to the last child node
                else:
                    next_key = current_node.key_pointer_map.keys()[child_index]
                    current_node = current_node.key_pointer_map.get(next_key)
            else: # iterate over the partitions to find the correct child node
                for start_key, end_key, pointers in current_node.partitions:
                    if start_key <= key <= end_key: # if the key is within the partition range
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
    
    # Insert the key and pointer into the parent node
    def insert_in_parent(self, left, key, right):
        if(self.root == left):
            # if the left node is the root, create a new root node
            root_node = Node(left.order)
            root_node.key_pointer_map[key] = left
            root_node.last_child_node = right
            self.root = root_node
            left.parent = root_node
            right.parent = root_node
            return
        
        # if the left node is not the root, find its parent node
        parent_node = left.parent

        # get all child nodes of the parent node
        child_nodes = list(parent_node.key_pointer_map.values())
        child_nodes.append(parent_node.last_child_node)
        for i in range(len(child_nodes)): # iterate over the child nodes to find the left node
            if(child_nodes[i] == left):
                parent_node.key_pointer_map[key] = child_nodes[i]
                
                # if the left node is the last child node, set the right node as the last child node
                if(i == (len(child_nodes) - 1)):
                    parent_node.last_child_node = right
                else:
                    next_i_key = parent_node.key_pointer_map.keys()[i+1]
                    parent_node.key_pointer_map[next_i_key] = right
                
                # if the parent node is full, split it
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
                    
                    # if the parent node is the root, create a new root node
                    print("Parential overflow, splitting into: " + str(parent_node.key_pointer_map.keys()) + " and " + str(parent_right.key_pointer_map.keys()))
                    
                    self.insert_in_parent(parent_node, value_, parent_right)

    # Return the leftmost node in the tree, used for debugging purposes to iterate over the nodes in the tree from left to right
    def get_leftmost_node(self):
        node = self.root
        while not node.leaf:
            node = node.key_pointer_map.peekitem(0)[1]  # Get the first child node
        return node
    
    # Partition the tree into nodes by iterating over each node and creating partitions and segments within them
    def partition_tree(self):
        # start from the leftmost leaf node
        current_node = self.get_leftmost_node()

        # traverse the tree and partition each node
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

    def print_memory_usage(self):
        node = self.get_leftmost_node()
        while node is not None:
            key_map_memory = sys.getsizeof(node.key_pointer_map)
            partition_memory = sys.getsizeof(node.partitions)
            print(f"Node {node}: Key Map Memory = {key_map_memory} bytes, Partition Memory = {partition_memory} bytes")
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

    # Prints the values of all keys with their corresponding pointers in the B+ tree
    def print_tree(self, node):
        if node is None:
            return

        # print keys and pointers of the current node
        for key, pointers in node.key_pointer_map.items():
            print(f"Key: {key}, Pointers: {pointers}")

        # if the node is not a leaf, recursively print its child nodes
        if not node.leaf:
            for child_node in node.key_pointer_map.values():
                self.print_tree(child_node)

        # print the last child node if it exists
        if node.last_child_node is not None:
            self.print_tree(node.last_child_node)