from namumark import Parser
from namumark.elements import *


def parse(*lines):
    return Parser().parse('\n'.join(lines))


def closed(block):
    block.closed = True
    return block


def test_heading():
    assert parse('= heading 1 =') == Document(
        Heading(1, 'heading 1'))
    assert parse('== heading 2 ==') == Document(
        Heading(2, 'heading 2'))
    assert parse('=== heading 3 ===') == Document(
        Heading(3, 'heading 3'))
    assert parse('==== heading 4 ====') == Document(
        Heading(4, 'heading 4'))
    assert parse('===== heading 5 =====') == Document(
        Heading(5, 'heading 5'))
    assert parse('====== heading 6 ======') == Document(
        Heading(6, 'heading 6'))

    # invalid syntax
    assert parse('=heading 1=') == Document(
        Paragraph('=heading 1='))


def test_quote():
    assert parse('> quote') == Document(
        Quote(
            Paragraph('quote')))

    assert parse(
        '> quote 1',
        '> quote 1',
    ) == Document(
        Quote(
            Paragraph(
                'quote 1',
                'quote 1')))

    assert parse(
        '> quote 1',
        '>> quote 2',
    ) == Document(
        Quote(
            closed(Paragraph('quote 1')),
            Quote(
                Paragraph('quote 2'))))

    assert parse(
        '> quote 1',
        '>> quote 2',
        '>>> quote 3',
    ) == Document(
        Quote(
            closed(Paragraph('quote 1')),
            Quote(
                closed(Paragraph('quote 2')),
                Quote(
                    Paragraph('quote 3')))))

    assert parse(
        '> quote 1',
        '>> quote 2',
        '>>>> quote 4',
        '> quote 1',
        '>>> quote 3',
    ) == Document(
        Quote(
            closed(Paragraph('quote 1')),
            closed(Quote(
                closed(Paragraph('quote 2')),
                closed(Quote(
                    closed(Quote(
                        closed(Paragraph('quote 4')))))))),
            closed(Paragraph('quote 1')),
            Quote(
                Quote(Paragraph('quote 3')))))


def test_unordered_list():
    assert parse(
        ' * unordered list item 1',
    ) == Document(
        UnorderedList(
            ListItem(
                Paragraph('unordered list item 1'))))

    assert parse(
        ' * unordered list item 1',
        ' * unordered list item 1',
    ) == Document(
        UnorderedList(
            closed(ListItem(
                closed(Paragraph('unordered list item 1')))),
            ListItem(
                Paragraph('unordered list item 1'))))

    assert parse(
        ' * unordered list item 1',
        '  * unordered list item 2',
    ) == Document(
        UnorderedList(
            ListItem(
                closed(Paragraph('unordered list item 1')),
                UnorderedList(
                    ListItem(
                        Paragraph('unordered list item 2'))))))

    assert parse(
        ' * unordered list item 1',
        '  * unordered list item 2',
        '   * unordered list item 3',
    ) == Document(
        UnorderedList(
            ListItem(
                closed(Paragraph('unordered list item 1')),
                UnorderedList(
                    ListItem(
                        closed(Paragraph('unordered list item 2')),
                        UnorderedList(
                            ListItem(
                                Paragraph('unordered list item 3'))))))))

    assert parse(
        ' * unordered list item 1',
        ' unordered list item 1',
        '  * unordered list item 2',
    ) == Document(
        UnorderedList(
            ListItem(
                closed(Paragraph(
                    'unordered list item 1',
                    'unordered list item 1')),
                UnorderedList(
                    ListItem(
                        Paragraph('unordered list item 2'))))))

    assert parse(
        ' * unordered list item 1',
        '  * unordered list item 2',
        '  unordered list item 2',
        '   * unordered list item 3',
    ) == Document(
        UnorderedList(
            ListItem(
                closed(Paragraph('unordered list item 1')),
                UnorderedList(
                    ListItem(
                        closed(Paragraph(
                            'unordered list item 2',
                            'unordered list item 2')),
                        UnorderedList(
                            ListItem(
                                Paragraph('unordered list item 3'))))))))

    assert parse(
        ' * unordered list item 1',
        ' unordered list item 1',
        '  * unordered list item 2',
        ' unordered list item 1',
        '   * unordered list item 3',
    ) == Document(
        UnorderedList(
            ListItem(
                closed(Paragraph(
                    'unordered list item 1',
                    'unordered list item 1')),
                closed(UnorderedList(
                    closed(ListItem(
                        closed(Paragraph('unordered list item 2')))))),
                closed(Paragraph('unordered list item 1')),
                Indentation(
                    UnorderedList(
                        ListItem(
                            Paragraph('unordered list item 3')))))))


