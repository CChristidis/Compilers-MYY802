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



def parser():
    global token
    token = lexical()
    print(token + " Start")
    program()


def program():
    global token

    if token == "program":
        token = lexical()  # program's ID (name)
        print(token + " program")
        if not acceptable_varname(token):
            printerror_parser("program's name must be an alphanumeric sequence, mandatorily starting with a letter.",
                              "program", linenum)
        block()

        token = lexical()  # program's end ('.')
        print(token + " program")
        if token != '.':
            printerror_parser("program's end with '.', not found.", "program", linenum)

    else:
        printerror_parser("illegal start of program's syntax.", "program", linenum)


def block():
    global token

    token = lexical()
    print(token + " block")
    if token == "{":
        declarations()
        subprograms()
        blockstatements()
        if token != '}':
            printerror_parser("'}' expected, not found.", "block", linenum)

    else:
        printerror_parser("'{' expected before block, not found.", "block", linenum)


def declarations():
    """ we can opt not to declare any variable whatsoever. """
    global token

    token = lexical()
    print(token + " declarations")
    while token == "declare":       # Kleene star implementation for "declare" non-terminal
        varlist()
        token = lexical()
        print(token + " declarations")


def varlist():
    global token

    token = lexical()  # variable's ID
    print(token + " varlist")

    if not acceptable_varname(token):
        printerror_parser("variable's identifier must be an alphanumeric sequence, mandatorily starting with a letter.",
                          "varlist", linenum)

    token = lexical()  # comma or semicolon
    print(token + " varlist")

    if token not in (',', ';'):
        printerror_parser("illegal variable declaration syntax.", "varlist", linenum)

    if token == ';':
        return

    while True:
        token = lexical()  # variable's ID
        print(token + " varlist")

        if not acceptable_varname(token):
            printerror_parser("variable's identifier must be an alphanumeric sequence, "
                              "mandatorily starting with a letter.", "varlist", linenum)
        token = lexical()  # comma or semicolon
        print(token + " varlist")
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
        print(token + " subprogram")
        if not acceptable_varname(token):
            printerror_parser("subprogram's identifier must be an alphanumeric sequence, "
                              "mandatorily starting with a letter.", "subprogram", linenum)

        token = lexical()  # (
        print(token + " subprogram")
        if token != '(':
            printerror_parser("'(' expected before formal parameters declaration, not found.", "subprogram", linenum)

        parlist("formal")  # ends with ')'

        block()


def statements():  # no unused token
    global token

    token = lexical()
    print(token + " statements")

    if token != ';':
        statement()
        if token != ';':
            printerror_parser("';' expected, not found.", "statements", linenum)

    else:
        token = lexical()  # semicolon
        print(token + " statements")
        if token != ';':
            printerror_parser("';' expected, not found.", "statements", linenum)

    token = lexical()  # '{'
    print(token + " statements")
    if token != '{':
        printerror_parser("'{' expected, not found.", "statements", linenum)

    token = lexical()
    print(token + " statements")
    statement()
    while token == ';':
        statement()

    if token != '}':
        printerror_parser("'}' expected, not found.", "statements", linenum)


def blockstatements():  # 1 unused token
    global token

    # token = lexical()
    # print(token + " blockstatements")

    statement()
    while token == ';':
        statement()


def statement():
    global token
    # already have 1 unused token from statements() or blockstatements()
    # after statement we necessarily need 1 left token

    # leave assignStat last
    if token == "if":
        if_whileStat("if")
    elif token == "while":
        if_whileStat("while")
    elif token == "switchcase":
        switch_in_for_caseStat("switchcase")
    elif token == "forcase":
        switch_in_for_caseStat("forcase")
    elif token == "incase":
        switch_in_for_caseStat("incase")
    elif token == "return":
        return_printStat("return")
    elif token == "call":
        callStat()
    elif token == "input":
        inputStat()
    elif token == "print":
        return_printStat("print")
    else:  # assignStat case
        if not acceptable_varname(token):
            print(token + " statement")
            printerror_parser("parameter's identifier must be an alphanumeric sequence, "
                              "mandatorily starting with a letter.", "statement", linenum)
        token = lexical()  # :=
        print(token + " statement")
        if token != ":=":
            printerror_parser("assignment syntax is incorrect.", "statement", linenum)

        token = lexical()
        print(token + " statement")
        expression()


def inputStat():
    global token

    token = lexical()  # (
    print(token + " inputStat")
    if token != '(':
        printerror_parser("'(' expected, not found.", "inputStat", linenum)

    token = lexical()  # ID
    print(token + " inputStat")
    if not acceptable_varname(token):
        printerror_parser("variable's identifier must be an alphanumeric sequence, "
                          "mandatorily starting with a letter.", "inputStat", linenum)

    token = lexical()  # )
    print(token + " inputStat")
    if token != ')':
        printerror_parser("')' expected, not found.", "inputStat", linenum)

    token = lexical()  # extra
    print(token + " inputStat(extra)")


def callStat():
    global token

    token = lexical()  # ID
    print(token + " callStat")

    if not acceptable_varname(token):
        printerror_parser("subprogram's identifier must be an alphanumeric sequence, "
                          "mandatorily starting with a letter.", "callStat", linenum)

    token = lexical()  # (
    print(token + " callStat")
    if token != '(':
        printerror_parser("'(' expected, not found.", "callStat", linenum)

    parlist("actual")  # TODO: I THINK that parlist doesn't retain an unused token, investigate

    token = lexical()  # )
    print(token + " callStat")
    if token != '(':
        printerror_parser("'(' expected, not found.", "callStat", linenum)

    token = lexical()  # extra
    print(token + " callStat(extra)")


