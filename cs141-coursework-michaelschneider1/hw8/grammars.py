"""
CMSC 14100
Winter 2025
HW8: Grammars and Parse Trees
"""
import string

class Variable:
    """
    Represents a node for a variable in a parse tree.

    Attributes:
        name (str): name of the variable
        children (list[Variable | Terminal]): subtrees (also parse trees)
    """
    __match_args__ = ('name', 'children')

    def __init__(self, name, children):
        assert isinstance(name, str), f'Variable name {name} must be a string'
        for child in children:
            assert isinstance(child, Variable) or isinstance(child, Terminal), (
                    f'Subtrees must be a Terminal or Variable')
        self.name = name
        self.children = children

    def __repr__(self):
        """
        Produces the expression that recreates this tree.
        """
        return f"Variable('{self.name}', {self.children})"

    def __str__(self):
        """
        Friendlier string representation
        """
        return f"({self.name} => {' '.join([str(child) for child in self.children])})"


class Terminal:
    """
    Represents a leaf for a terminal in a parse tree.

    Attributes:
        name (str): terminal symbol
    """
    __match_args__ = ('name',)

    def __init__(self, name):
        assert isinstance(name, str), f'Terminal name {name} must be a string'
        self.name = name 

    def __repr__(self):
        """
        Produces the expression that recreates this tree.
        """
        return f"Terminal('{self.name}')"

    def __str__(self):
        """
        Friendly string representation. Uses ε to denote an empty string.
        """
        return 'ε' if self.name == '' else self.name


class Grammar:
    """
    Represents a grammar.

    Attributes:
        variables (set[str]): set of variable names
        terminals (set[str]): set of terminals symbols
        productions (dict[str,list[list[str]]]): dictionary of productions
        start (str): name of start variable
    """
    def __init__(self, variables, terminals, productions, start):
        for v in variables:
            assert isinstance(v, str), (
                    f'Variables must be strings: {v} is not a string')
        for a in terminals:
            assert isinstance(a, str), (
                    f'Terminals must be strings: {a} is not a string')
        assert start in variables, (
                f"Start variable '{start}' must be in variables")
        assert variables & terminals == set(), (
                f'Variables and terminals must be disjoint: '
                f'{variables & terminals} are in both')
        for v in productions:
            assert v in variables, (
                    f"LHS of all productions must be a variable: "
                    f"'{v}' is not in variables")
            for rhs in productions[v]:
                for a in rhs:
                    assert a in (variables | terminals), (
                            f"RHS of all productions must be a string of "
                            f"terminals and variables: '{a}' is not a terminal or variable")

        self.variables = variables
        self.terminals = terminals
        self.productions = productions
        self.start = start

    def __repr__(self):
        """
        Produces the expression that recreates the grammar.
        """
        return (f"Grammar({self.variables}, {self.terminals}, "
                f"{self.productions}, '{self.start}')")

    def __str__(self):
        """
        Human-readable definition of the grammar.
        """
        rules = []
        for v in self.productions:
            sents = []
            for rhs in self.productions[v]:
                sent = [f'«{a}»' if a in self.variables else a for a in rhs]
                sents.append(' '.join(sent) if sent else 'ε')
            rules.append(f'«{v}» -> {" | ".join(sents)}')
        ps = '\n    '.join(rules)
        return (f"V = {{{', '.join(sorted(self.variables))}}},"
                f"\nT = {{{', '.join(sorted(self.terminals))}}},"
                f"\nS = {self.start},"
                f"\nP : {ps}")


########################
# Parse tree definitions
########################

g1 = Variable('S', [Terminal('a'), Variable('S', [Terminal('a'), Variable('S', [Terminal('')]), Terminal('b')]), Terminal('b')])
ap1 = Variable('S', [Terminal('b'), Variable('S', [Terminal('a'), Variable('S', [Terminal('a'), Variable('S', [Terminal('a'), Variable('S', [Terminal('b'), Variable('S', [Terminal('a'), Variable('S', [Terminal('')]), Terminal('b')]), Terminal('a')]), Terminal('b')]), Terminal('b')]), Terminal('b')]), Terminal('a')])
pal1 = Variable('S', [Terminal('b'), Variable('S', [Terminal('a'), Variable('S', [Terminal('b'), Variable('S', [Terminal('b'), Variable('S', [Terminal('')]), Terminal('b')]), Terminal('b')]), Terminal('a')]), Terminal('b')])
pal2 = Variable('S', [Terminal('t'), Variable('S', [Terminal('a'), Variable('S', [Terminal('t'), Variable('S', [Terminal('t'), Variable('S', [Terminal('')]), Terminal('t')]), Terminal('t')]), Terminal('a')]), Terminal('t')])
wc1 = Variable('S', [Terminal('t'), Variable('S', [Terminal('c'), Variable('S', [Terminal('a'), Variable('S', [Terminal('c'), Variable('S', [Terminal('g'), Variable('S', [Terminal('c'), Variable('S', [Terminal('')]), Terminal('g')]), Terminal('c')]), Terminal('g')]), Terminal('t')]), Terminal('g')]), Terminal('a')])

