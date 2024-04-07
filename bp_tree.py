from sortedcontainers import SortedList

class Bp_Tree:
    def __init__(self, order):
        self.order = order
        self.leaves = SortedList()
        self.pointers = {}

