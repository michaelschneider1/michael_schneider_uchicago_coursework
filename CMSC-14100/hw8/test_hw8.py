"""
CMSC 14100
Winter 2025

Test code for Homework #8
"""

import os
import sys
import traceback
import pytest
import copy
import helpers

# Handle the fact that the test code may not
# be in the same directory as the solution code
sys.path.insert(0, os.getcwd())

# Don't complain about the position of the import
# pylint: disable=wrong-import-position
import hw8, grammars
import random
from grammars import Variable, Terminal

MODULE = "hw8"


ident = lambda sigma: dict(list((x, x) for x in sigma) + [('','')])
anti = lambda sigma: dict(list(zip(list(sigma), reversed(list(sigma)))) + [('','')])

@pytest.mark.parametrize("seq, transform, expected",
                         [(list('a'), ident('ab'), True),
                          (list('babbbbab'), ident('ab'), True),
                          (list('ab'), anti('ab'), True),
                          (list('babbbbab'), anti('ab'), False),
                          (list('baaabababbba'), anti('ab'), True),
                          (list(''), anti('ACGT'), True),
                          (list('AT'), anti('ACGT'), True),
                          (list('TATTTTAT'), anti('ACGT'), False),
                          (list('TCACGCGCGTGA'), anti('ACGT'), True),
                          ])
def test_is_pal(seq, transform, expected):
    """  
    Test code for Exercise 1: is_pal
    """
    steps = [
        f"actual = hw8.is_pal('{seq}', {transform})"
        ]
    recreate_msg = helpers.gen_recreate_commands(MODULE, steps)

    try:
        actual = hw8.is_pal(seq, transform)
    except Exception as e:
        helpers.fail_and_augment_recreate_unexpected_exception(recreate_msg, e)

    err_msg = helpers.check_result(actual, expected)
    if err_msg is not None:
        pytest.fail(err_msg + recreate_msg)


@pytest.mark.parametrize("tree, expected",
                         [(Terminal(''), 0),
                          (Terminal('a'), 0),
                          (Terminal('if'), 0),
                          (Variable('S', [Terminal('a'), Variable('S', [Terminal('')]), Terminal('b')]), 2),
                          (grammars.d2, 1),
                          (grammars.d1, 3),
                          (grammars.at1, 11),
                          (grammars.py1, 48),
                          (grammars.e3, 40),
                          (grammars.c3, 17)
                          ])
def test_derivation_length(tree, expected):
    """
    Test code for Exercise 2: derivation_length
    """
    steps = [
            f'from grammars import Variable, Terminal',
            f'tree = {repr(tree)}',
            f"actual = hw8.derivation_length(tree)"
        ]
    recreate_msg = helpers.gen_recreate_commands(MODULE, steps)

    try:
        actual = hw8.derivation_length(tree)
    except Exception as e:
        helpers.fail_and_augment_recreate_unexpected_exception(recreate_msg, e)

    err_msg = helpers.check_result(actual, expected)
    if err_msg is not None:
        pytest.fail(err_msg + recreate_msg)


@pytest.mark.parametrize("tree1, tree2, expected",
                         [(Terminal(''), Terminal(''), True),
                          (Terminal('a'), Terminal(''), False),
                          (Terminal('a'), Variable('a', []), False),
                          (Variable('a', []), Terminal('a'), False),
                          (Variable('S', []), Variable('S', []), True),
                          (Variable('S', [Terminal('a')]), Variable('S', [Terminal('a')]), True),
                          (Variable('S', [Terminal('a')]), Variable('S', [Terminal('b')]), False),
                          (grammars.pal1, grammars.pal2, False),
                          (grammars.pal1, copy.deepcopy(grammars.pal1), True),
                          (grammars.c2, copy.deepcopy(grammars.c2), True),
                          ])
def test_is_equal(tree1, tree2, expected):
    """
    Test code for Exercise 3: is_equal
    """
    steps = [
            f'from grammars import Variable, Terminal',
            f'tree1 = {repr(tree1)}',
            f'tree2 = {repr(tree2)}',
            f"actual = hw8.is_equal(tree1, tree2)"
        ]
    recreate_msg = helpers.gen_recreate_commands(MODULE, steps)

    try:
        actual = hw8.is_equal(tree1, tree2)
    except Exception as e:
        helpers.fail_and_augment_recreate_unexpected_exception(recreate_msg, e)

    err_msg = helpers.check_result(actual, expected)
    if err_msg is not None:
        pytest.fail(err_msg + recreate_msg)