e1 = Variable('E', [Variable('T', [Variable('F', [Terminal('('), Variable('E', [Variable('T', [Variable('F', [Variable('N', [Terminal('9')])])])]), Terminal(')')])])])
e2 = Variable('E', [Variable('T', [Variable('T', [Variable('F', [Terminal('('), Variable('E', [Variable('E', [Variable('E', [Variable('E', [Variable('E', [Variable('T', [Variable('T', [Variable('T', [Variable('T', [Variable('T', [Variable('F', [Variable('N', [Variable('N', [Variable('N', [Variable('N', [Terminal('0')]), Terminal('0')]), Terminal('4')]), Terminal('6')])])]), Terminal('×'), Variable('F', [Variable('N', [Variable('N', [Variable('N', [Terminal('4')]), Terminal('3')]), Terminal('5')])])]), Terminal('×'), Variable('F', [Variable('N', [Terminal('0')])])]), Terminal('×'), Variable('F', [Terminal('('), Variable('E', [Variable('E', [Variable('E', [Variable('T', [Variable('T', [Variable('T', [Variable('F', [Variable('N', [Terminal('4')])])]), Terminal('×'), Variable('F', [Variable('N', [Variable('N', [Terminal('6')]), Terminal('8')])])]), Terminal('×'), Variable('F', [Terminal('('), Variable('E', [Variable('E', [Variable('T', [Variable('F', [])])]), Terminal('+'), Variable('T', [Variable('F', [Variable('N', [])])])]), Terminal(')')])])]), Terminal('+'), Variable('T', [Variable('F', [Terminal('('), Variable('E', [Variable('T', [Variable('F', [Variable('N', [Terminal('3')])])])]), Terminal(')')])])]), Terminal('+'), Variable('T', [Variable('F', [Terminal('('), Variable('E', [Variable('T', [Variable('T', [Variable('F', [Terminal('('), Variable('E', [Variable('E', []), Terminal('+'), Variable('T', [])]), Terminal(')')])]), Terminal('×'), Variable('F', [Variable('N', [Variable('N', [Variable('N', []), Terminal('8')]), Terminal('3')])])])]), Terminal(')')])])]), Terminal(')')])]), Terminal('×'), Variable('F', [Variable('N', [Terminal('9')])])])]), Terminal('+'), Variable('T', [Variable('F', [Variable('N', [Terminal('1')])])])]), Terminal('+'), Variable('T', [Variable('F', [Terminal('('), Variable('E', [Variable('E', [Variable('E', [Variable('T', [Variable('T', [Variable('F', [Variable('N', [Variable('N', [Terminal('2')]), Terminal('2')])])]), Terminal('×'), Variable('F', [Variable('N', [Variable('N', [Variable('N', [Variable('N', [Variable('N', [Variable('N', [Variable('N', []), Terminal('3')]), Terminal('1')]), Terminal('6')]), Terminal('5')]), Terminal('0')]), Terminal('8')])])])]), Terminal('+'), Variable('T', [Variable('T', [Variable('F', [Variable('N', [Variable('N', [Terminal('6')]), Terminal('1')])])]), Terminal('×'), Variable('F', [Terminal('('), Variable('E', [Variable('T', [Variable('T', [Variable('T', [Variable('T', [Variable('T', [Variable('F', [Terminal('('), Variable('E', []), Terminal(')')])]), Terminal('×'), Variable('F', [Terminal('('), Variable('E', [Variable('T', [])]), Terminal(')')])]), Terminal('×'), Variable('F', [Terminal('('), Variable('E', [Variable('T', [Variable('F', [])])]), Terminal(')')])]), Terminal('×'), Variable('F', [Variable('N', [Terminal('6')])])]), Terminal('×'), Variable('F', [Variable('N', [Terminal('8')])])])]), Terminal(')')])])]), Terminal('+'), Variable('T', [Variable('F', [Terminal('('), Variable('E', [Variable('T', [Variable('F', [Terminal('('), Variable('E', [Variable('T', [Variable('T', [Variable('T', [Variable('F', [Variable('N', [])])]), Terminal('×'), Variable('F', [Variable('N', [Terminal('8')])])]), Terminal('×'), Variable('F', [Variable('N', [Terminal('9')])])])]), Terminal(')')])])]), Terminal(')')])])]), Terminal(')')])])]), Terminal('+'), Variable('T', [Variable('T', [Variable('F', [Variable('N', [Variable('N', [Terminal('8')]), Terminal('1')])])]), Terminal('×'), Variable('F', [Terminal('('), Variable('E', [Variable('E', [Variable('E', [Variable('E', [Variable('T', [Variable('F', [Variable('N', [Variable('N', [Variable('N', [Variable('N', [Variable('N', [Variable('N', [Terminal('2')]), Terminal('1')]), Terminal('1')]), Terminal('2')]), Terminal('1')]), Terminal('2')])])])]), Terminal('+'), Variable('T', [Variable('T', [Variable('F', [Terminal('('), Variable('E', [Variable('T', [Variable('T', [Variable('T', [Variable('F', [Variable('N', [Variable('N', []), Terminal('3')])])]), Terminal('×'), Variable('F', [Variable('N', [Variable('N', [Variable('N', []), Terminal('0')]), Terminal('4')])])]), Terminal('×'), Variable('F', [Terminal('('), Variable('E', [Variable('E', [Variable('E', [Variable('T', [])]), Terminal('+'), Variable('T', [Variable('F', [])])]), Terminal('+'), Variable('T', [Variable('T', [Variable('T', []), Terminal('×'), Variable('F', [])]), Terminal('×'), Variable('F', [Variable('N', [])])])]), Terminal(')')])])]), Terminal(')')])]), Terminal('×'), Variable('F', [Variable('N', [Variable('N', [Variable('N', [Variable('N', [Terminal('3')]), Terminal('2')]), Terminal('3')]), Terminal('4')])])])]), Terminal('+'), Variable('T', [Variable('T', [Variable('F', [Terminal('('), Variable('E', [Variable('E', [Variable('T', [Variable('F', [Variable('N', [Variable('N', [Terminal('5')]), Terminal('7')])])])]), Terminal('+'), Variable('T', [Variable('T', [Variable('T', [Variable('T', [Variable('T', [Variable('T', [Variable('T', []), Terminal('×'), Variable('F', [])]), Terminal('×'), Variable('F', [Variable('N', [])])]), Terminal('×'), Variable('F', [Variable('N', [Terminal('1')])])]), Terminal('×'), Variable('F', [Variable('N', [Variable('N', [Terminal('9')]), Terminal('1')])])]), Terminal('×'), Variable('F', [Terminal('('), Variable('E', [Variable('E', [Variable('T', [Variable('T', []), Terminal('×'), Variable('F', [])])]), Terminal('+'), Variable('T', [Variable('T', [Variable('T', []), Terminal('×'), Variable('F', [])]), Terminal('×'), Variable('F', [Variable('N', [])])])]), Terminal(')')])]), Terminal('×'), Variable('F', [Variable('N', [Variable('N', [Variable('N', [Variable('N', [Variable('N', []), Terminal('3')]), Terminal('1')]), Terminal('6')]), Terminal('8')])])])]), Terminal(')')])]), Terminal('×'), Variable('F', [Terminal('('), Variable('E', [Variable('E', [Variable('E', [Variable('E', [Variable('E', [Variable('E', [Variable('T', [Variable('T', [Variable('F', [])]), Terminal('×'), Variable('F', [Variable('N', [])])])]), Terminal('+'), Variable('T', [Variable('T', [Variable('T', [Variable('F', [])]), Terminal('×'), Variable('F', [Variable('N', [])])]), Terminal('×'), Variable('F', [Variable('N', [Terminal('0')])])])]), Terminal('+'), Variable('T', [Variable('F', [Variable('N', [Variable('N', [Terminal('1')]), Terminal('9')])])])]), Terminal('+'), Variable('T', [Variable('F', [Variable('N', [Variable('N', [Variable('N', [Terminal('1')]), Terminal('9')]), Terminal('4')])])])]), Terminal('+'), Variable('T', [Variable('T', [Variable('F', [Variable('N', [Terminal('3')])])]), Terminal('×'), Variable('F', [Terminal('('), Variable('E', [Variable('E', [Variable('E', [Variable('E', [Variable('E', []), Terminal('+'), Variable('T', [])]), Terminal('+'), Variable('T', [Variable('T', []), Terminal('×'), Variable('F', [])])]), Terminal('+'), Variable('T', [Variable('F', [Variable('N', [])])])]), Terminal('+'), Variable('T', [Variable('T', [Variable('T', [Variable('F', [])]), Terminal('×'), Variable('F', [Terminal('('), Variable('E', []), Terminal(')')])]), Terminal('×'), Variable('F', [Terminal('('), Variable('E', [Variable('T', [])]), Terminal(')')])])]), Terminal(')')])])]), Terminal('+'), Variable('T', [Variable('T', [Variable('T', [Variable('T', [Variable('T', [Variable('F', [Variable('N', [Variable('N', []), Terminal('4')])])]), Terminal('×'), Variable('F', [Terminal('('), Variable('E', [Variable('E', [Variable('T', [])]), Terminal('+'), Variable('T', [Variable('F', [])])]), Terminal(')')])]), Terminal('×'), Variable('F', [Variable('N', [Variable('N', [Variable('N', [Variable('N', []), Terminal('9')]), Terminal('4')]), Terminal('9')])])]), Terminal('×'), Variable('F', [Terminal('('), Variable('E', [Variable('T', [Variable('F', [Variable('N', [Terminal('8')])])])]), Terminal(')')])]), Terminal('×'), Variable('F', [Variable('N', [Variable('N', [Terminal('5')]), Terminal('1')])])])]), Terminal(')')])])]), Terminal('+'), Variable('T', [Variable('T', [Variable('F', [Terminal('('), Variable('E', [Variable('T', [Variable('T', [Variable('T', [Variable('T', [Variable('F', [Terminal('('), Variable('E', [Variable('T', [Variable('F', [])])]), Terminal(')')])]), Terminal('×'), Variable('F', [Variable('N', [Terminal('1')])])]), Terminal('×'), Variable('F', [Terminal('('), Variable('E', [Variable('E', [Variable('T', [Variable('F', [Terminal('('), Variable('E', []), Terminal(')')])])]), Terminal('+'), Variable('T', [Variable('F', [Variable('N', [Terminal('1')])])])]), Terminal(')')])]), Terminal('×'), Variable('F', [Variable('N', [Variable('N', [Terminal('8')]), Terminal('9')])])])]), Terminal(')')])]), Terminal('×'), Variable('F', [Terminal('('), Variable('E', [Variable('T', [Variable('F', [Variable('N', [Terminal('9')])])])]), Terminal(')')])])]), Terminal(')')])])]), Terminal('+'), Variable('T', [Variable('F', [Terminal('('), Variable('E', [Variable('T', [Variable('F', [Terminal('('), Variable('E', [Variable('E', [Variable('E', [Variable('E', [Variable('E', [Variable('E', [Variable('T', [Variable('T', [Variable('T', [Variable('F', [Variable('N', [])])]), Terminal('×'), Variable('F', [Variable('N', [Terminal('6')])])]), Terminal('×'), Variable('F', [Variable('N', [Variable('N', [Variable('N', []), Terminal('0')]), Terminal('1')])])])]), Terminal('+'), Variable('T', [Variable('F', [Variable('N', [Variable('N', [Variable('N', [Variable('N', []), Terminal('8')]), Terminal('0')]), Terminal('9')])])])]), Terminal('+'), Variable('T', [Variable('F', [Terminal('('), Variable('E', [Variable('E', [Variable('E', [Variable('E', [Variable('E', []), Terminal('+'), Variable('T', [])]), Terminal('+'), Variable('T', [Variable('T', []), Terminal('×'), Variable('F', [])])]), Terminal('+'), Variable('T', [Variable('F', [Terminal('('), Variable('E', []), Terminal(')')])])]), Terminal('+'), Variable('T', [Variable('F', [Variable('N', [Variable('N', []), Terminal('5')])])])]), Terminal(')')])])]), Terminal('+'), Variable('T', [Variable('F', [Terminal('('), Variable('E', [Variable('T', [Variable('T', [Variable('F', [Terminal('('), Variable('E', [Variable('T', [])]), Terminal(')')])]), Terminal('×'), Variable('F', [Variable('N', [Terminal('6')])])])]), Terminal(')')])])]), Terminal('+'), Variable('T', [Variable('F', [Terminal('('), Variable('E', [Variable('T', [Variable('T', [Variable('F', [Terminal('('), Variable('E', [Variable('T', [Variable('T', []), Terminal('×'), Variable('F', [])])]), Terminal(')')])]), Terminal('×'), Variable('F', [Terminal('('), Variable('E', [Variable('E', [Variable('T', [Variable('F', [])])]), Terminal('+'), Variable('T', [Variable('F', [Variable('N', [])])])]), Terminal(')')])])]), Terminal(')')])])]), Terminal('+'), Variable('T', [Variable('F', [Variable('N', [Terminal('4')])])])]), Terminal(')')])])]), Terminal(')')])])]), Terminal(')')])]), Terminal('×'), Variable('F', [Variable('N', [Variable('N', [Terminal('1')]), Terminal('1')])])])])
e3 = Variable('E', [Variable('E', [Variable('T', [Variable('T', [Variable('T', [Variable('F', [Variable('N', [Variable('N', [Variable('N', [Terminal('2')]), Terminal('1')]), Terminal('8')])])]), Terminal('×'), Variable('F', [Variable('N', [Variable('N', [Variable('N', [Variable('N', [Terminal('3')]), Terminal('2')]), Terminal('0')]), Terminal('7')])])]), Terminal('×'), Variable('F', [Variable('N', [Terminal('2')])])])]), Terminal('+'), Variable('T', [Variable('T', [Variable('F', [Terminal('('), Variable('E', [Variable('T', [Variable('T', [Variable('F', [Variable('N', [Terminal('6')])])]), Terminal('×'), Variable('F', [Terminal('('), Variable('E', [Variable('E', [Variable('T', [Variable('T', [Variable('F', [Variable('N', [Terminal('2')])])]), Terminal('×'), Variable('F', [Variable('N', [Variable('N', [Terminal('9')]), Terminal('9')])])])]), Terminal('+'), Variable('T', [Variable('F', [Variable('N', [Terminal('9')])])])]), Terminal(')')])])]), Terminal(')')])]), Terminal('×'), Variable('F', [Variable('N', [Variable('N', [Terminal('4')]), Terminal('2')])])])])

