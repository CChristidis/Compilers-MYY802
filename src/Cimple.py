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





def openfile(path: str):
    global fd

    try:
        fd = open(path, 'r')

    except IOError:
        sys.exit("Error: File" + path + " does not appear to exist.")


def perror_lexical(err_msg: str):
    sys.exit(err_msg)


def lexical() -> int:
    """potential keyword list."""
    token = []
    """
        state board:
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
    stateid = 0
    status = False                          # non-final state

    while status is False:
        curr = fd.read(1)
        token.append(curr)  # push current char into stack
        if stateid == 0:
            if len(token) > 30:
                perror_lexical("Token buffer exceeded the maximum length of 30 characters")

            if curr.isalpha():
                stateid = 1                   # goto: check for alphanumeric
            elif curr.isdigit():
                stateid = 2                   # goto: final
            elif curr in ('+', '-', '*', '/', '=', '(', ')', ';', '[', ']', ',', '{', '}'):
                stateid = 3
            elif curr == '<':
                stateid = 4
            elif curr == '>':
                stateid = 5
            elif curr == ':':
                stateid = 6
            elif curr == '#':
                stateid = 7
            elif curr == '':
                stateid = 8                   # EOF
            elif curr.isspace():
                continue                    # blank character, ignore
            else:
                perror_lexical("Unrecognizable token " + '"' + curr + '".')            # error state

        if stateid == 1:
            while curr.isalnum():
                curr = fd.read(1)
                token.append(curr)

            if curr.isspace():
                """ ------------------------------ FINAL ------------------------------ """
                status = True               # EOF or end of identifier sequence
                """ ------------------------------ FINAL ------------------------------ """
            else:
                perror_lexical("Invalid variable identifier '" + "".join(token) +
                               "'. Must include exclusively numbers or letters.")

        if stateid == 2:
            while curr.isdigit():
                curr = fd.read(1)
                token.append(curr)

            if curr.isdigit() is False:
                if curr.isspace() is False:
                    perror_lexical("Variable assignment at '" + "".join(token) +
                                   "'ended erroneously. Must include exclusively digits.")
                else:
                    """ ------------------------------ FINAL ------------------------------ """
                    status = True            # EOF or end of digit sequence
                    """ ------------------------------ FINAL ------------------------------ """

        if stateid == 4:
            curr = fd.read(1)
            if curr in ('=', '>'):
                token.append(curr)
                status = True

            elif curr.isspace():
                status = True

            else:
                token.append(curr)
                perror_lexical("Unrecognizable token '" + "".join(token) + "'Did you mean '<=' or '<>'?")


def main(argv):
    input_file = argv[1]
    openfile(input_file)
    lexical()


if __name__ == "__main__":
    main(sys.argv)
