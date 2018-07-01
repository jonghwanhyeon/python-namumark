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


class Element(Node):
    def __init__(self, *children):
        super().__init__()
        self.children = list(children)

    def dump(self, indent=2):
        def do_dump(element, depth=0):
            yield '{indent}{element}'.format(
                indent=' ' * (indent * depth),
                element=repr(element)
            )

            if isinstance(element, Element):
                for child in element:
                    yield from do_dump(child, depth + 1)

        return '\n'.join(do_dump(self))

    def __repr__(self):
        keys = vars(self).keys()
        keys -= {'parent', 'children'}
        keys = filter(lambda key: not key.startswith('_'), keys)

        mappings = [
            '{}={}'.format(key, repr(getattr(self, key)))
            for key in sorted(keys)
        ]

        return '{name}({mappings})'.format(
            name=self.__class__.__name__,
            mappings=', '.join(mappings)
        )