at1 = Variable('S', [Variable('NP', [Variable('Det', [Terminal('the')]), Variable('Nominal', [Variable('Noun', [Terminal('mat')])])]), Variable('VP', [Variable('Verb', [Terminal('sat')]), Variable('NP', [Variable('Det', [Terminal('the')]), Variable('Nominal', [Variable('Noun', [Terminal('oat')])])])])])
at2 = Variable('S', [Variable('NP', [Variable('Det', [Terminal('a')]), Variable('Nominal', [Variable('Noun', [Terminal('cat')])])]), Variable('VP', [Variable('Verb', [Terminal('pat')])])])
at3 = Variable('S', [Variable('NP', [Variable('ProperNoun', [Terminal('Pat')])]), Variable('VP', [Variable('Verb', [Terminal('eat')]), Variable('NP', [Variable('Det', [Terminal('a')]), Variable('Nominal', [Variable('Nominal', [Variable('Nominal', [Variable('Nominal', [Variable('Nominal', [Variable('Nominal', [Variable('Nominal', [Variable('Nominal', [Variable('Noun', [Terminal('bat')])]), Variable('Noun', [Terminal('vat')])]), Variable('Noun', [Terminal('bat')])]), Variable('Noun', [Terminal('oat')])]), Variable('Noun', [Terminal('cat')])]), Variable('Noun', [Terminal('vat')])]), Variable('Noun', [Terminal('hat')])]), Variable('Noun', [Terminal('hat')])])])])])

