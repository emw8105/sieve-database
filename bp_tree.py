from sortedcontainers import SortedList

class Node:
    def __init__(self, order):
        self.order = order
        self.keys = SortedList()
        self.values = SortedList()
        self.leaf = True

class Bp_Tree:
    def __init__(self, order):
        self.root = Node(order)

