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






def lex():
    #TODO: len(varname) <= 30
    print("")