py1 = Variable('if_statement', [Terminal('if'), Variable('bool_expr', [Variable('bool_term', [Variable('bool_atom', [Terminal('('), Variable('bool_expr', [Variable('bool_term', [Variable('bool_term', [Variable('bool_atom', [Terminal('False')])]), Terminal('and'), Variable('bool_atom', [Terminal('True')])])]), Terminal(')')])])]), Terminal(':'), Variable('statement', [Variable('if_statement', [Terminal('if'), Variable('bool_expr', [Terminal('not'), Variable('bool_expr', [Variable('bool_expr', [Variable('bool_expr', [Variable('bool_term', [Variable('bool_atom', [Terminal('True')])])]), Terminal('or'), Variable('bool_term', [Variable('bool_term', [Variable('bool_atom', [Terminal('True')])]), Terminal('and'), Variable('bool_atom', [Variable('NAME', [Terminal('n')])])])]), Terminal('or'), Variable('bool_term', [Variable('bool_term', [Variable('bool_atom', [Variable('NAME', [Terminal('e')])])]), Terminal('and'), Variable('bool_atom', [Variable('NAME', [Terminal('e')])])])])]), Terminal(':'), Variable('statement', [Terminal('return'), Variable('bool_expr', [Variable('bool_expr', [Variable('bool_term', [Variable('bool_atom', [Terminal('('), Variable('bool_expr', [Variable('bool_term', [Variable('bool_atom', [Variable('NAME', [Terminal('e')])])])]), Terminal(')')])])]), Terminal('or'), Variable('bool_term', [Variable('bool_term', [Variable('bool_term', [Variable('bool_term', [Variable('bool_atom', [Variable('NAME', [Terminal('j')])])]), Terminal('and'), Variable('bool_atom', [Variable('NAME', [Terminal('m')])])]), Terminal('and'), Variable('bool_atom', [Terminal('True')])]), Terminal('and'), Variable('bool_atom', [Variable('NAME', [Terminal('d')])])])])])])])])
py2 = Variable('for_loop', [Terminal('for'), Variable('NAME', [Terminal('b')]), Terminal('in'), Variable('NAME', [Terminal('s')]), Terminal(':'), Variable('statement', [Terminal('return'), Variable('expr', [Variable('term', [Variable('term', [Variable('atom', [Terminal('('), Variable('expr', [Variable('term', [Variable('atom', [Variable('NUMBER', [Terminal('6')])])])]), Terminal(')')])]), Terminal('*'), Variable('atom', [Variable('NUMBER', [Terminal('2')])])])])])])
py3 = Variable('statement', [Terminal('return'), Variable('expr', [Variable('term', [Variable('atom', [Variable('NUMBER', [Terminal('7')])])])])])

