from .element import Element


class Block(Element):
    def __init__(self, *children):
        super().__init__(*children)

        # Blocks are normally open at first
        self.closed = False


class Document(Block):
    pass


class Heading(Block):
    def __init__(self, level, *children):
        super().__init__(*children)

        self.level = level
        self.closed = True


class Quote(Block):
    pass


class Paragraph(Block):
    pass


class List(Block):
    pass


class UnorderedList(List):
    pass


class OrderedList(List):
    def __init__(self, start, bullet, *children):
        super().__init__(*children)

        self.start = start
        self.bullet = bullet


class ListItem(Block):
    pass


class Indentation(Block):
    pass


class ThematicBreak(Block):
    def __init__(self):
        super().__init__()

        self.closed = True