@pytest.mark.parametrize("tree, expected",
                         [(Terminal(''),  ''),
                          (Terminal('a'), 'a'),
                          (Variable('S', [Terminal('a'), Terminal('b')]), 'ab'),
                          (Variable('S', [Terminal('a'), Variable('S', [])]), 'a«S»'),
                          (grammars.d1, '{[]}{}'),
                          (grammars.d3, '[[{}]([[]][()]([{{}}{}]{[{[]}{}][()][]}())(())[])[({})[]]{}]()'),
                          (grammars.e3,'218×3207×2+(6×(2×99+9))×42'),
                          (grammars.e2,'(0046×435×0×(4×68×(«F»+«N»)+(3)+((«E»+«T»)×«N»83))×9+1+(22×«N»316508+61×((«E»)×(«T»)×(«F»)×6×8)+((«N»×8×9)))+81×(211212+(«N»3×«N»04×(«T»+«F»+«T»×«F»×«N»))×3234+(57+«T»×«F»×«N»×1×91×(«T»×«F»+«T»×«F»×«N»)×«N»3168)×(«F»×«N»+«F»×«N»×0+19+194+3×(«E»+«T»+«T»×«F»+«N»+«F»×(«E»)×(«T»))+«N»4×(«T»+«F»)×«N»949×(8)×51)+((«F»)×1×((«E»)+1)×89)×(9))+((«N»×6×«N»01+«N»809+(«E»+«T»+«T»×«F»+(«E»)+«N»5)+((«T»)×6)+((«T»×«F»)×(«F»+«N»))+4)))×11'),
                          (grammars.reg1, '(ja)y**'),
                          (grammars.reg3, 'v**a*e(((«X»+«F»)**)*)*')
                          ])
def test_evaluate(tree, expected):
    """
    Test code for Exercise 4: evaluate
    """
    steps = [
            f'from grammars import Variable, Terminal',
            f'tree = {repr(tree)}',
            f"actual = hw8.evaluate(tree)"
        ]
    recreate_msg = helpers.gen_recreate_commands(MODULE, steps)

    try:
        actual = hw8.evaluate(tree)
    except Exception as e:
        helpers.fail_and_augment_recreate_unexpected_exception(recreate_msg, e)

    err_msg = helpers.check_result(actual, expected)
    if err_msg is not None:
        pytest.fail(err_msg + recreate_msg)

@pytest.mark.parametrize("tree, separator, expected",
                         [
                          (Variable('S', [Terminal('a'), Terminal('b')]), ',', 'a,b'),
                          (Variable('S', [Terminal('a'), Variable('S', [])]), ' ', 'a «S»'),
                          (grammars.d2, 'true', '(true)'),
                          (grammars.reg1, 'regular', '(regularjregulararegular)regularyregular*regular*'),
                          (grammars.py1, ' ', 'if ( False and True ) : if not True or True and n or e and e : return ( e ) or j and m and True and d'),
                          (grammars.c1, ' ','if ( ~ ~ ~ ~ ~ true ^ l ^ ( ~ true & true ) ) { return ( false & false ) & w & true & false & ( u & true ^ false & true & true ) ^ true ; }'),
                          (grammars.at1, ' ','the mat sat the oat'),
                          ])
def test_evaluate_sep(tree, separator, expected):
    """
    Test code for Exercise 4: evaluate with separator
    """
    steps = [
            f'from grammars import Variable, Terminal',
            f'tree = {repr(tree)}',
            f"actual = hw8.evaluate(tree, '{separator}')"
        ]
    recreate_msg = helpers.gen_recreate_commands(MODULE, steps)

    try:
        actual = hw8.evaluate(tree, separator)
    except Exception as e:
        helpers.fail_and_augment_recreate_unexpected_exception(recreate_msg, e)

    err_msg = helpers.check_result(actual, expected)
    if err_msg is not None:
        pytest.fail(err_msg + recreate_msg)


