# Xrhstos Xristidhs 4526
from enum import Enum
import sys


class TokenNomenclature(Enum):
    # arithmetic operators:
    PLUS = 0
    MINUS = 1
    ASTERISK = 2
    SLASH = 3

    # relational operators:
    LESSTHAN = 4
    GREATERTHAN = 5
    EQUALS = 6              # =
    LESSTHANEQUALS = 7
    GREATERTHANEQUALS = 8
    NOTEQUALS = 9           # <>

    # assignment symbol
    ASSIGN = 10             # :=

    # delimeters
    SEMICOLON = 11
    COMMA = 12
    COLON = 13

    # parentheses and brackets
    SQRBROPEN = 14          # [
    SQRBRCLOSE = 15         # ]
    PARENTHOPEN = 16        # (
    PARENTHCLOSE = 17       # )
    CURLYBROPEN = 18        # {
    CURLYBRCLOSE = 19       # }

    # End of program:
    FULLSTOP = 20           # .

    # comment symbol:
    COMMENT = 21            # #

    #  keywords:
    PROGRAM = 22
    DECLARE = 23
    IF = 24
    ELSE = 25
    WHILE = 26
    SWITCHCASE = 27
    FORCASE = 28
    INCASE = 29
    CASE = 30
    DEFAULT = 31
    NOT = 32
    AND = 33
    OR = 34
    FUNCTION = 35
    PROCEDURE = 36
    CALL = 37
    RETURN = 38
    IN = 39
    INOUT = 40
    INPUT = 41
    PRINT = 42

    # end of file
    EOF = 43


tokens = {
    '+':            TokenNomenclature.PLUS,
    '-':            TokenNomenclature.MINUS,
    '*':            TokenNomenclature.ASTERISK,
    '/':            TokenNomenclature.SLASH,
    '<':            TokenNomenclature.LESSTHAN,
    '>':            TokenNomenclature.GREATERTHAN,
    '=':            TokenNomenclature.EQUALS,
    '<=':           TokenNomenclature.LESSTHANEQUALS,
    '>=':           TokenNomenclature.GREATERTHANEQUALS,
    '<>':           TokenNomenclature.NOTEQUALS,
    ':=':           TokenNomenclature.ASSIGN,
    ';':            TokenNomenclature.SEMICOLON,
    ',':            TokenNomenclature.COMMA,
    ':':            TokenNomenclature.COLON,
    '[':            TokenNomenclature.SQRBROPEN,
    ']':            TokenNomenclature.SQRBRCLOSE,
    '(':            TokenNomenclature.PARENTHOPEN,
    ')':            TokenNomenclature.PARENTHCLOSE,
    '{':            TokenNomenclature.CURLYBROPEN,
    '}':            TokenNomenclature.CURLYBRCLOSE,
    '.':            TokenNomenclature.FULLSTOP,
    '#':            TokenNomenclature.COMMENT,
    'program':      TokenNomenclature.PROGRAM,
    'declare':      TokenNomenclature.DECLARE,
    'if':           TokenNomenclature.IF,
    'else':         TokenNomenclature.ELSE,
    'while':        TokenNomenclature.WHILE,
    'switchcase':   TokenNomenclature.SWITCHCASE,
    'forcase':      TokenNomenclature.FORCASE,
    'incase':       TokenNomenclature.INCASE,
    'case':         TokenNomenclature.CASE,
    'default':      TokenNomenclature.DEFAULT,
    'not':          TokenNomenclature.NOT,
    'and':          TokenNomenclature.AND,
    'or':           TokenNomenclature.OR,
    'function':     TokenNomenclature.FUNCTION,
    'procedure':    TokenNomenclature.PROCEDURE,
    'call':         TokenNomenclature.CALL,
    'return':       TokenNomenclature.RETURN,
    'in':           TokenNomenclature.IN,
    'inout':        TokenNomenclature.INOUT,
    'EOF':          TokenNomenclature.EOF
}


def openfile(path):
    global fd

    try:
        fd = open(path, 'r')

    except IOError:
        sys.exit("Error: File does not appear to exist.")


# TODO: len(varname) <= 30



def lex():
    """potential keyword list."""
    pot_keyword = []
    """state board:
            0: default state / blank-character-as-input state
            1: alphabet state
            2: digit state
            3: arithmetic operator or delimiter state (+, -, *, /, =) or (, , ;, [, ], (, ), {, })
            4: less-than sign state (<)
            5: greater-than sign state (>)
            6: colon state (:)
            7: comment state (#)
            8: EOF state ('')
            9: empty sequence state
    """
    state = 0
    status = False  # non-final state

    while status is False:
        curr = fd.read(1)
        if state == 0:
            if curr.isalpha():
                state = 1  # goto: check for alphanumeric
            elif curr.isdigit():
                state = 2  # goto: final
            elif curr in ('+', '-', '*', '/', '=', '(', ')', ';', '[', ']', ',', '{', '}'):
                state = 3
            elif curr == '<':
                state = 4
            elif curr == '>':
                state = 5
            elif curr == ':':
                state = 6
            elif curr == '#':
                state = 7

        elif state == 1:
            curr = fd.read(1)
            while curr.isalnum():







def main(argv):
   input_file = argv[1]
   openfile(input_file)
   lex()


if __name__ == "__main__":
    main(sys.argv)
