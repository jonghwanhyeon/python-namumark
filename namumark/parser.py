import re

from .elements import *
from .specs import *

newline_pattern = re.compile(r'\r\n|\n|\r')


class Parser:
    def __init__(self):
        self._document = None

    def parse(self, source):
        self._document = Document()

        for line in newline_pattern.split(source):
            self._incorporate_line(line)

        return self._document

    def _incorporate_line(self, line):
        """Incorporate a given line to the current document"""

        # 1. Find last open block
        last_open_block, remaining_text = self._find_last_open_block(self._document, line)

        # 2. Try to create a new block
        tree, deepest, remaining_text = self._create_block(remaining_text)

        # 3. Incorporate the new block if it is created
        if tree:
            self._incorporate_block(tree, last_open_block)
            block_for_text = deepest
        else:
            block_for_text = last_open_block

        # 4. Incorporate the remaining text
        if remaining_text:
            self._incorporate_text(remaining_text, block_for_text)

    def _find_last_open_block(self, block, text):
        """Find the last open block that can handle a given text.
        If a block cannot handle the given text,
        the block and its descendatns will be closed, and its parent will be returned
        """

        remaining_text = text

        last_open_block = None
        for open_block in self._iterate_open_blocks(block):
            consumed, remaining_text = spec_of(open_block).consume(remaining_text)
            if not consumed:
                # This open_block and its descendatns are not suitable for a given text
                self._close_blocks(open_block)
                last_open_block = open_block.parent  # last sutiable block
                break

            last_open_block = open_block

        return last_open_block, remaining_text

    def _create_block(self, text):
        """Create a block from a given text. If the given text contains nested markers,
        this function creates all nested blocks
        """
        remaining_text = text

        tree = None
        deepest = None
        while True:
            for spec in block_specs:
                new_block, remaining_text = spec.create(remaining_text)
                if not new_block:
                    continue

                deepest = new_block
                if tree:
                    deepest.wrap(tree)
                else:
                    tree = new_block

                break
            else:  # No specs created a block
                break

        return tree, deepest, remaining_text

    def _incorporate_block(self, block, target):
        """Incorporate a given block into a given target. If the given target
        cannot contain the given block, this function searches a new target
        along its ancestors
        """
        candidate = target
        while not spec_of(candidate).can_contain(block):
            candidate = candidate.parent
        self._close_blocks(candidate.last_child)

        candidate.append(block)

    def _incorporate_text(self, text, target):
        """Incorporate a given text into a given target. If the given target
        cannot accept text, the given text will be wrapped in Paragraph
        """
        if not spec_of(target).accepts_text:
            text = Paragraph(text)

        target.append(text)

    def _iterate_open_blocks(self, block):
        """Iterate open blocks from a given block.
        Note: Only last children can be open blocks
        """
        current = block
        while current and isinstance(current, Block) and (not current.closed):
            yield current

            current = current.last_child

    def _close_blocks(self, block):
        """Close a given block and its descendatns"""
        for open_block in self._iterate_open_blocks(block):
            open_block.closed = True
