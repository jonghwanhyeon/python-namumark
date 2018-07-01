class Element:
    def __init__(self, *children):
        self.parent = None
        self.children = []

        for child in children:
            self.append(child)

    def append(self, element):
        """Append a given element as a last child of this element"""
        element.parent = self
        self.children.append(element)

        return self

    def prepend(self, element):
        """Prepend a given element as a first child of this element"""
        element.parent = self
        self.children.insert(0, element)

        return self

    def wrap(self, element):
        """Wrap this element in a given element"""
        deepest = element
        while deepest.first_child:
            deepest = deepest.first_child
        deepest.append(self)

        return element

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

    @property
    def first_child(self):
        return self.children[0] if self.children else None

    @property
    def last_child(self):
        return self.children[-1] if self.children else None

    def __iter__(self):
        return iter(self.children)

    def __repr__(self):
        identifier = '{:04x}'.format(id(self))

        keys = vars(self).keys()
        keys -= {'parent', 'children'}
        keys = filter(lambda key: not key.startswith('_'), keys)
        mappings = [
            '{}={}'.format(key, repr(getattr(self, key)))
            for key in sorted(keys)
        ]

        return '{name}#{identifier}({mappings})'.format(
            name=self.__class__.__name__,
            identifier=identifier[-4:],
            mappings=', '.join(mappings)
        )