c1 = Variable('statement', [Variable('if_statement', [Terminal('if'), Terminal('('), Variable('bool_expr', [Terminal('~'), Variable('bool_expr', [Terminal('~'), Variable('bool_expr', [Variable('bool_expr', [Terminal('~'), Variable('bool_expr', [Terminal('~'), Variable('bool_expr', [Terminal('~'), Variable('bool_expr', [Variable('bool_expr', [Variable('bool_term', [Variable('bool_atom', [Terminal('true')])])]), Terminal('^'), Variable('bool_term', [Variable('bool_atom', [Variable('NAME', [Terminal('l')])])])])])])]), Terminal('^'), Variable('bool_term', [Variable('bool_atom', [Terminal('('), Variable('bool_expr', [Terminal('~'), Variable('bool_expr', [Variable('bool_term', [Variable('bool_term', [Variable('bool_atom', [Terminal('true')])]), Terminal('&'), Variable('bool_atom', [Terminal('true')])])])]), Terminal(')')])])])])]), Terminal(')'), Terminal('{'), Variable('statement', [Terminal('return'), Variable('bool_expr', [Variable('bool_expr', [Variable('bool_term', [Variable('bool_term', [Variable('bool_term', [Variable('bool_term', [Variable('bool_term', [Variable('bool_atom', [Terminal('('), Variable('bool_expr', [Variable('bool_term', [Variable('bool_term', [Variable('bool_atom', [Terminal('false')])]), Terminal('&'), Variable('bool_atom', [Terminal('false')])])]), Terminal(')')])]), Terminal('&'), Variable('bool_atom', [Variable('NAME', [Terminal('w')])])]), Terminal('&'), Variable('bool_atom', [Terminal('true')])]), Terminal('&'), Variable('bool_atom', [Terminal('false')])]), Terminal('&'), Variable('bool_atom', [Terminal('('), Variable('bool_expr', [Variable('bool_expr', [Variable('bool_term', [Variable('bool_term', [Variable('bool_atom', [Variable('NAME', [Terminal('u')])])]), Terminal('&'), Variable('bool_atom', [Terminal('true')])])]), Terminal('^'), Variable('bool_term', [Variable('bool_term', [Variable('bool_term', [Variable('bool_atom', [Terminal('false')])]), Terminal('&'), Variable('bool_atom', [Terminal('true')])]), Terminal('&'), Variable('bool_atom', [Terminal('true')])])]), Terminal(')')])])]), Terminal('^'), Variable('bool_term', [Variable('bool_atom', [Terminal('true')])])]), Terminal(';')]), Terminal('}')])])
c2 = Variable('if_statement', [Terminal('if'), Terminal('('), Variable('bool_expr', [Variable('bool_term', [Variable('bool_term', [Variable('bool_atom', [Terminal('('), Variable('bool_expr', [Terminal('~'), Variable('bool_expr', [Terminal('~'), Variable('bool_expr', [Variable('bool_term', [Variable('bool_atom', [Terminal('('), Variable('bool_expr', [Variable('bool_term', [Variable('bool_term', [Variable('bool_atom', [Variable('NAME', [Terminal('n')])])]), Terminal('&'), Variable('bool_atom', [Terminal('('), Variable('bool_expr', [Terminal('~'), Variable('bool_expr', [Terminal('~'), Variable('bool_expr', [Terminal('~'), Variable('bool_expr', [Variable('bool_term', [Variable('bool_atom', [Terminal('('), Variable('bool_expr', [Variable('bool_expr', []), Terminal('^'), Variable('bool_term', [])]), Terminal(')')])])])])])]), Terminal(')')])])]), Terminal(')')])])])])]), Terminal(')')])]), Terminal('&'), Variable('bool_atom', [Terminal('true')])])]), Terminal(')'), Terminal('{'), Variable('statement', [Terminal('return'), Variable('expr', [Variable('expr', [Variable('term', [Variable('atom', [Variable('NAME', [Terminal('l')])])])]), Terminal('+'), Variable('term', [Variable('term', [Variable('atom', [Variable('NUMBER', [Terminal('8')])])]), Terminal('*'), Variable('atom', [Terminal('('), Variable('expr', [Variable('term', [Variable('term', [Variable('term', [Variable('atom', [Variable('NUMBER', [Terminal('0')])])]), Terminal('*'), Variable('atom', [Variable('NUMBER', [Terminal('9')])])]), Terminal('*'), Variable('atom', [Variable('NAME', [Terminal('y')])])])]), Terminal(')')])])]), Terminal(';')]), Terminal('}')])
c3 = Variable('for_loop', [Terminal('for'), Terminal('('), Variable('type', [Terminal('bool')]), Variable('NAME', [Terminal('l')]), Terminal(':'), Variable('NAME', [Terminal('z')]), Terminal(')'), Terminal('{'), Variable('statement', [Terminal('return'), Variable('expr', [Variable('expr', [Variable('expr', [Variable('term', [Variable('atom', [Variable('NUMBER', [Terminal('5')])])])]), Terminal('+'), Variable('term', [Variable('atom', [Variable('NAME', [Terminal('x')])])])]), Terminal('+'), Variable('term', [Variable('atom', [Variable('NUMBER', [Terminal('4')])])])]), Terminal(';')]), Terminal('}')])