tags = {'': '', '(': '<div>', '[': '<span>', '{': '<p>', ')': '</div>', ']': '</span>', '}': '</p>'}
@pytest.mark.parametrize("tree, ph, expected",
                         [(Terminal(''), ident(''), Terminal('')),
                          (Terminal('a'), ident('ab'), Terminal('a')),
                          (Terminal('a'), anti('ab'), Terminal('b')),
                          (Variable('S', [Terminal('a')]), anti('ab'), Variable('S', [Terminal('b')])),
                          (grammars.pal1, {'': '', 'a': 'a', 'b': 't'}, grammars.pal2),
                          (grammars.at1, 
                           ({x: x for x in grammars.AT.terminals} | 
                            {x: 'at' for x in grammars.AT.terminals if x.endswith('at')} |
                            {'': ''}), 
                           Variable('S', [Variable('NP', [Variable('Det', [Terminal('the')]), Variable('Nominal', [Variable('Noun', [Terminal('at')])])]), Variable('VP', [Variable('Verb', [Terminal('at')]), Variable('NP', [Variable('Det', [Terminal('the')]), Variable('Nominal', [Variable('Noun', [Terminal('at')])])])])])),
                          (grammars.d1, tags, Variable('S', [Terminal('<p>'), Variable('S', [Terminal('<span>'), Terminal('</span>')]), Terminal('</p>'), Variable('S', [Terminal('<p>'), Terminal('</p>')])])),
                          (grammars.d1, {x: '' for x in grammars.DYCK3.terminals} | {'':""}, Variable('S', [Terminal(''), Variable('S', [Terminal(''), Terminal('')]), Terminal(''), Variable('S', [Terminal(''), Terminal('')])])),
                          (grammars.d3, tags, Variable('S', [Terminal('<span>'), Variable('S', [Terminal('<span>'), Variable('S', [Terminal('<p>'), Terminal('</p>')]), Terminal('</span>'), Variable('S', [Terminal('<div>'), Variable('S', [Terminal('<span>'), Variable('S', [Terminal('<span>'), Terminal('</span>')]), Terminal('</span>'), Variable('S', [Terminal('<span>'), Variable('S', [Terminal('<div>'), Terminal('</div>')]), Terminal('</span>'), Variable('S', [Terminal('<div>'), Variable('S', [Terminal('<span>'), Variable('S', [Terminal('<p>'), Variable('S', [Terminal('<p>'), Terminal('</p>')]), Terminal('</p>'), Variable('S', [Terminal('<p>'), Terminal('</p>')])]), Terminal('</span>'), Variable('S', [Terminal('<p>'), Variable('S', [Terminal('<span>'), Variable('S', [Terminal('<p>'), Variable('S', [Terminal('<span>'), Terminal('</span>')]), Terminal('</p>'), Variable('S', [Terminal('<p>'), Terminal('</p>')])]), Terminal('</span>'), Variable('S', [Terminal('<span>'), Variable('S', [Terminal('<div>'), Terminal('</div>')]), Terminal('</span>'), Variable('S', [Terminal('<span>'), Terminal('</span>')])])]), Terminal('</p>'), Variable('S', [Terminal('<div>'), Terminal('</div>')])])]), Terminal('</div>'), Variable('S', [Terminal('<div>'), Variable('S', [Terminal('<div>'), Terminal('</div>')]), Terminal('</div>'), Variable('S', [Terminal('<span>'), Terminal('</span>')])])])])]), Terminal('</div>'), Variable('S', [Terminal('<span>'), Variable('S', [Terminal('<div>'), Variable('S', [Terminal('<p>'), Terminal('</p>')]), Terminal('</div>'), Variable('S', [Terminal('<span>'), Terminal('</span>')])]), Terminal('</span>'), Variable('S', [Terminal('<p>'), Terminal('</p>')])])])]), Terminal('</span>'), Variable('S', [Terminal('<div>'), Terminal('</div>')])])),
                         (grammars.e3, {x: x for x in grammars.ARITHMETIC.terminals} | {'+': '–', '×': '÷', '': ''}, Variable('E', [Variable('E', [Variable('T', [Variable('T', [Variable('T', [Variable('F', [Variable('N', [Variable('N', [Variable('N', [Terminal('2')]), Terminal('1')]), Terminal('8')])])]), Terminal('÷'), Variable('F', [Variable('N', [Variable('N', [Variable('N', [Variable('N', [Terminal('3')]), Terminal('2')]), Terminal('0')]), Terminal('7')])])]), Terminal('÷'), Variable('F', [Variable('N', [Terminal('2')])])])]), Terminal('–'), Variable('T', [Variable('T', [Variable('F', [Terminal('('), Variable('E', [Variable('T', [Variable('T', [Variable('F', [Variable('N', [Terminal('6')])])]), Terminal('÷'), Variable('F', [Terminal('('), Variable('E', [Variable('E', [Variable('T', [Variable('T', [Variable('F', [Variable('N', [Terminal('2')])])]), Terminal('÷'), Variable('F', [Variable('N', [Variable('N', [Terminal('9')]), Terminal('9')])])])]), Terminal('–'), Variable('T', [Variable('F', [Variable('N', [Terminal('9')])])])]), Terminal(')')])])]), Terminal(')')])]), Terminal('÷'), Variable('F', [Variable('N', [Variable('N', [Terminal('4')]), Terminal('2')])])])])),
                          ])
                         
