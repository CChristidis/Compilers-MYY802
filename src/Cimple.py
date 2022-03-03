# Xrhstos Xristidhs 4526
from enum import Enum
import sys

"""Global variables"""
linenum = 1
token = ''


def openfile(path: str):
    global fd

    try:
        fd = open(path, 'r')

    except IOError:
        sys.exit("Error: File" + path + " does not appear to exist.")


def printerror_lexical(err_msg: str, line):
    sys.exit("Lexical Error: " + err_msg + " Line: " + str(line))


def printerror_parser(err_msg: str, nterminal_symbol):
    sys.exit("Syntax Error: " + err_msg + " Non-terminal symbol: " + nterminal_symbol)


class LexAutomaton:
    def __init__(self, fd):
        self.stateid = 0
        self.token = []
        self.fd = fd

    @staticmethod
    def check_int_overflow(self, intg_lst) -> bool:
        strint = [str(intg) for intg in intg_lst]
        joined_string = "".join(strint)
        joined_int = int(joined_string)

        return abs(joined_int) > 2 ** 32 - 1

    def automaton(self):
        global linenum
        eof = ''
        """potential keyword list."""
        token = self.token
        stateid = self.stateid
        fd = self.fd
        """
            state board:
                0: default state / blank-character-as-input state
                1: alphabet state
                2: digit state
                3: less-than sign state (<) 
                4: greater-than sign state (>)
                5: colon state (:)
                6: comment state (#)
        """

        status = False  # non-final state

        while status is False:
            curr = fd.read(1)
            token.append(curr)  # push current char into stack
            if stateid == 0:
                if curr.isalpha():
                    stateid = 1
                elif curr.isdigit():
                    stateid = 2
                elif curr in ('+', '-', '*', '/', '=', '(', ')', ';', '[', ']', ',', '{', '}', '.'):
                    # keep in mind that '.' signals the end of the program.
                    return token
                elif curr == '<':
                    stateid = 3
                elif curr == '>':
                    stateid = 4
                elif curr == ':':
                    stateid = 5
                elif curr == '#':   # in this state we need to find another '#' symbol, before a potential eof occurs.
                    first = 1
                    stateid = 6
                elif curr == eof:
                    return 'eof'
                elif curr.isspace() or '\n' in curr:
                    if '\n' in curr:
                        linenum += 1
                    token.pop()
                    continue  # blank character, ignore
                else:
                    printerror_lexical("unrecognizable token " + '"' + curr + '".', linenum)  # error state

            if stateid == 1:
                if curr.isalnum():
                    if len(token) > 30:
                        printerror_lexical("token buffer exceeded maximum length of 30 characters.", linenum)

                else:
                    fd.seek(fd.tell() - 1)  # go back 1 character.
                    token.pop()
                    status = True

            if stateid == 2:
                if curr.isdigit():
                    if self.check_int_overflow(self, token):
                        printerror_lexical("integer overflow.", linenum)

                elif curr.isalpha():
                    printerror_lexical("variable assignment at '" + "".join(token) +
                                       " 'ended erroneously. Must exclusively include digits.", linenum)

                elif curr.isspace() or '\n' in curr:
                    if '\n' in curr:
                        linenum += 1
                        token.pop()
                    status = True

                else:
                    fd.seek(fd.tell() - 1)  # go back 1 character.
                    token.pop()
                    status = True

            if stateid == 3:
                curr = fd.read(1)
                if curr in ('=', '>'):
                    token.append(curr)
                    status = True

                elif curr.isspace() or '\n' in curr:
                    if '\n' in curr:
                        linenum += 1
                    status = True

                else:
                    fd.seek(fd.tell() - 1)  # go back 1 character.
                    status = True

            if stateid == 4:
                curr = fd.read(1)
                if curr == '=':
                    token.append(curr)
                    status = True

                elif curr.isspace() or '\n' in curr:
                    if '\n' in curr:
                        linenum += 1
                    status = True

                else:
                    fd.seek(fd.tell() - 1)  # go back 1 character.
                    status = True

            if stateid == 5:
                curr = fd.read(1)
                if curr == '=':
                    token.append(curr)
                    status = True
                else:
                    if curr.isspace() and '\n' in curr is False:
                        token.append(curr)
                    printerror_lexical("unrecognizable token '" + "".join(token) + "'Do you mean ':=' ?", linenum)

            if stateid == 6:
                if first == 1:
                    if curr == eof:
                        printerror_lexical("unclosed comment.", linenum)
                    first = 0
                else:
                    if curr == eof:
                        printerror_lexical("unclosed comment.", linenum)
                    elif curr == '#':
                        stateid = 0  # comments have no further use in syntactical analysis
                        token = []


        return token


def lexical():
    aut = LexAutomaton(fd)
    token = aut.automaton()
    return "".join(token)

# TODO: Create a method for every non-terminal symbol of Cimple's grammar, as shown in prof's notes.
def parser():
    global token
    token = lexical()
    program()


def program():
    global token

    if token == "program":
        token = lexical()  # program's ID (name)
        if not (token[0].isalpha() and token.isalnum()):
            printerror_parser("program's name must be an alphanumeric sequence, mandatorily starting with a letter.",
                              "program")
        block()
    else:
        printerror_parser("unexpected beginning of program's syntax.", "program")


def block():
    global token

    token = lexical()
    if token == "{":
        declarations()
        # subprograms()
        # blockstatements()
    else:
        printerror_parser("'{' expected before block, not found.", "block")


def declarations():
    global token

    token = lexical()
    if token == "declare":
        pass
        # TODO: PAME XRHSTARA

    """ we can opt not to declare any variable. """


def check_file(path) -> bool:
    return path[-3:] == ".ci"


def main(argv):
    input_file = argv[1]

    """ check if file has .ci extension. check_file function. """
    # if not check_file(input_file):
        # sys.exit("File extension not acceptable.")

    openfile(input_file)
    parser()


if __name__ == "__main__":
    main(sys.argv)


"""
def is_blank(tk: str) -> bool:
    return tk.isspace() or tk == '' or '\n' in tk
"""
