from .element import Element


class Block(Element):
    def __init__(self, *children):
        super().__init__(*children)

        # Blocks are normally open at first
        self.closed = False