def test_morph(tree, ph, expected):
    """
    Test code for Exercise 5: morph
    """
    steps = [
            f'from grammars import Variable, Terminal',
            f'tree = {repr(tree)}',
            f'morphism = {ph}',
            f"actual = hw8.morph(tree, morphism)"
        ]
    recreate_msg = helpers.gen_recreate_commands(MODULE, steps)

    tree_copy = copy.deepcopy(tree) # make copy of tree to check that it wasn't modified

    try:
        actual = hw8.morph(tree, ph)
    except Exception as e:
        helpers.fail_and_augment_recreate_unexpected_exception(recreate_msg, e)

    err_msg = helpers.check_result(repr(actual), repr(expected))
    if err_msg is not None:
        pytest.fail(err_msg + recreate_msg)

    err_msg = helpers.check_list_unmodified('tree', repr(tree), repr(tree_copy))
    if err_msg is not None:
        pytest.fail(err_msg + recreate_msg)


@pytest.mark.parametrize("tree, expected",
                         [(Terminal(''), Terminal('')),
                          (Terminal('a'), Terminal('a')),
                          (Variable('S', [Terminal('a')]), Variable('S', [Terminal('a')])),
                          (Variable('S', [Terminal('a'), Terminal('b')]), Variable('S', [Terminal('b'), Terminal('a')])),
                          (Variable('S', [Terminal('['), Terminal(']')]), Variable('S', [Terminal(']'), Terminal('[')])),
                          (grammars.pal2, grammars.pal2),
                          (grammars.d1, Variable('S', [Variable('S', [Terminal('}'), Terminal('{')]), Terminal('}'), Variable('S', [Terminal(']'), Terminal('[')]), Terminal('{')])),
                          (grammars.d3, Variable('S', [Variable('S', [Terminal(')'), Terminal('(')]), Terminal(']'), Variable('S', [Variable('S', [Variable('S', [Variable('S', [Terminal('}'), Terminal('{')]), Terminal(']'), Variable('S', [Variable('S', [Terminal(']'), Terminal('[')]), Terminal(')'), Variable('S', [Terminal('}'), Terminal('{')]), Terminal('(')]), Terminal('[')]), Terminal(')'), Variable('S', [Variable('S', [Variable('S', [Variable('S', [Variable('S', [Terminal(']'), Terminal('[')]), Terminal(')'), Variable('S', [Terminal(')'), Terminal('(')]), Terminal('(')]), Terminal(')'), Variable('S', [Variable('S', [Variable('S', [Terminal(')'), Terminal('(')]), Terminal('}'), Variable('S', [Variable('S', [Variable('S', [Terminal(']'), Terminal('[')]), Terminal(']'), Variable('S', [Terminal(')'), Terminal('(')]), Terminal('[')]), Terminal(']'), Variable('S', [Variable('S', [Terminal('}'), Terminal('{')]), Terminal('}'), Variable('S', [Terminal(']'), Terminal('[')]), Terminal('{')]), Terminal('[')]), Terminal('{')]), Terminal(']'), Variable('S', [Variable('S', [Terminal('}'), Terminal('{')]), Terminal('}'), Variable('S', [Terminal('}'), Terminal('{')]), Terminal('{')]), Terminal('[')]), Terminal('(')]), Terminal(']'), Variable('S', [Terminal(')'), Terminal('(')]), Terminal('[')]), Terminal(']'), Variable('S', [Terminal(']'), Terminal('[')]), Terminal('[')]), Terminal('(')]), Terminal(']'), Variable('S', [Terminal('}'), Terminal('{')]), Terminal('[')]), Terminal('[')])),
                          (grammars.at1, Variable('S', [Variable('VP', [Variable('NP', [Variable('Nominal', [Variable('Noun', [Terminal('oat')])]), Variable('Det', [Terminal('the')])]), Variable('Verb', [Terminal('sat')])]), Variable('NP', [Variable('Nominal', [Variable('Noun', [Terminal('mat')])]), Variable('Det', [Terminal('the')])])])),
                          (grammars.py2, Variable('for_loop', [Variable('statement', [Variable('expr', [Variable('term', [Variable('atom', [Variable('NUMBER', [Terminal('2')])]), Terminal('*'), Variable('term', [Variable('atom', [Terminal(')'), Variable('expr', [Variable('term', [Variable('atom', [Variable('NUMBER', [Terminal('6')])])])]), Terminal('(')])])])]), Terminal('return')]), Terminal(':'), Variable('NAME', [Terminal('s')]), Terminal('in'), Variable('NAME', [Terminal('b')]), Terminal('for')])),
                          ])
