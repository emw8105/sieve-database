from bp_tree import Bp_Tree

class Wikipedia_Server:
    def __init__(self, tree_order):
        self.file_wikipedia_20160701_0 = "Filtered_wikipedia_dataset.txt"
        self.tree = Bp_Tree(tree_order)


# decide on tree order here (should be 3 or more to be a proper b+ tree; )
tree_order = 5
server = Wikipedia_Server(tree_order)