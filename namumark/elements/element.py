class Node:
    def __init__(self):
        self.parent = None
        self.children = []

    def append(self, node):
        """Append a given node as a last child of this node"""
        node.parent = self
        self.children.append(node)

        return self

    def prepend(self, node):
        """Prepend a given node as a first child of this node"""
        node.parent = self
        self.children.insert(0, node)

        return self

    def wrap(self, node):
        """Wrap a given node around this node"""
        deepest = node
        while deepest.first_child:
            deepest = deepest.first_child
        deepest.append(self)

        return node

    @property
    def first_child(self):
        return self.children[0] if self.children else None

    @property
    def last_child(self):
        return self.children[-1] if self.children else None

    def __iter__(self):
        return iter(self.children)