def test_reversal(tree, expected):
    """
    Test code for Exercise 6: reversal
    """
    steps = [
            f'from grammars import Variable, Terminal',
            f'tree = {repr(tree)}',
            f"actual = hw8.reversal(tree)"
        ]
    recreate_msg = helpers.gen_recreate_commands(MODULE, steps)

    tree_copy = copy.deepcopy(tree) # make copy of tree to check that it wasn't modified

    try:
        actual = hw8.reversal(tree)
    except Exception as e:
        helpers.fail_and_augment_recreate_unexpected_exception(recreate_msg, e)

    err_msg = helpers.check_result(repr(actual), repr(expected))
    if err_msg is not None:
        pytest.fail(err_msg + recreate_msg)

    err_msg = helpers.check_list_unmodified('tree', repr(tree), repr(tree_copy))
    if err_msg is not None:
        pytest.fail(err_msg + recreate_msg)


@pytest.mark.parametrize("tree, grammar, name, expected",
                         [
                             (Terminal(')'), grammars.DYCK3, 'DYCK3', True),
                             (Terminal(')'), grammars.ARITHMETIC, 'ARITHMETIC', True),
                             (grammars.d1, grammars.DYCK3, 'DYCK3', True),
                             (grammars.at1, grammars.AT, 'AT', True),
                             (grammars.pal1, grammars.PAL_ab, 'PAL_ab', True),
                             (grammars.g1, grammars.NON_PAL_ab, 'NON_PAL_ab', False),
                             (grammars.pal1, grammars.NON_PAL_ab, 'NON_PAL_ab', False),
                             (grammars.c2, grammars.C_LIKE, 'C_LIKE', True),
                             (grammars.e2, grammars.ARITHMETIC, 'ARITHMETIC', True),
                             (grammars.py2, grammars.PY, 'PY', True),
                             (grammars.reg3, grammars.REGEXP, 'REGEXP', True),
                          ])
def test_is_valid_parse_tree(tree, grammar, name, expected):
    """
    Test code for Exercise 7: is_valid_parse_tree
    """
    steps = [
            f'from grammars import Variable, Terminal',
            f"tree = {repr(tree)}",
            f"actual = hw8.is_valid_parse_tree(tree, grammars.{name})"
        ]
    recreate_msg = helpers.gen_recreate_commands(MODULE, steps)

    try:
        actual = hw8.is_valid_parse_tree(tree, grammar)
    except Exception as e:
        helpers.fail_and_augment_recreate_unexpected_exception(recreate_msg, e)

    err_msg = helpers.check_result(repr(actual), repr(expected))
    if err_msg is not None:
        pytest.fail(err_msg + recreate_msg)