def return_printStat(typ):
    global token

    token = lexical()  # '('
    print(token + " return_printStat")

    if token != '(':
        printerror_parser("'(' expected, not found.", typ + "Stat", linenum)

    token = lexical()
    print(token + " return_printStat")

    expression()

    if token != ')':
        printerror_parser("')' expected, not found.", typ + "Stat", linenum)


def if_whileStat(conditional):  # 1 unused token
    global token

    token = lexical()  # '('
    print(token + " if_whileStat")

    if token != '(':
        printerror_parser("'(' expected, not found.", conditional + "Stat", linenum)

    condition()

    if token != ')':
        printerror_parser("')' expected, not found.", conditional + "Stat", linenum)

    statements()

    if conditional == "if":
        elsepart()


def switch_in_for_caseStat(selection_control):
    global token

    token = lexical()  # 'case' or "default"
    print(token + " switch_in_for_caseStat")

    while token == "case":
        token = lexical()  # '('
        print(token + " switch_in_for_caseStat")
        if token != '(':
            printerror_parser("'(' expected, not found.", selection_control + "Stat", linenum)
        condition()
        if token != ')':
            printerror_parser("')' keyword expected, not found.", selection_control + "Stat", linenum)
        statements()
        token = lexical()
        print(token + " switch_in_for_caseStat")

    if token != "default" and selection_control in ("switchcase", "forcase"):
        printerror_parser("'default' keyword expected, not found.", selection_control + "Stat", linenum)

    if selection_control in ("switchcase", "forcase"):
        statements()

    token = lexical()  # extra
    print(token + " switch_in_for_caseStat")


def condition():    # 1 unused token after
    global token

    token = lexical() # "not" or '[' for boolfactor
    print(token + " condition")

    boolterm()      # or boolterm()...

    while token == "or":
        boolterm()


def boolterm():     # 1 unused token after
    boolfactor()    #  and boolfactor()...

    while token == "and":
        boolfactor()


def boolfactor():   # 1 unused token after
    global token

    if token == "not":
        token = lexical()
        print(token + " boolfactor")
        if token != '[':
            printerror_parser("'[' expected, not found.", "boolfactor", linenum)

        condition()
        if token != ']':
            printerror_parser("']' expected, not found.", "boolfactor", linenum)
        token = lexical()  # for boolterm
        print(token + " boolfactor")

    elif token == "[":
        condition()
        if token != ']':
            printerror_parser("']' expected, not found.", "boolfactor", linenum)
        token = lexical()  # for boolterm
        print(token + " boolfactor")

    else:
        expression()
        token = lexical()  # tst
        if token not in ('=', '<=', '>=', '>', '<', '<>'):
            printerror_parser("relational oparator expected, not found.", "boolfactor", linenum)
        token = lexical()
        print(token + " boolfactor")
        expression()


def elsepart():  # 1 unused token
    global token

    token = lexical()
    print(token + " elsepart")

    if token == "else":
        statements()
        token = lexical()
        print(token + " elsepart")


def expression():  # after expression we have 1 token left.
                   # needs 1 token before entering
    global token

    if token in ('+', '-'):  # optionalSign
        token = lexical()
        print(token + " expression")

    term()
    token = lexical()
    print(token + " expression")
    while token in ('+', '-'):  # Kleene star
        term()


def term():
    global token
    # after term we have 1 token left.
    # already have one unused token before calling term()
    factor()

    token = lexical()
    print(token + " term")
    while token in ('*', '/'):  # MUL_OP
        factor()
        token = lexical()
        print(token + " term")


def factor():
    global token
    # already have one unused token before calling factor()
    # no token left after factor return
    if isinstance(token, int):  # INTEGER
        return  # terminal symbol

    elif token == '(':
        token = lexical()
        print(token + " factor")
        expression()
        token = lexical()  # ')'
        print(token + " factor")

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
    print(token + " idtail")

    if token == '(':
        parlist("actual")
        if token != ')':
            printerror_parser("')' expected, not found.", "idtail", linenum)


def parlist(arg_type):
    global token

    token = lexical()
    print(token + " parlist")

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
            print(token + " parlist")
            if not acceptable_varname(token):
                printerror_parser("invalid token after ',' while declaring formal parameters.", arg_type + "parlist",
                                  linenum)


def paritem(arg_type):
    global token

    if token not in ('in', 'inout'):
        printerror_parser("illegal formal parameter declaration syntax. Specify evaluation strategy.", arg_type+"paritem",
                          linenum)

    if arg_type == "actual" and token == "in":
        token = lexical()
        print(token + " paritem")
        expression()

    token = lexical()  # parameter's ID
    print(token + " paritem")

    if not acceptable_varname(token):
        printerror_parser("parameter's identifier must be an alphanumeric sequence, "
                          "mandatorily starting with a letter.", arg_type+"paritem", linenum)

    token = lexical()  # comma or closing parenthesis
    print(token + " paritem")

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
    # lexical()


if __name__ == "__main__":
    main(sys.argv)