d1 = Variable('S', [Terminal('{'), Variable('S', [Terminal('['), Terminal(']')]), Terminal('}'), Variable('S', [Terminal('{'), Terminal('}')])])
d2 = Variable('S', [Terminal('('), Terminal(')')])
d3 = Variable('S', [Terminal('['), Variable('S', [Terminal('['), Variable('S', [Terminal('{'), Terminal('}')]), Terminal(']'), Variable('S', [Terminal('('), Variable('S', [Terminal('['), Variable('S', [Terminal('['), Terminal(']')]), Terminal(']'), Variable('S', [Terminal('['), Variable('S', [Terminal('('), Terminal(')')]), Terminal(']'), Variable('S', [Terminal('('), Variable('S', [Terminal('['), Variable('S', [Terminal('{'), Variable('S', [Terminal('{'), Terminal('}')]), Terminal('}'), Variable('S', [Terminal('{'), Terminal('}')])]), Terminal(']'), Variable('S', [Terminal('{'), Variable('S', [Terminal('['), Variable('S', [Terminal('{'), Variable('S', [Terminal('['), Terminal(']')]), Terminal('}'), Variable('S', [Terminal('{'), Terminal('}')])]), Terminal(']'), Variable('S', [Terminal('['), Variable('S', [Terminal('('), Terminal(')')]), Terminal(']'), Variable('S', [Terminal('['), Terminal(']')])])]), Terminal('}'), Variable('S', [Terminal('('), Terminal(')')])])]), Terminal(')'), Variable('S', [Terminal('('), Variable('S', [Terminal('('), Terminal(')')]), Terminal(')'), Variable('S', [Terminal('['), Terminal(']')])])])])]), Terminal(')'), Variable('S', [Terminal('['), Variable('S', [Terminal('('), Variable('S', [Terminal('{'), Terminal('}')]), Terminal(')'), Variable('S', [Terminal('['), Terminal(']')])]), Terminal(']'), Variable('S', [Terminal('{'), Terminal('}')])])])]), Terminal(']'), Variable('S', [Terminal('('), Terminal(')')])])

reg1 = Variable('S', [Variable('Y', [Variable('G', [Variable('P', [Terminal('('), Variable('S', [Variable('Y', [Variable('G', [Variable('C', [Terminal('j')])]), Variable('G', [Variable('C', [Terminal('a')])])])]), Terminal(')')])]), Variable('G', [Variable('Z', [Variable('G', [Variable('Z', [Variable('G', [Variable('C', [Terminal('y')])]), Terminal('*')])]), Terminal('*')])])])])
reg2 = Variable('S', [Variable('X', [Variable('X', [Variable('F', [Variable('Y', [Variable('G', [Variable('Z', [Variable('G', [Variable('P', [Terminal('('), Variable('S', [Variable('Y', [Variable('Y', [Variable('G', [Variable('C', [Terminal('a')])]), Variable('G', [Variable('C', [Terminal('u')])])]), Variable('G', [Variable('Z', [Variable('G', [Variable('C', [Terminal('a')])]), Terminal('*')])])])]), Terminal(')')])]), Terminal('*')])]), Variable('G', [Variable('C', [Terminal('r')])])])]), Terminal('+'), Variable('F', [Variable('G', [Variable('C', [Terminal('o')])])])]), Terminal('+'), Variable('F', [Variable('Y', [Variable('G', [Variable('Z', [Variable('G', [Variable('C', [Terminal('t')])]), Terminal('*')])]), Variable('G', [Variable('C', [Terminal('w')])])])])])])
reg3 = Variable('S', [Variable('Y', [Variable('Y', [Variable('Y', [Variable('G', [Variable('Z', [Variable('G', [Variable('Z', [Variable('G', [Variable('C', [Terminal('v')])]), Terminal('*')])]), Terminal('*')])]), Variable('G', [Variable('Z', [Variable('G', [Variable('C', [Terminal('a')])]), Terminal('*')])])]), Variable('G', [Variable('C', [Terminal('e')])])]), Variable('G', [Variable('Z', [Variable('G', [Variable('P', [Terminal('('), Variable('S', [Variable('G', [Variable('Z', [Variable('G', [Variable('P', [Terminal('('), Variable('S', [Variable('G', [Variable('Z', [Variable('G', [Variable('Z', [Variable('G', [Variable('P', [Terminal('('), Variable('S', [Variable('X', [Variable('X', []), Terminal('+'), Variable('F', [])])]), Terminal(')')])]), Terminal('*')])]), Terminal('*')])])]), Terminal(')')])]), Terminal('*')])])]), Terminal(')')])]), Terminal('*')])])])])