d1 = Variable('S', [Terminal('{'), Terminal('}')])
p2 = Variable('statement', [Variable('if_statement', [Terminal('if'), Variable('bool_expr', [Variable('bool_term', [Variable('bool_atom', [Terminal('True')])])]), Terminal(':'), Variable('statement', [Variable('for_loop', [Terminal('for'), Variable('NAME', [Terminal('a')]), Terminal('in'), Variable('NAME', [Terminal('i')]), Terminal(':'), Variable('statement', [Variable('if_statement', [Terminal('if'), Variable('bool_expr', [Variable('bool_term', [Variable('bool_atom', [Terminal('True')])])]), Terminal(':'), Variable('statement', [Variable('assignment', [Variable('target', [Variable('NAME', [Terminal('s')])]), Terminal('='), Variable('expr', [Variable('expr', [Variable('term', [Variable('term', [Variable('atom', [Variable('NAME', [Terminal('h')])])]), Terminal('*'), Variable('atom', [Variable('NUMBER', [Terminal('5')])])])]), Terminal('+'), Variable('term', [Variable('term', [Variable('term', [Variable('atom', [Terminal('('), Variable('expr', [Variable('term', [Variable('atom', [Terminal('('), Variable('expr', [Variable('term', [Variable('atom', [Variable('NUMBER', [Terminal('6')])])])]), Terminal(')')])])]), Terminal(')')])]), Terminal('*'), Variable('atom', [Terminal('('), Variable('expr', [Variable('expr', [Variable('expr', [Variable('term', [Variable('atom', [Variable('NUMBER', [Terminal('2')])])])]), Terminal('+'), Variable('term', [Variable('term', [Variable('term', [Variable('term', [Variable('atom', [Variable('NAME', [Terminal('m')])])]), Terminal('*'), Variable('atom', [Variable('NUMBER', [Terminal('8')])])]), Terminal('*'), Variable('atom', [Terminal('('), Variable('expr', [Variable('expr', [Variable('term', [Variable('term', []), Terminal('*'), Variable('atom', [])])]), Terminal('+'), Variable('term', [Variable('atom', [Terminal('('), Variable('expr', []), Terminal(')')])])]), Terminal(')')])]), Terminal('*'), Variable('atom', [Variable('NUMBER', [Terminal('5')])])])]), Terminal('+'), Variable('term', [Variable('term', [Variable('term', [Variable('atom', [Variable('NUMBER', [Terminal('4')])])]), Terminal('*'), Variable('atom', [Terminal('('), Variable('expr', [Variable('term', [Variable('term', [Variable('term', [Variable('atom', [])]), Terminal('*'), Variable('atom', [Variable('NUMBER', [])])]), Terminal('*'), Variable('atom', [Variable('NAME', [Terminal('r')])])])]), Terminal(')')])]), Terminal('*'), Variable('atom', [Terminal('('), Variable('expr', [Variable('expr', [Variable('expr', [Variable('term', [Variable('atom', [Variable('NUMBER', [])])])]), Terminal('+'), Variable('term', [Variable('term', [Variable('atom', [Variable('NUMBER', [])])]), Terminal('*'), Variable('atom', [Variable('NAME', [Terminal('h')])])])]), Terminal('+'), Variable('term', [Variable('term', [Variable('atom', [Variable('NUMBER', [Terminal('8')])])]), Terminal('*'), Variable('atom', [Variable('NUMBER', [Terminal('5')])])])]), Terminal(')')])])]), Terminal(')')])]), Terminal('*'), Variable('atom', [Variable('NUMBER', [Terminal('8')])])])])])])])])])])])])
r3 = Variable('S', [Variable('X', [Variable('F', [Variable('Y', [Variable('Y', [Variable('Y', [Variable('G', [Variable('C', [Terminal('p')])]), Variable('G', [Variable('Z', [Variable('G', [Variable('C', [Terminal('i')])]), Terminal('*')])])]), Variable('G', [Variable('P', [Terminal('('), Variable('S', [Variable('Y', [Variable('G', [Variable('Z', [Variable('G', [Variable('P', [Terminal('('), Variable('S', [Variable('G', [Variable('C', [Terminal('z')])])]), Terminal(')')])]), Terminal('*')])]), Variable('G', [Variable('Z', [Variable('G', [Variable('C', [Terminal('k')])]), Terminal('*')])])])]), Terminal(')')])])]), Variable('G', [Variable('Z', [Variable('G', [Variable('Z', [Variable('G', [Variable('P', [Terminal('('), Variable('S', [Variable('Y', [Variable('G', [Variable('P', [Terminal('('), Variable('S', [Variable('X', [Variable('X', [Variable('X', [Variable('X', [Variable('X', [Variable('X', []), Terminal('+'), Variable('F', [])]), Terminal('+'), Variable('F', [Variable('G', [])])]), Terminal('+'), Variable('F', [Variable('G', [Variable('Z', [])])])]), Terminal('+'), Variable('F', [Variable('Y', [Variable('Y', [Variable('Y', []), Variable('G', [])]), Variable('G', [Variable('Z', [])])])])]), Terminal('+'), Variable('F', [Variable('G', [Variable('C', [Terminal('a')])])])])]), Terminal(')')])]), Variable('G', [Variable('C', [Terminal('o')])])])]), Terminal(')')])]), Terminal('*')])]), Terminal('*')])])])]), Terminal('+'), Variable('F', [Variable('G', [Variable('P', [Terminal('('), Variable('S', [Variable('Y', [Variable('G', [Variable('P', [Terminal('('), Variable('S', [Variable('G', [Variable('C', [Terminal('a')])])]), Terminal(')')])]), Variable('G', [Variable('P', [Terminal('('), Variable('S', [Variable('Y', [Variable('Y', [Variable('Y', [Variable('Y', [Variable('G', [Variable('C', [Terminal('c')])]), Variable('G', [Variable('P', [Terminal('('), Variable('S', [Variable('Y', [Variable('G', [Variable('P', [Terminal('('), Variable('S', []), Terminal(')')])]), Variable('G', [Variable('C', [Terminal('s')])])])]), Terminal(')')])])]), Variable('G', [Variable('P', [Terminal('('), Variable('S', [Variable('Y', [Variable('G', [Variable('Z', [Variable('G', [Variable('C', [])]), Terminal('*')])]), Variable('G', [Variable('P', [Terminal('('), Variable('S', [Variable('Y', [])]), Terminal(')')])])])]), Terminal(')')])])]), Variable('G', [Variable('Z', [Variable('G', [Variable('Z', [Variable('G', [Variable('P', [Terminal('('), Variable('S', [Variable('X', [Variable('X', []), Terminal('+'), Variable('F', [])])]), Terminal(')')])]), Terminal('*')])]), Terminal('*')])])]), Variable('G', [Variable('C', [Terminal('y')])])])]), Terminal(')')])])])]), Terminal(')')])])])])])
a4 = Variable('S', [Variable('NP', [Variable('ProperNoun', [Terminal('Pat')])]), Variable('VP', [Variable('Verb', [Terminal('pat')]), Variable('NP', [Variable('Pronoun', [Terminal('I')])])])])
w5 = Variable('S', [Terminal('t'), Variable('S', [Terminal('t'), Variable('S', [Terminal('g'), Variable('S', [Terminal('a'), Variable('S', [Terminal('g'), Variable('S', [Terminal('')]), Terminal('c')]), Terminal('t')]), Terminal('c')]), Terminal('a')]), Terminal('a')])
c6 = Variable('statement', [Variable('if_statement', [Terminal('if'), Terminal('('), Variable('bool_expr', [Variable('bool_expr', [Variable('bool_term', [Variable('bool_term', [Variable('bool_atom', [Terminal('('), Variable('bool_expr', [Variable('bool_term', [Variable('bool_atom', [Terminal('false')])])]), Terminal(')')])]), Terminal('&'), Variable('bool_atom', [Terminal('('), Variable('bool_expr', [Terminal('~'), Variable('bool_expr', [Terminal('~'), Variable('bool_expr', [Variable('bool_term', [Variable('bool_atom', [Terminal('false')])])])])]), Terminal(')')])])]), Terminal('^'), Variable('bool_term', [Variable('bool_term', [Variable('bool_atom', [Variable('NAME', [Terminal('i')])])]), Terminal('&'), Variable('bool_atom', [Variable('NAME', [Terminal('f')])])])]), Terminal(')'), Terminal('{'), Variable('statement', [Variable('for_loop', [Terminal('for'), Terminal('('), Variable('type', [Terminal('int')]), Variable('NAME', [Terminal('e')]), Terminal(':'), Variable('NAME', [Terminal('w')]), Terminal(')'), Terminal('{'), Variable('statement', [Terminal('return'), Variable('bool_expr', [Variable('bool_expr', [Variable('bool_term', [Variable('bool_atom', [Terminal('true')])])]), Terminal('^'), Variable('bool_term', [Variable('bool_term', [Variable('bool_atom', [Terminal('('), Variable('bool_expr', [Variable('bool_expr', [Terminal('~'), Variable('bool_expr', [Variable('bool_term', [Variable('bool_term', [Variable('bool_term', [Variable('bool_atom', [Terminal('false')])]), Terminal('&'), Variable('bool_atom', [Terminal('false')])]), Terminal('&'), Variable('bool_atom', [Terminal('false')])])])]), Terminal('^'), Variable('bool_term', [Variable('bool_term', [Variable('bool_term', [Variable('bool_atom', [Variable('NAME', [Terminal('i')])])]), Terminal('&'), Variable('bool_atom', [Variable('NAME', [Terminal('f')])])]), Terminal('&'), Variable('bool_atom', [Terminal('true')])])]), Terminal(')')])]), Terminal('&'), Variable('bool_atom', [Terminal('('), Variable('bool_expr', [Variable('bool_expr', [Terminal('~'), Variable('bool_expr', [Variable('bool_term', [Variable('bool_atom', [Terminal('false')])])])]), Terminal('^'), Variable('bool_term', [Variable('bool_term', [Variable('bool_term', [Variable('bool_atom', [Terminal('false')])]), Terminal('&'), Variable('bool_atom', [Terminal('true')])]), Terminal('&'), Variable('bool_atom', [Terminal('false')])])]), Terminal(')')])])]), Terminal(';')]), Terminal('}')])]), Terminal('}')])])
d7 = Variable('S', [Terminal('{'), Variable('S', [Terminal('('), Terminal(')')]), Terminal('}'), Variable('S', [Terminal('{'), Terminal('}')])])

