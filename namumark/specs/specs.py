import re

from collections import namedtuple

from . import spec_for
from ..elements import *


@spec_for(Block)
class BlockSpec:
    accepts_text = False

    @classmethod
    def create(cls, text):
        """Try to create an element from a given text. Normally, this function
        looks only markers and uses only those markers from the given text.

        If success, returns (Created element, remaining text)
        Otherwise, returns (None, the given text)
        """
        return (None, text)

    @classmethod
    def consume(cls, text, context):
        """Try to consume markers from a given text. This function checks
        whether the given text is sutiable for this element or not.

        If success, returns (True, remaining text)
        Otherwise, returns (False, the given text)
        """
        return (False, text)

    @staticmethod
    def can_contain(element):
        """Returns whether the element of this specification
        can contain a given element?
        """
        return False


@spec_for(Document)
class DocumentSpec(BlockSpec):
    accepts_text = False

    @classmethod
    def consume(cls, text, context):
        return (True, text)

    @staticmethod
    def can_contain(element):
        return True


@spec_for(Heading)
class HeadingSpec(BlockSpec):
    '''
    = heading 1 =
    == heading 2 ==
    === heading 3 ===
    ==== heading 4 ====
    ===== heading 5 =====
    ====== heading 6 ======
    '''
    syntax = re.compile(r'''
        ^
            (\={1,6})  # marker
            [ ]+  # required whitespace
            (.*)  # text
            [ ]+  # required whitespace
            \1
        $
    ''', re.VERBOSE)

    accepts_text = True

    @classmethod
    def create(cls, text):
        match = cls.syntax.search(text)
        if not match:
            return (None, text)

        level = len(match.group(1))
        return (Heading(level=level), match.group(2))

    @staticmethod
    def can_contain(element):
        return False


@spec_for(Quote)
class QuoteSpec(BlockSpec):
    '''
    > text 1
    > text 2
    '''
    syntax = re.compile(r'''
        ^
            \>  # marker
            [ ]*  # optional whitespace
            (.*)  # text
        $
    ''', re.VERBOSE)

    accepts_text = False

    @classmethod
    def create(cls, text):
        consumed, remaining_text = cls.consume(text, None)
        if not consumed:
            return (None, text)

        return (Quote(), remaining_text)

    @classmethod
    def consume(cls, text, context):
        match = cls.syntax.search(text)
        if not match:
            return (False, text)

        return (True, match.group(1))

    @staticmethod
    def can_contain(element):
        return True


@spec_for(UnorderedList)
class UnorderedListSpec(BlockSpec):
    '''
     * text 1
     * text 2
    '''
    syntax_for_create = re.compile(r'''
        ^
            [ ]  # required whitespace
            (
                \*  # marker
                [ ]?  # optional whitespace
                .*  # text
            )
        $
    ''', re.VERBOSE)

    syntax_for_consume = re.compile(r'''
        ^
            [ ]  # required whitespace
            (
                (?:  # a new unordered list item
                    \*  # marker
                    [ ]?  # optional whitespace
                    .*  # text
                )
                |
                (?:  # line continuations
                    (?!\*)  # no unordered list marker
                    (?![1AaIi]\.)  # no ordered list marker
                    .*  # text
                )
            )
        $
    ''', re.VERBOSE)

    accepts_text = False

    @classmethod
    def create(cls, text):
        # ' * text 1' -> '* text 1'
        match = cls.syntax_for_create.search(text)
        if not match:
            return (None, text)

        return (UnorderedList(), match.group(1))

    @classmethod
    def consume(cls, text, context):
        # ' * text 1' -> '* text 1'
        # ' text 1' -> 'text 1'
        match = cls.syntax_for_consume.search(text)
        if not match:
            return (False, text)

        return (True, match.group(1))

    @staticmethod
    def can_contain(element):
        return True