############################
# Grammar definition helpers
############################
def rules(alp):
    """
    Transform space-separated CFG rules to list form
    """
    return [list(x) for x in alp.split(' ')]

def lex(words):
    """
    Ensure lexicon rules are in consistent order
    """
    return sorted([[x] for x in words])

def lingrule(rules):
    """
    Convert linguistics-style rules to list form
    """
    return [x.split() for x in rules]

def bnf(rules):
    """
    Convert Backus-Naur-style rules to list form
    """
    return [x.split() for x in rules.split(' | ')]

#####################
# Grammar definitions
#####################

# {a^k b^k | k >= 0}
AB_n = Grammar({'S'}, set('ab'), {'S': rules('aSb ')}, 'S')

# Dyck(3): The language of balanced brackets on three different types of brackets
DYCK3 = Grammar({'S'}, 
            set('(){}[]'), 
            {'S': rules('(S)S [S]S {S}S () [] {}')},
            'S')

# Palindromes over a and b
PAL_ab = Grammar({'S'},
                 set('ab'),
                 {'S': rules('aSa bSb a b ')},
                 'S')

# Non-palindromes over a and b
NON_PAL_ab = Grammar({'S', 'A'},
                     set('ab'),
                     {'S': rules('aSa bSb aAb bAa'),
                      'A': rules(' aA bA')},
                     'S')

# Watson-Crick palindromes
WC_PAL = Grammar({'S'},
                 set('acgt'),
                 {'S': rules('aSt cSg gSc tSa ')},
                 'S')

# Non-squares over a and b
NON_SQ_ab = Grammar(set('SAB'),
                    set('ab'),
                    {'S': rules('AB BA A B'),
                     'A': rules('aAa aAb bAa bAb a'),
                     'B': rules('aBa aBb Bba bBb b')},
                     'S')

# Basic arithmetic expressions
ARITHMETIC = Grammar(set('ETFN'),
                     set('+×()0123456789'),
                     {'E': rules('E+T T'),
                      'T': rules('T×F F'),
                      'F': rules('(E) N'),
                      'N': ([list(x) for x in string.digits] +
                            [['N',x] for x in string.digits])},
                     'E')

# Regular expressions (Shallit, 2009)
REGEXP = Grammar(set('SFGCPXYZ'),
                 set('()+*') | set(string.ascii_lowercase),
                 {'S': rules('X Y G'),
                  'X': rules('X+F F+F'),
                  'F': rules('Y G'),
                  'Y': rules('YG GG'),
                  'G': rules('Z C P'),
                  'C': [[x] for x in string.ascii_lowercase],
                  'Z': rules('G*'),
                  'P': rules('(S)')},
                 'S')

# the cat eat the hat
AT = Grammar({'S', 'NP', 'VP', 'Nominal', 'Det', 'Pronoun', 'ProperNoun', 
              'Noun', 'Verb'},
             {'the', 'a', 'I', 'you', 'it', 'Pat', 'bat', 'cat', 'hat', 'mat', 
              'oat', 'rat', 'vat', 'eat', 'pat', 'sat'},
             {'S': bnf('NP VP'),
              'NP': bnf('Pronoun | ProperNoun | Det Nominal'),
              'Nominal': bnf('Nominal Noun | Noun'),
              'VP': bnf('Verb | Verb NP'),
              'Det': bnf('the | a'),
              'Pronoun': bnf('I | you | it'),
              'ProperNoun': bnf('Pat'),
              'Noun': bnf('bat | cat | hat | mat | oat | rat | vat'),
              'Verb': bnf('eat | pat | sat')},
             'S')

# Started from Guido Van Rossum's small grammar at
# https://medium.com/@gvanrossum_83706/peg-parsers-7ed72462f97c
PY = Grammar({'statement', 'expr', 'term', 'atom', 'assignment', 'target', 
              'if_statement', 'for_loop', 'NAME', 'NUMBER', 'bool_expr',
              'bool_term', 'bool_atom'},
             (set('+,*,-,/,(,),=,:,if,return,for,in,or,and,not,True,False'.split(',')) |
              set(string.ascii_lowercase) |
              set(string.digits)),
             {'statement': bnf('assignment | return expr | return bool_expr | if_statement | for_loop'),
              'expr': bnf('expr + term | term'),
              'bool_expr': bnf('not bool_expr | bool_expr or bool_term | bool_term'),
              'bool_term': bnf('bool_term and bool_atom | bool_atom'),
              'bool_atom': bnf('NAME | True | False | ( bool_expr )'),
              'term': bnf('term * atom | atom'),
              'atom': bnf('NAME | NUMBER | ( expr )'),
              'assignment': bnf('target = expr'),
              'target': bnf('NAME'),
              'if_statement': bnf('if bool_expr : statement'),
              'for_loop': bnf('for NAME in NAME : statement'),
              'NAME': [[x] for x in string.ascii_lowercase],
              'NUMBER': [[x] for x in string.digits]},
             'statement')