@pytest.mark.parametrize("seed, grammar, start, name, expected",
                         [(889, grammars.DYCK3, 'S', 'DYCK3', d1),
                          (2434, grammars.PY, 'statement', 'PY', p2),
                          (3193, grammars.REGEXP, 'S', 'REGEXP', r3),
                          (765, grammars.AT, 'S', 'AT', a4),
                          (315, grammars.WC_PAL, 'S', 'WC_PAL', w5),
                          (65, grammars.C_LIKE, 'statement', 'C_LIKE', c6),
                          (173, grammars.DYCK3, 'S', 'DYCK3', d7),
                          ])
def test_generate_parse_tree(seed, grammar, start, name, expected):
    """
    Test code for Exercise 8: generate_parse_tree
    """
    steps = [
            f'import random',
            f'random.seed({seed})',
            f"actual = hw8.generate_parse_tree(grammars.{name}, '{start}')"
        ]
    recreate_msg = helpers.gen_recreate_commands(MODULE, steps)

    try:
        random.seed(seed)
        actual = hw8.generate_parse_tree(grammar, start)
    except Exception as e:
        helpers.fail_and_augment_recreate_unexpected_exception(recreate_msg, e)

    err_msg = helpers.check_result(repr(actual), repr(expected))
    if err_msg is not None:
        pytest.fail(err_msg + recreate_msg)


