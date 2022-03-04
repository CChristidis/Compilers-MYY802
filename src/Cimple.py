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


def printerror_lexical(err_msg: str, line: int):
    sys.exit("Lexical Error: " + err_msg + " Line: " + str(line))


def printerror_parser(err_msg: str, nterminal_symbol: str, line: int):
    sys.exit("Syntax Error: " + err_msg + " Non-terminal symbol: " + nterminal_symbol + ". Line: " + str(line))


def check_int_overflow(intg_lst) -> bool:
    strint = [str(intg) for intg in intg_lst]
    joined_string = "".join(strint)
    joined_int = int(joined_string)

    return abs(joined_int) > 2 ** 32 - 1


def is_blank(tk: str) -> bool:
    return tk.isspace() or '\n' in tk


def acceptable_varname(tk: str) -> bool:
    return tk[0].isalpha() and tk.isalnum()


class LexAutomaton:
    def __init__(self, fd):
        self.stateid = 0
        self.token = []
        self.fd = fd


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
                    printerror_lexical("End of program reached, without the mandatory '.'.", linenum)
                elif is_blank(curr):
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
                    if check_int_overflow(token):
                        printerror_lexical("integer overflow.", linenum)

                elif curr.isalpha():
                    printerror_lexical("variable assignment at '" + "".join(token) +
                                       " 'ended erroneously. Must exclusively include digits.", linenum)

                elif is_blank(curr):
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

                elif is_blank(curr):
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

                elif is_blank(curr):
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
                    if is_blank(curr) is False:
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


# TODO: Create a function for every non-terminal symbol of Cimple's grammar, as shown in prof's notes.
def parser():
    global token
    token = lexical()
    program()


def program():
    global token

    if token == "program":
        token = lexical()  # program's ID (name)
        if not acceptable_varname(token):
            printerror_parser("program's name must be an alphanumeric sequence, mandatorily starting with a letter.",
                              "program", linenum)
        block()
    else:
        printerror_parser("illegal start of program's syntax.", "program", linenum)


def block():
    global token

    token = lexical()
    if token == "{":
        declarations()
        subprograms()
        """ don't call lexical at the beginning of blockstatements!"""
        # blockstatements()
    else:
        printerror_parser("'{' expected before block, not found.", "block", linenum)


def declarations():
    """ we can opt not to declare any variable whatsoever. """
    global token

    token = lexical()
    print(token)
    while token == "declare":       # Kleene star implementation for "declare" non-terminal
        varlist()
        token = lexical()
        print(token)


def varlist():
    global token

    token = lexical()  # variable's ID
    print(token)

    if not acceptable_varname(token):
        printerror_parser("variable's identifier must be an alphanumeric sequence, mandatorily starting with a letter.",
                          "varlist", linenum)

    token = lexical()  # comma or semicolon
    print(token)

    if token not in (',', ';'):
        printerror_parser("illegal variable declaration syntax.", "varlist", linenum)

    if token == ';':
        return

    while True:
        token = lexical()  # variable's ID
        print(token)
        if not acceptable_varname(token):
            printerror_parser("variable's identifier must be an alphanumeric sequence, "
                              "mandatorily starting with a letter.", "varlist", linenum)
        token = lexical()  # comma or semicolon
        if token not in (',', ';'):
            printerror_parser("illegal variable declaration syntax.", "varlist", linenum)
        if token == ';':
            break


def subprograms():
    subprogram()


def subprogram():
    global token
    # token = lexical(). already have 1 token from declarations

    while token in ("function", "procedure"):
        token = lexical()  # subprogram's ID
        print(token)
        if not acceptable_varname(token):
            printerror_parser("subprogram's identifier must be an alphanumeric sequence, "
                              "mandatorily starting with a letter.", "subprogram", linenum)

        token = lexical()  # (
        print(token)
        if token != '(':
            printerror_parser("'(' expected before formal parameters declaration, not found.", "subprogram", linenum)

        parlist("formal")  # ends with ')'

        block()
        #token = lexical()  # for blockstatements()