# C-like version
C_LIKE = Grammar({'statement', 'expr', 'term', 'atom', 'assignment', 'target', 
                  'if_statement', 'for_loop', 'NAME', 'NUMBER', 'bool_expr',
                  'bool_term', 'bool_atom', 'type'},
                 (set('+,*,-,/,(,),=,:,if,return,for,{,},true,false,&,^,~,;,int,bool,double,char,float'.split(',')) |
                  set(string.ascii_lowercase) |
                  set(string.digits)), 
                 {'statement': bnf('assignment ; | return expr ; | return bool_expr ; | if_statement | for_loop'), 
                  'expr': bnf('expr + term | term'), 
                  'bool_expr': bnf('~ bool_expr | bool_expr ^ bool_term | bool_term'),
                  'bool_term': bnf('bool_term & bool_atom | bool_atom'),
                  'bool_atom': bnf('NAME | true | false | ( bool_expr )'),
                  'term': bnf('term * atom | atom'), 
                  'atom': bnf('NAME | NUMBER | ( expr )'), 
                  'assignment': bnf('type target = expr'), 
                  'target': bnf('NAME'), 
                  'if_statement': bnf('if ( bool_expr ) { statement }'), 
                  'for_loop': bnf('for ( type NAME : NAME ) { statement }'), 
                  'type': bnf('int | bool | double | char'),
                  'NAME': [[x] for x in string.ascii_lowercase], 
                  'NUMBER': [[x] for x in string.digits]}, 
                 'statement')


# Definition for a simple English grammar, from Jurafsky and Martin (2025) Ch. 18 
# https://web.stanford.edu/~jurafsky/slp3/
# add or replace with your favourite words
nouns = set(('gun chili pepper book thief pants elephant morning trip '
             'breeze flight class cat horse car house course beef stew chicken '
             'volleyball phone tablet computer science program code keyboard '
             'fish swimming swim piano guitar monitor saxophone euphonium shoe '
             'department city division angle grinder saw tooth headphones '
             'pork bowl ball rice noodles congee egg pita bread carrot pumpkin '
             'kabocha celery broccoli cow pig boar wool cotton leather boot '
             'crow owl snake pigeon seagull eagle wall iron knife ').split())
verbs = set(('do want throw write leave fly shot run read take pet eat fish '
             'shout talk sing dance listen speak stream swim type calculate '
             'grow harvest bake broil braise fry toast drink water buy sell '
             'compose illuminate steal break jump pickle cook clean walk ').split())
adjectives = set(('first last latest direct nice easy comfortable troublesome '
                  'far cold hot warm fast slow exciting boring quick').split())
det = set('the a an this that these those some much many most any all'.split())
pronouns = set('he she I you me it us they them'.split())
proper_nouns = set(('Chicago Toronto Tokyo Halifax Charlottetown Waterloo '
                    'Kitchener London Pickering Oshawa Mississauga '
                    'Edmonton Calgary Vancouver Surrey Guelph Brampton '
                    'Montréal Québec Gatineau Ottawa Markham Stouffville '
                    'Parkdale Scarborough Willowdale Guildwood Agincourt Rouge '
                    'Pearson Diefenbaker King Vaughan Caledon Halton Hamilton '
                    'Oliver Ike Maria Salome Sara Katrina Lauren Claire Joe '
                    'Belmond Leos Levi Shellin Eli Emma Sonny Enna Claude Wilson ').split())
prepositions = set(('from to on near in through above behind under ahead below ' 
                    'beneath').split())
conjunctions = set('and or but'.split())
aux = set('be can could do have might may must should will does'.split())
possessives = set('my your his her their'.split())
adverbs = set(('totally completely helpfully cheerfully terribly sutbly ' 
               'accidentally namely conversely certainly usually generally '
               'frequently rarely suspiciously generously loudly kindly ').split())

lexicon = (nouns | verbs | det | pronouns | proper_nouns | prepositions | 
           aux | adjectives | adverbs | possessives)

ENG = Grammar({'S', 'NP', 'VP', 'Det', 'N', 'V', 'Nom', 'PP', 'Pronoun',
               'Proper', 'Prep', 'Adv', 'Poss', 'AP', 'Adj', 'Aux'},
              lexicon,
              {'S': lingrule(['NP VP', 'VP', 'Aux NP VP']),
               'NP': lingrule(['Det Nom', 'Pronoun', 'Proper', 'AP NP']),
               'VP': lingrule(['V NP', 'V', 'V NP PP', 'V PP', 'VP PP', 'Adv VP']),
               'AP': lingrule(['Det', 'Poss', 'AP Adj']),
               'Nom': lingrule(['Nom N', 'N', 'Nom PP']),
               'PP': lingrule(['Prep NP']),
               'Det': lex(det),
               'N': lex(nouns),
               'V': lex(verbs),
               'Adj': lex(adjectives),
               'Adv': lex(adverbs),
               'Aux': lex(aux),
               'Poss': lex(possessives),
               'Pronoun': lex(pronouns),
               'Proper': lex(proper_nouns),
               'Prep': lex(prepositions)
               },
              'S')