a41 = Variable('E', [Variable('T', [Variable('F', [Variable('N', [Terminal('0')])])])])
a51 = Variable('E', [Variable('T', [Variable('F', [Variable('N', [Terminal('6')])])])])
r34 = Variable('S', [Variable('X', [Variable('F', [Variable('Y', [Variable('Y', []), Variable('G', [])])]), Terminal('+'), Variable('F', [Variable('Y', [Variable('G', []), Variable('G', [])])])])])
p23 = Variable('statement', [Variable('if_statement', [Terminal('if'), Variable('bool_expr', [Variable('bool_term', [])]), Terminal(':'), Variable('statement', [Variable('if_statement', [])])])])
@pytest.mark.parametrize("seed, grammar, start, depth, name, expected",
                         [(889, grammars.DYCK3, 'S', 1, 'DYCK3', d1),
                          (889, grammars.DYCK3, 'S', 50, 'DYCK3', d1),
                          (315, grammars.ARITHMETIC, 'E', 4, 'ARITHMETIC', a41),
                          (2434, grammars.ARITHMETIC, 'E', 5, 'ARITHMETIC', a51),
                          (3193, grammars.REGEXP, 'S', 4, 'REGEXP', r34),
                          (2434, grammars.PY, 'statement', 3, 'PY', p23),
                          ])
def test_generate_parse_tree_depth(seed, grammar, start, depth, name, expected):
    """
    Test code for Exercise 8: generate_parse_tree with depth
    """
    steps = [
            f'import random'
            f'random.seed({seed})',
            f"actual = hw8.generate_parse_tree(grammars.{name}, '{start}', {depth})"
        ]
    recreate_msg = helpers.gen_recreate_commands(MODULE, steps)

    try:
        random.seed(seed)
        actual = hw8.generate_parse_tree(grammar, start, depth)
    except Exception as e:
        helpers.fail_and_augment_recreate_unexpected_exception(recreate_msg, e)

    err_msg = helpers.check_result(repr(actual), repr(expected))
    if err_msg is not None:
        pytest.fail(err_msg + recreate_msg)

