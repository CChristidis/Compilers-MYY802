# Xrhstos Xristidhs, 4526, cse84526
import sys

"""Global variables"""
linenum = 1
token = ''
fd = ''


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
    return tk.isspace() or tk == '\n'


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
                    if curr == '\n':
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
    token = ("".join(token)).replace(" ", "")
    return token



def parser():
    global token
    token = lexical()
    program()


def program():
    global token

    if token == "program":
        token = lexical()  # program's ID (name)
        print("Program '" + token + "' has started.")
        if not acceptable_varname(token):
            printerror_parser("program's name must be an alphanumeric sequence, mandatorily starting with a letter.",
                              "program", linenum)
        token = lexical()
        block()
        print("Syntax analysis ended successfully.")

    else:
        printerror_parser("illegal start of program's syntax.", "program", linenum)


def block():
    global token

    if token == "{":
        token = lexical()
        declarations()
        subprograms()
        blockstatements()
        if token != '}':
            printerror_parser("'}' expected, not found.", "block", linenum)
        token = lexical()

    else:
        printerror_parser("'{' expected before block, not found.", "block", linenum)


def declarations():
    """ we can opt not to declare any variable whatsoever. """
    global token

    while token == "declare":       # Kleene star implementation for "declare" non-terminal
        token = lexical()
        varlist()
        token = lexical()


def varlist():
    global token

    if not acceptable_varname(token):
        printerror_parser("variable's identifier must be an alphanumeric sequence, "
                          "mandatorily starting with a letter.", "varlist", linenum)

    token = lexical()  # comma

    while token != ';':  # can leave only and only if token == ';'
        token = lexical()  # variable's id
        if not acceptable_varname(token):
            printerror_parser("variable's identifier must be an alphanumeric sequence, "
                              "mandatorily starting with a letter.", "varlist", linenum)
        token = lexical()


def subprograms():
    subprogram()



def subprogram():
    # TODO: edw tha paixtei mpalitsa sth 2h fash, exe to katharo
    global token

    while token in ("function", "procedure"):
        token = lexical()  # subprogram's ID  (e.g. isPrime)
        if not acceptable_varname(token):
            printerror_parser("subprogram's identifier must be an alphanumeric sequence, "
                              "mandatorily starting with a letter.", "subprogram", linenum)

        token = lexical()  # (
        if token != '(':
            printerror_parser("'(' expected before formal parameters declaration, not found.", "subprogram", linenum)

        parlist("formal")  # ends with ')'

        block()



def parlist(arg_type):
    global token

    token = lexical()

    if arg_type == "actual":
        actualparitem()

    elif arg_type == "formal":
        formalparitem()

    while token == ',':
        token = lexical()
        if arg_type == "actual":
            actualparitem()

        elif arg_type == "formal":
            formalparitem()
    if token != ')':
        printerror_parser("')' expected, not found.", "statements", linenum)

    token = lexical()



def actualparitem():
    global token

    if token not in ('in', 'inout'):
        printerror_parser("illegal actual parameter declaration syntax. Specify evaluation strategy.", "actualparitem",
                          linenum)

    if token == "in":
        token = lexical()
        expression()

    elif token == "inout":
        token = lexical()  # parameter's ID
        if not acceptable_varname(token):
            printerror_parser("parameter's identifier must be an alphanumeric sequence, "
                              "mandatorily starting with a letter.", "actualparitem", linenum)

        token = lexical()  # comma or closing parenthesis


def formalparitem():
    global token

    if token not in ('in', 'inout'):
        printerror_parser("illegal formal parameter declaration syntax. Specify evaluation strategy.", "formalparitem",
                          linenum)
    token = lexical()  # parameter's ID

    if not acceptable_varname(token):
        printerror_parser("parameter's identifier must be an alphanumeric sequence, "
                          "mandatorily starting with a letter.", "formalparitem", linenum)

    token = lexical()  # comma or closing parenthesis

    if token not in (')', ','):

        printerror_parser("illegal formal parameter declaration syntax, no ')' or ',' found.", "formalparitem", linenum)



def statements():  # no unused token
    global token

    if token != ';':  # TODO
        if token != '{':
            statement()
            if token != ';':
                printerror_parser("';' expected, not found.", "statements", linenum)
            token = lexical()

        elif token == '{':
            token = lexical()
            blockstatements()

            if token != '}':
                printerror_parser("'}' expected, not found.", "statements", linenum)

            token = lexical()
        else:
            printerror_parser("'{' expected, not found.", "statements", linenum)




def blockstatements():  # 1 unused token
    global token

    statement()

    while token == ';':
        token = lexical()
        statement()


def statement():
    global token
    # already have 1 unused token from statements() or blockstatements()
    # after statement we necessarily NEED 1 left token
    # leave assignStat last
    if token == "if":  # ok
        if_whileStat("if")
    elif token == "while":  # ok
        if_whileStat("while")
    elif token == "switchcase":
        switch_in_for_caseStat("switchcase")
    elif token == "forcase":
        switch_in_for_caseStat("forcase")
    elif token == "incase":
        switch_in_for_caseStat("incase")
    elif token == "return":  # ok
        return_printStat("return")
    elif token == "call":
        callStat()
    elif token == "input":
        inputStat()
    elif token == "print":  # ok
        return_printStat("print")
    elif token.isalnum():  # assignStat case # ok
        if not acceptable_varname(token):
            printerror_parser("parameter's identifier must be an alphanumeric sequence, "
                              "mandatorily starting with a letter.", "statement", linenum)
        token = lexical()  # :=
        if token != ":=":
            printerror_parser("assignment syntax is incorrect.", "statement", linenum)

        token = lexical()
        expression()


