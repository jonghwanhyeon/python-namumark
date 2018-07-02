from .element import Element


class Block(Element):
    def __init__(self, *children):
        super().__init__(*children)

        # Blocks are normally open at first
        self.closed = False


class Document(Block):
    pass


class Heading(Block):
    def __init__(self, level):
        super().__init__()

        self.level = level
        self.closed = True


class Quote(Block):
    pass


class Paragraph(Block):
    pass


class Indentation(Block):
    pass


class ThematicBreak(Block):
    def __init__(self):
        super().__init__()

        self.closed = True
