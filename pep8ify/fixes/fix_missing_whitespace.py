from __future__ import unicode_literals
from lib2to3.fixer_base import BaseFix
from lib2to3.fixer_util import Newline
from lib2to3.pgen2 import token
from lib2to3.pygram import python_symbols as symbols


class FixMissingWhitespace(BaseFix):
    '''
    Each comma, semicolon or colon should be followed by whitespace.
    '''

    def match(self, node):
        if (node.type in (token.COLON, token.COMMA, token.SEMI) and
            node.get_suffix() != " "):
            # If there is a newline after, no space
            if (node.get_suffix().find('\n') == 0 or
                (node.next_sibling and node.next_sibling.children and
                 node.next_sibling.children[0] == Newline())):
                return False
            # If we are using slice notation, no space necessary
            if node.parent.type in [symbols.subscript, symbols.sliceop]:
                return False
            return True
        return False

    def transform(self, node, results):
        next_sibling = node.next_sibling
        if not next_sibling:
            next_sibling = node.parent.next_sibling
            if not next_sibling:
                return
        new_prefix = " %s" % next_sibling.prefix.lstrip(' \t')
        if next_sibling.prefix != new_prefix:
            next_sibling.prefix = new_prefix
            next_sibling.changed()