def inputStat():
    global token

    token = lexical()

    if token != '(':
        printerror_parser("'(' expected, not found.", "inputStat", linenum)

    token = lexical()  # ID
    if not acceptable_varname(token):
        printerror_parser("variable's identifier must be an alphanumeric sequence, "
                          "mandatorily starting with a letter.", "inputStat", linenum)

    token = lexical()  # )
    if token != ')':
        printerror_parser("')' expected, not found.", "inputStat", linenum)

    token = lexical()  # extra



def callStat():
    global token

    token = lexical()

    if not acceptable_varname(token):
        printerror_parser("subprogram's identifier must be an alphanumeric sequence, "
                          "mandatorily starting with a letter.", "callStat", linenum)

    token = lexical()  # (
    if token != '(':
        printerror_parser("'(' expected, not found.", "callStat", linenum)

    parlist("actual")  # TODO: I THINK that parlist retain an unused token so no need for an extra one, investigate

    # if token != ')':
        # printerror_parser("')' expected, not found.", "callStat", linenum)


def return_printStat(typ):
    global token

    token = lexical()

    if token != '(':
        printerror_parser("'(' expected, not found.", typ + "Stat", linenum)

    token = lexical()

    expression()

    if token != ')':
        printerror_parser("')' expected, not found.", typ + "Stat", linenum)

    token = lexical()  # extra


def if_whileStat(conditional):  # 1 unused token
    global token

    token = lexical()

    if token != '(':
        printerror_parser("'(' expected, not found.", conditional + "Stat", linenum)

    token = lexical()

    condition()

    if token != ')':
        printerror_parser("')' expected, not found.", conditional , linenum)

    token = lexical()

    statements()

    if conditional == "if":
        elsepart()


def elsepart():  # 1 unused token
    global token

    # already has 1 token from statements()

    if token == "else":
        token = lexical()
        statements()


def switch_in_for_caseStat(selection_control):
    global token

    token = lexical()

    while token == "case":
        token = lexical()  # '('
        if token != '(':
            printerror_parser("'(' expected, not found.", selection_control + "Stat", linenum)

        token = lexical()
        condition()
        if token != ')':
            printerror_parser("')' keyword expected, not found.", selection_control + "Stat", linenum)
        token = lexical()
        statements()

    if token != "default" and selection_control in ("switchcase", "forcase"):
        printerror_parser("'default' keyword expected, not found.", selection_control + "Stat", linenum)

    if selection_control in ("switchcase", "forcase"):
        token = lexical()
        statements()


def condition():    # 1 unused token after
    global token

    boolterm()

    while token == "or":
        token = lexical()
        boolterm()


def boolterm():     # 1 unused token after
    global token
    boolfactor()    #  and boolfactor()...

    while token == "and":
        token = lexical()
        boolfactor()


def boolfactor():   # 1 unused token after
    global token

    if token == "not":
        token = lexical()
        if token != '[':
            printerror_parser("'[' expected, not found.", "boolfactor", linenum)
        token = lexical()
        condition()
        if token != ']':
            printerror_parser("']' expected, not found.", "boolfactor", linenum)
        token = lexical()  # for boolterm

    elif token == "[":
        token = lexical()
        condition()
        if token != ']':
            printerror_parser("']' expected, not found.", "boolfactor", linenum)
        token = lexical()  # for boolterm

    else:
        expression()

        if token not in ('=', '<=', '>=', '>', '<', '<>'):
            printerror_parser("relational operator expected, not found.", "boolfactor", linenum)
        token = lexical()
        expression()


def expression():  # after expression we have 1 token left.
                   # needs 1 token before entering
    global token

    if token in ('+', '-'):  # optionalSign
        token = lexical()

    term()

    while token in ('+', '-'):  # Kleene star
        token = lexical()
        term()


def term():
    global token
    # after term we have 1 token left.
    # already have one unused token before calling term()
    factor()

    while token in ('*', '/'):  # MUL_OP
        token = lexical()
        factor()


def factor():
    global token

    # already have one unused token before calling factor()
    # 1 token left after factor return

    if token.isdigit():  # INTEGER
        token = lexical()
        return  # terminal symbol

    elif token == '(':
        token = lexical()
        expression()
        if token != ')':
            printerror_parser("')' expected, not found.", "factor", linenum)
        token = lexical()

    else:  # variable or subprogram case
        if not acceptable_varname(token):
            printerror_parser("parameter's or subprogram's identifier must be an alphanumeric sequence, "
                              "mandatorily starting with a letter.", "factor", linenum)
        token = lexical()  # if you find relational goto boolfactor
        idtail()


def idtail():
    global token

    if token == '(':
        parlist("actual")

        #token = lexical()
        #print(token + " idtail2")


def check_file(path: str) -> bool:
    return path[-3:] == ".ci"


def get_extn(file: str) -> str:
    idx = file.rindex('.')
    return file[idx:]


if __name__ == "__main__":
    input_file = sys.argv[1]

    """ check if file has .ci extension. check_file function. """
    if not check_file(input_file):
        sys.exit("File extension '" + get_extn(input_file) + "' not acceptable.")

    openfile(input_file)
    parser()