# TODO: statements() , blockstatements() after implementing statement()
def statements():
    global token

    token = lexical()

    if token != ';':
        statement()

    else:
        token = lexical()  # semicolon
        if token != ';':
            printerror_parser("';' expected, not found.", "statements", linenum)


def statement():
    global token
    # already have 1 unused token from statements()

    # leave assignStat last
    if token == "if":
        # ifStat() and elsepart()
    elif token == "while":
        # whileStat()
    elif token == "switchcase":
        # switchcaseStat()
    elif token == "forcase":
        # forcaseStat()
    elif token == "incase":
        # incaseStat()
    elif token == "return":
        # returnStat()
    elif token == "call":
        # callStat()
    elif token == "input":
        # inputStat()
    elif token == "print":
        # printStat()
    else:  # assignStat case
        if not acceptable_varname(token):
            printerror_parser("parameter's identifier must be an alphanumeric sequence, "
                              "mandatorily starting with a letter.", "statement", linenum)
        token = lexical()  # :=
        if token != ":=":
            printerror_parser("assignment syntax is incorrect.", "statement", linenum)

        expression()


def expression():  # after expression() we have 1 token left.
    global token

    token = lexical()

    if token in ('+', '-'):  # optionalSign
        token = lexical()
        term()

    term()
    token = lexical()
    while token in ('+', '-'):  # Kleene star
        term()
        token = lexical()

def term():
    global token
    # already have one unused token before calling term()
    factor()

    token = lexical()
    while token in ('*', '/'):  # MUL_OP
        factor()




def factor():
    global token
    # already have one unused token before calling factor()
    if isinstance(token, int):  # INTEGER
        return  # terminal symbol

    elif token == '(':
        expression()
        token = lexical()  # ')'

        if token != ')':
            printerror_parser("')' expected, not found.", "factor", linenum)

    else:  # variable or subprogram case
        if not acceptable_varname(token):
            printerror_parser("parameter's or subprogram's identifier must be an alphanumeric sequence, "
                              "mandatorily starting with a letter.", "factor", linenum)
        idtail()


def idtail():
    global token

    token = lexical()

    if token == '(':
        parlist("actual")
        if token != ')':
            printerror_parser("')' expected, not found.", "idtail", linenum)



def parlist(arg_type):
    global token

    token = lexical()
    print(token)

    while True:
        if token == ')':
            return

        if arg_type == "actual":
            paritem(arg_type)

        elif arg_type == "formal":
            paritem(arg_type)

        """
         suppose we have a declaration example (in a, in b, ). Comma followed by closed parenthesis is not valid.
         """
        if token == ',':
            token = lexical()
            if not acceptable_varname(token):
                printerror_parser("invalid token after ',' while declaring formal parameters.", arg_type + "parlist",
                                  linenum)


def paritem(arg_type):
    global token

    if token not in ('in', 'inout'):
        printerror_parser("illegal formal parameter declaration syntax. Specify evaluation strategy.", arg_type+"paritem",
                          linenum)

    if arg_type == "actual" and token == "in":
        expression()

    token = lexical()  # parameter's ID
    print(token)

    if not acceptable_varname(token):
        printerror_parser("parameter's identifier must be an alphanumeric sequence, "
                          "mandatorily starting with a letter.", arg_type+"paritem", linenum)

    token = lexical()  # comma or closing parenthesis
    print(token)

    if token not in (')', ','):
        printerror_parser("illegal formal parameter declaration syntax, no ')' or ',' found.", arg_type+"paritem", linenum)














def check_file(path: str) -> bool:
    return path[-3:] == ".ci"


def get_extn(file: str) -> str:
    idx = file.find('.')
    return file[idx:]


def main(argv):
    input_file = argv[1]

    """ check if file has .ci extension. check_file function. """
    if not check_file(input_file):
        sys.exit("File extension '" + get_extn(input_file) + "' not acceptable.")

    openfile(input_file)
    parser()



if __name__ == "__main__":
    main(sys.argv)



