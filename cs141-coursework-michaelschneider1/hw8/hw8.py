"""
CMSC 14100
Winter 2025
Homework #8

We will be using anonymous grading, so please do NOT include your name
in this file.

People Consulted:
   List anyone (other than the course staff) that you consulted about
   this assignment.

Online resources consulted:
   List the URLs of any online resources other than the course text and
   the official Python language documentation that you used to complete
   this assignment.
"""

import random
from grammars import Variable, Terminal

# Constants for indicating variables in evaluation
LEFT_VAR_BRACKET = '«'  # LEFT-POINTING DOUBLE ANGLE QUOTATION MARK, chr(0xAB)
RIGHT_VAR_BRACKET = '»' # RIGHT-POINTING DOUBLE ANGLE QUOTATION MARK, chr(0xBB)


# Exercise 1
def is_pal(seq, transform):
    """
    Given a sequence and an involutive antimorphism, determine whether the
    sequence is a palindrome with respect to the antimorphism.

    Input:
        seq (list[str]): sequence as a list
        transform (dict[str,str]): dictionary that maps a letter to a letter,
            is involutive

    Output (bool): True if seq is palindromic under transform, False otherwise
    """
    if seq == []:
        return True
    else:
        first, *rest = seq
        if transform[first] != seq[-1]:
            return False
        else:
            return is_pal(rest[:-1], transform)

# Exercise 2
def derivation_length(tree):
    """
    Given a parse tree, compute the length of the derivation represented by the 
    parse tree. The length of the derivation is the number of production rules
    that are applied according to the parse tree.

    Input: 
        tree (Variable | Terminal): parse tree

    Output (int): length of derivation for parse tree
    """
    if isinstance(tree, Terminal) or tree.children == []:
        return 0
    else:
        total = 0
        for child in tree.children:
            total += derivation_length(child)
        return total + 1

# Exercise 3
def is_equal(tree1, tree2):
    """
    Given two parse trees, determine if they are equal.

    Input:
        tree1 (Variable | Terminal): a parse tree
        tree2 (Variable | Terminal): a parse tree

    Output (bool): True if tree1 and tree2 are equal, False otherwise
    """
    if isinstance(tree1, Terminal) and isinstance(tree2, Terminal):
        return tree1.name == tree2.name
    elif isinstance(tree1, Variable) and isinstance (tree2, Variable):
        if len(tree1.children) != len(tree2.children):
            return False
        if tree1.name != tree2.name:
            return False
        for index in range(len(tree1.children)):
            return is_equal(tree1.children[index], tree2.children[index])
        return True
    else:
        return False
# Exericse 4
def evaluate(tree, separator=''):
    """
    Given a parse tree, produce the string that it represents. Terms may be 
    separated by a given separator. If the parse tree is incomplete, then for
    each variable with name V and no children, the string '«V»' is produced.

    Input:
        tree (Variable | Terminal): parse tree
        separator (str): Separator in between terminal symbols in the resulting
            string. Empty string by default.

    Output (str): the string represented by the parse tree
    """
    final_list = []
    if isinstance(tree, Terminal):
        final_list.append(tree.name)
    elif isinstance(tree, Variable):
        if len(tree.children) == 0:
            final_list.append(LEFT_VAR_BRACKET + tree.name + RIGHT_VAR_BRACKET)
        else:
            for child in tree.children:
                final_list.append(evaluate(child, separator))
    
    return separator.join(final_list)

# Exercise 5
def morph(tree, ph):
    """
    Given a parse tree and a morphism, produce a new parse tree that represents 
    the string for the parse tree after applying the morphism. The new parse 
    tree may not necessarily be a valid parse tree for the original grammar.

    Input:
        tree (Variable | Terminal): parse tree
        ph (dict[str,str]): a dictionary that maps a terminal to another string

    Output (Variable | Terminal): parse tree for the morphic image of the string
    """
    if isinstance(tree, Terminal):
        return Terminal(ph.get(tree.name))
    elif isinstance(tree, Variable):
        final = Variable(tree.name, [])

        for child in tree.children:
            if isinstance(child, Variable):
                final.children.append(morph(child, ph))
            else:
                final.children.append(Terminal(ph.get(child.name)))
        return final

# Exercise 6
def reversal(tree):
    """
    Given a parse tree, produce a new parse tree that represents the string
    in reverse. The new parse tree may not necessarily be a valid parse tree 
    for the original grammar.

    Input:
        tree (Variable | Terminal): parse tree

    Output (Variable | Terminal): parse tree for the reversal of the string
    """
    if isinstance(tree, Terminal):
        return tree
    elif isinstance(tree, Variable):
        final = Variable(tree.name, [])

        for child in reversed(tree.children):
            if isinstance(child, Variable):
                final.children.append(reversal(child))
            else:
                final.children.append(Terminal(child.name))
    
        return final
# Exercise 7
def is_valid_parse_tree(tree, grammar):
    """
    Given a parse tree and a grammar, determine if the parse tree is valid with
    respect to the given grammar.

    Input:
        tree (Variable | Terminal): parse tree
        grammar (Grammar): grammar definition

    Output (bool): True if tree is valid for grammar, False otherwise
    """
    if isinstance(tree, Terminal):
        return tree.name in grammar.terminals or tree.name == ''
    else:
        if tree.name not in grammar.variables:
            return False
        if tree.children == []:
            return True
        else:
            name_list = []
            for child in tree.children:
                if child.name != '':
                    name_list.append(child.name)
            if name_list not in grammar.productions.get(tree.name, []):
                return False

            for child in tree.children:
                if not is_valid_parse_tree(child, grammar):
                    return False
            
            return True

# Exericse 8
def generate_parse_tree(grammar, var, depth=20):
    """
    Given a grammar, produce a randomly generated parse tree. Provide a depth
    to control the height of the resulting parse tree, which may produce an
    incomplete, but valid, parse tree.

    Input:
        grammar (Grammar): a grammar
        var (str): the name of the variable for the root of the tree
        depth (int): maximum depth of the parse tree to generate, 20 by default

    Output (Variable): A parse tree rooted at the given variable
    """
    if depth == 0:
        if var in grammar.terminals:
            return Variable(var, [Terminal(var)])
        else:
            return Variable(var, [])
    if var not in grammar.productions:
        return Variable(var, [])
    
    random_production = random.choice(grammar.productions[var])

    children = []
    for name in random_production:
        if name in grammar.variables:
            children.append(generate_parse_tree(grammar, name, depth - 1))
        else:
            children.append(Terminal(name))
    if random_production == []:
        children.append(Terminal(''))
    
    return Variable(var, children)