@spec_for(OrderedList)
class OrderedListSpec(BlockSpec):
    '''
     1. text 1
     A. text 2
     a. text 3
     I. text 4
     i. text 5

     I.#42 text 6
     I. text 7
    '''
    syntax_for_create = re.compile(r'''
        ^
            [ ]  # required whitespace
            (?P<marker>
                (?P<bullet>[1AaIi])  # marker, bullet
                \.  # marker
            )
            (?:
                \#  # marker
                (?P<start>\d+)  # marker, start
            )?
            (?P<text>
                [ ]?  # optional whitespace
                .*  # text
            )
        $
    ''', re.VERBOSE)

    syntax_for_consume = re.compile(r'''
        ^
            [ ]  # required whitespace
            (
                (?:  # a new unordered list item
                    (?P<bullet>[1AaIi])  # marker, bullet
                    \.  # marker
                    (?!\#\d+)  # no start marker
                    [ ]?  # optional whitespace
                    .*  # text
                )
                |
                (?:  # line continuations
                    (?!\*)  # no unordered list marker
                    (?![1AaIi]\.)  # no ordered list marker
                    .*  # text
                )
            )
        $
    ''', re.VERBOSE)

    accepts_text = False

    @classmethod
    def create(cls, text):
        # ' 1. text 1' -> '1. text 1'
        # ' 1.#42 text 1' -> '1. text 1'
        match = cls.syntax_for_create.search(text)
        if not match:
            return (None, text)

        return (
            OrderedList(bullet=match.group('bullet'),
                        start=int(match.group('start') or 1)),
            match.group('marker') + match.group('text'))

    @classmethod
    def consume(cls, text, context):
        # ' text 1' -> 'text 1'
        # ' 1. text 1' -> '1. text 1'
        match = cls.syntax_for_consume.search(text)
        if not match:
            return (False, text)

        bullet = match.group('bullet')
        if bullet and (bullet != context.bullet):
            return (False, text)

        return (True, match.group(1))

    @staticmethod
    def can_contain(element):
        return True


@spec_for(ListItem)
class ListItemSpec(BlockSpec):
    '''
    * text 1
    1. text 2
    A. text 3
    a. text 4
    I. text 5
    i. text 6

    * text 1
    text 2

    1. text 1
    text 2
    '''
    syntax = re.compile(r'''
        ^
            (?:
                \*  # unordered list marker
                |
                [1AaIi]\.  # ordered list marker
            )
            [ ]?  # optional whitespace
            (.*)  # text
        $
    ''', re.VERBOSE)

    accepts_text = False

    @classmethod
    def create(cls, text):
        match = cls.syntax.search(text)
        if not match:
            return (False, text)

        return (ListItem(), match.group(1))

    @classmethod
    def consume(cls, text, context):
        match = cls.syntax.search(text)
        if match:
            # Case 1: a new list item
            return (False, text)

        # Case 2: line continuations
        return (True, text)

    @staticmethod
    def can_contain(element):
        return True


@spec_for(Paragraph)
class ParagraphSpec(BlockSpec):
    accepts_text = True

    @classmethod
    def consume(cls, text, context):
        return (True, text)

    @staticmethod
    def can_contain(element):
        return False


@spec_for(Indentation)
class IndentationSpec(BlockSpec):
    '''
     text 1
     text 2
    '''
    syntax = re.compile(r'''
        ^
            [ ]  # marker
            (.*)  # text
        $
    ''', re.VERBOSE)

    accepts_text = False

    @classmethod
    def create(cls, text):
        consumed, remaining_text = cls.consume(text, None)
        if not consumed:
            return (None, text)

        return (Indentation(), remaining_text)

    @classmethod
    def consume(cls, text, context):
        match = cls.syntax.search(text)
        if not match:
            return (False, text)

        return (True, match.group(1))

    @staticmethod
    def can_contain(element):
        return True


@spec_for(ThematicBreak)
class ThematicBreakSpec(BlockSpec):
    '''
    ----
    -----
    ------
    -------
    --------
    ---------
    '''
    syntax = re.compile(r'''
        ^
            \-{4,9}  # marker
        $
    ''', re.VERBOSE)

    accepts_text = False

    @classmethod
    def create(cls, text):
        match = cls.syntax.search(text)
        if not match:
            return (None, text)

        return (ThematicBreak(), '')

    @staticmethod
    def can_contain(element):
        return False