def test_ordered_list():
    bullets = '1AaIi'

    for bullet in bullets:
        assert parse(
            ' {}. ordered list item 1'.format(bullet),
        ) == Document(
            OrderedList(
                1, bullet,
                ListItem(
                    Paragraph('ordered list item 1'))))

        assert parse(
            ' {}. ordered list item 1'.format(bullet),
            ' {}. ordered list item 1'.format(bullet),
        ) == Document(
            OrderedList(
                1, bullet,
                closed(ListItem(
                    closed(Paragraph('ordered list item 1')))),
                ListItem(
                    Paragraph('ordered list item 1'))))

        assert parse(
            ' {}.#10 ordered list item 1'.format(bullet),
            ' {}. ordered list item 1'.format(bullet),
        ) == Document(
            OrderedList(
                10, bullet,
                closed(ListItem(
                    closed(Paragraph('ordered list item 1')))),
                ListItem(
                    Paragraph('ordered list item 1'))))

        assert parse(
            ' {}. ordered list item 1'.format(bullet),
            '  {}. ordered list item 2'.format(bullet),
        ) == Document(
            OrderedList(
                1, bullet,
                ListItem(
                    closed(Paragraph('ordered list item 1')),
                    OrderedList(
                        1, bullet,
                        ListItem(
                            Paragraph('ordered list item 2'))))))

        assert parse(
            ' {}. ordered list item 1'.format(bullet),
            '  {}. ordered list item 2'.format(bullet),
            '   {}. ordered list item 3'.format(bullet),
        ) == Document(
            OrderedList(
                1, bullet,
                ListItem(
                    closed(Paragraph('ordered list item 1')),
                    OrderedList(
                        1, bullet,
                        ListItem(
                            closed(Paragraph('ordered list item 2')),
                            OrderedList(
                                1, bullet,
                                ListItem(
                                    Paragraph('ordered list item 3'))))))))

        assert parse(
            ' {}. ordered list item 1'.format(bullet),
            ' ordered list item 1',
            '  {}. ordered list item 2'.format(bullet),
        ) == Document(
            OrderedList(
                1, bullet,
                ListItem(
                    closed(Paragraph(
                        'ordered list item 1',
                        'ordered list item 1')),
                    OrderedList(
                        1, bullet,
                        ListItem(
                            Paragraph('ordered list item 2'))))))

        assert parse(
            ' {}. ordered list item 1'.format(bullet),
            '  {}. ordered list item 2'.format(bullet),
            '  ordered list item 2',
            '   {}. ordered list item 3'.format(bullet),
        ) == Document(
            OrderedList(
                1, bullet,
                ListItem(
                    closed(Paragraph('ordered list item 1')),
                    OrderedList(
                        1, bullet,
                        ListItem(
                            closed(Paragraph(
                                'ordered list item 2',
                                'ordered list item 2')),
                            OrderedList(
                                1, bullet,
                                ListItem(
                                    Paragraph('ordered list item 3'))))))))

        assert parse(
            ' {}. ordered list item 1'.format(bullet),
            ' ordered list item 1',
            '  {}. ordered list item 2'.format(bullet),
            ' ordered list item 1',
            '   {}. ordered list item 3'.format(bullet),
        ) == Document(
            OrderedList(
                1, bullet,
                ListItem(
                    closed(Paragraph(
                        'ordered list item 1',
                        'ordered list item 1')),
                    closed(OrderedList(
                        1, bullet,
                        closed(ListItem(
                            closed(Paragraph('ordered list item 2')))))),
                    closed(Paragraph('ordered list item 1')),
                    Indentation(
                        OrderedList(
                            1, bullet,
                            ListItem(
                                Paragraph('ordered list item 3')))))))


def test_indentation():
    assert parse(
        'indentation 0',
        ' indentation 1',
    ) == Document(
        closed(Paragraph('indentation 0')),
        Indentation(
            Paragraph('indentation 1')))

    assert parse(
        'indentation 0',
        ' indentation 1',
        '  indentation 2',
    ) == Document(
        closed(Paragraph('indentation 0')),
        Indentation(
            closed(Paragraph('indentation 1')),
            Indentation(
                Paragraph('indentation 2'))))

    assert parse(
        'indentation 0',
        ' indentation 1',
        '  indentation 2',
        ' indentation 1',
    ) == Document(
        closed(Paragraph('indentation 0')),
        Indentation(
            closed(Paragraph('indentation 1')),
            closed(Indentation(
                closed(Paragraph('indentation 2')))),
            Paragraph('indentation 1')))

    assert parse(
        'indentation 0',
        ' indentation 1',
        '  indentation 2',
        'indentation 0',
        '  indentation 2',
    ) == Document(
        closed(Paragraph('indentation 0')),
        closed(Indentation(
            closed(Paragraph('indentation 1')),
            closed(Indentation(
                closed(Paragraph('indentation 2')))))),
        closed(Paragraph('indentation 0')),
        Indentation(
            Indentation(
                Paragraph('indentation 2'))))


def test_thematic_break():
    assert parse('----') == Document(
        ThematicBreak())

    assert parse('-----') == Document(
        ThematicBreak())

    assert parse('------') == Document(
        ThematicBreak())

    assert parse('-------') == Document(
        ThematicBreak())

    assert parse('--------') == Document(
        ThematicBreak())

    assert parse('---------') == Document(
        ThematicBreak())

    # invalid syntax
    assert parse('---') == Document(
        Paragraph('---'))
