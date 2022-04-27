# Xrhstos Xristidhs, 4526, cse84526
import sys
import os

program_name = ""

""" Lexical and syntax analysis globals:"""
linenum = 1
token = ''
fd = ''

""" Intermediary code globals: """
# for test set label = 99
label = 1
temp_var_num = 1  # temporary variable counter.
all_quads = {}
main_program_declared_vars = []

##### testing #####

symbol_table = []
offset = 12

""" activation record layout (numbered in indices): """
# 0-th index: subprogram's return address. Size: 4 bytes
# 1-st index: access link (It refers to information stored in other activation records that is non-local.). Size: 4 bytes
# 2-nd index: function's return value or None if subrpogram is a procedure. Size: 4 bytes
# 3-rd index: function's parameter. Size: 4 bytes
# ..........: function's parameter. Size: 4 bytes
# .
# .
# (4 + n - 1)-th index: function's local variable. Size: 4 bytes
# ..........: function's local variable. Size: 4 bytes
# .
# .
# (4 + n - 1 + k - 1)-th index: function's temporary variable. Size: 4 bytes
# ..........: function's temporary variable. Size: 4 bytes
# .
# .
# Activation record's length = (4 + 4 + 4) + 4 * (n + k + m) = 12 +  4 * (n + k + m) bytes
# First function's parameter can possibly start at offset 12.

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


####################### INTERMEDIATE CODE FUNCTIONS AND CLASSES(start) #######################

# temporary variables are used for: 1) storing subprogram's return value
#                                   2) intermediary result storage
def newTemp():
    # T_1, T_2, ..., T_n
    global temp_var_num
    new_temp = "T_" + str(temp_var_num)
    temp_var_num += 1

    return new_temp


def nextQuad():
    return label


def genQuad(op, oprnd1, oprnd2, target):
    global label, all_quads

    quad = Quad(op, oprnd1, oprnd2, target)

    all_quads[quad] = label
    #print(str(label) + ": " + str(quad))

    label += 1


def emptyList():
    return []


def makeList(label):
    return [label]


def mergeList(list1, list2):
    return list1 + list2


# assigns label to target field of quads with label in list
def backpatch(list, label):
    global all_quads

    for q, q_label in all_quads.items():
        if q_label in list:
            q.target = label  # set q's 4th field to label
            #print("------------------CHANGED-------------------")
            #print(str(q_label) + ": " + str(q))
            #print("------------------CHANGED-------------------")


class Quad():
    def __init__(self, op, oprnd1, oprnd2, target):
        self.op = op
        self.oprnd1 = oprnd1
        self.oprnd2 = oprnd2
        self.target = target

    def __str__(self):
        return (str(self.op) + ", " + str(self.oprnd1) + ", " + str(self.oprnd2) + ", " + str(self.target))

####################### INTERMEDIATE CODE FUNCTIONS AND CLASSES (end) #######################


####################### FILE CREATOR FUNCTIONS AND CLASSES (start) #######################


class ExceptionHandler(object):
    class Break(Exception):
      """Break out of the with statement"""


    def __init__(self, value):
        self.value = value

    def __enter__(self):
        return self.value

    def __exit__(self, etype, value, traceback):
        error = self.value.__exit__(etype, value, traceback)
        if etype == self.Break:
            print('Nested supbrogram or subrpogram call found. Aborting c file creation.')
            return True
        return error




def declared_vars_to_c(declared_vars_list: list) -> str:
    declared_vars_list_to_c = [el + ", " for el in declared_vars_list]
    temp_vars_list = ["T_" + str(i) + ", " if i < temp_var_num - 1 else "T_" + str(i) + ";" for i in range(1, temp_var_num)]
    merged_vars_list = mergeList(declared_vars_list_to_c, temp_vars_list)
    merged_vars_list.insert(0, "int ")

    return "".join(merged_vars_list)

def create_c_file():
    has_nests = False

    math_ops = ('+', '-', '*', '/')
    c_line_end = "; \n"
    if_str_start = "if ("
    if_str_end = ") goto "

    with ExceptionHandler(open('test.c', 'w', encoding='utf-8')) as c_file:
        c_file.write("# include <stdio.h> \n \n")
        c_file.write("int main(int argc, char **argv) { \n")


        for q, q_label in all_quads.items():
            q_label = str(q_label)
            label_str = "\t L_" + q_label + ": "

            if q.op == "begin_block" and q.oprnd1 == program_name:
                c_file.write("\t" + declared_vars_to_c(main_program_declared_vars) + "\n")
                c_file.write(label_str + "\n")
                continue

            elif q.op == "begin_block" and q.oprnd1 != program_name or q.op == "call":
                has_nests = True
                raise ExceptionHandler.Break

            elif q.op == "halt":
                c_file.write(label_str + "{}" + "\n")

            elif q.op == "end_block":
                c_file.write("}")
                break

            elif q.op in math_ops:
                c_file.write(label_str + q.target + " = " + str(q.oprnd1) + " " + q.op + " " + str(q.oprnd2) +
                             c_line_end)

            elif q.op == ":=":
                c_file.write(label_str + q.target + " = " + str(q.oprnd1) + c_line_end)

            elif q.op == "=":
                c_file.write(label_str + if_str_start + q.oprnd1 + " == " + q.oprnd2 + if_str_end + "L_" +
                             str(q.target) + c_line_end)

            elif q.op == "<>":
                c_file.write(label_str + if_str_start + q.oprnd1 + " != " + q.oprnd2 + if_str_end + "L_" +
                             str(q.target) + c_line_end)

            elif q.op in (">=", "<=", ">", "<"):
                c_file.write(label_str + if_str_start + q.oprnd1 + " " + q.op + " " + q.oprnd2 + if_str_end + "L_" +
                             str(q.target) + c_line_end)

            elif q.op == "jump":
                c_file.write(label_str + "goto " + "L_" + str(q.target) + c_line_end)

            elif q.op == "ret":
                c_file.write(label_str + "return " + str(q.oprnd1) + c_line_end)

            elif q.op == "in":
                c_file.write(label_str + 'scanf("%i", &'+ q.oprnd1 + ')' + c_line_end)

            elif q.op == "out":
                print_str = "printf(\"%i" + " \\" + 'n' + "\", "
                c_file.write(label_str + print_str + q.oprnd1 + ')' + c_line_end)

    if has_nests:
        os.remove("test.c")


def create_int_file():
    with open('test.int', 'w', encoding='utf-8') as int_code_file:
        for q, q_label in all_quads.items():
            int_code_file.write(str(q_label) + ": " + str(q) + '\n')

####################### FILE CREATOR FUNCTIONS AND CLASSES (end) #######################

####################### SYMBOL TABLE FUNCTIONS AND CLASSES (start) #######################


# Every instantiation of this class is created and inserted into the symbol table at the start of
# the corresponding subprogram. Νevertheless, its fields are evaluated when they are created inside
# the code.


class Entity:
    def __init__(self, name: str):
        self.name = name


class Variable(Entity):
    def __init__(self, name: str, datatype, offset: int):
        super().__init__(name)                      # variable's ID
        self.datatype = datatype                    # variable's data type
        self.offset = offset                        # distance from stack's head = 4 * len


class TemporaryVariable(Variable):
    def __init__(self, name: str, datatype, offset: int):
        super().__init__(name, datatype, offset)



class Subprogram(Entity):
    def __init__(self, name: str, startingQuad, formalParameters: list, framelength: int):
        super().__init__(name)                      # subprogram's ID
        self.startingQuad = startingQuad            # subprogram's first quad
        self.formalParameters = formalParameters    # list containing a subprogram's formal parameters
        self.framelength = framelength              # activation record's length in bytes


class Procedure(Subprogram):
        def __init__(self, name: str, startingQuad, formalParameters: list, framelength: int):
            super().__init__(name, startingQuad, formalParameters, framelength)

        def __str__(self):
            return (str(self.name) + ", " + str(self.startingQuad) + ", "  + str(self.framelength))

class Function(Subprogram):
        def __init__(self, name: str, startingQuad, datatype, formalParameters: list, framelength: int):
            super().__init__(name, startingQuad, formalParameters, framelength)
            self.datatype = datatype

        def __str__(self):
            return (str(self.name) + ", " + str(self.startingQuad) + ", " + str(self.datatype) + ", " + str(self.framelength))


class FormalParameter(Entity):
    def __init__(self, name: str, datatype, mode: str):
        super().__init__(name)
        self.datatype = datatype
        self.mode = mode

    def __str__(self):
        return (str(self.name) + ", " + str(self.datatype) + ", " + str(self.mode))


class Parameter(FormalParameter):
        def __init__(self, name: str, datatype, mode: str, offset: int):
            super().__init__(name, datatype, mode)  # parameter's ID
            self.offset = offset


class SymbolicConstant(Entity):
    def __init__(self, name: str, datatype, value):
        super().__init__(name)
        self.datatype = datatype
        self.value = value






def addRecordToCurrentLevel(record):
    global symbol_table

    symbol_table[-1].append(record)



def addNewLevel():
    # invoked at the START of main program or a subprogram
    global symbol_table

    symbol_table.append([])


def removeCurrentLevel():
    # invoked at the END of main program or a subprogram
    global symbol_table

    symbol_table.pop(-1)


def updateField(field_value):
    # field_value is either framlength (int) or Quad object (Quad)
    global symbol_table

    if isinstance(field_value, int):
        symbol_table[-1][-1].framelength += field_value


    elif isinstance(field_value, Quad):
        symbol_table[-1][-1].startingQuad = field_value


def addFormalParameter(formal_parameter):
    global symbol_table
   # print(symbol_table[-1])
    symbol_table[-1][-1].formalParameters.append(formal_parameter)


def getRecord(recordName: str):
    record = [record for level in reversed(symbol_table) for record in level if record.name == recordName][0]
    return record



####################### SYMBOL TABLE FUNCTIONS AND CLASSES (end) #######################

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

        while not status:
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
                elif curr == '#':  # in this state we need to find another '#' symbol, before a potential eof occurs.
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

                else:  # signals the end of a declaration!
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

                else:  # signals the end of a declaration!
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
                    if not is_blank(curr):
                        token.append(curr)
                    printerror_lexical("unrecognizable token '" + "".join(token) + "'. Do you mean ':='?", linenum)

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
    global token, program_name

    if token == "program":
        token = lexical()  # program's ID (name)
        program_name = token

        print("Program '" + program_name + "' has started.")

        if not acceptable_varname(token):
            printerror_parser("program's name must be an alphanumerical sequence, mandatorily starting with a letter.",
                              "program", linenum)
        token = lexical()


        block(program_name)



        print("Syntax analysis ended successfully.")


    else:
        printerror_parser("illegal start of program's syntax.", "program", linenum)


def block(subprogramID:str):
    global token

    if token == "{":
        token = lexical()
        declarations(subprogramID)
        subprograms()

        genQuad("begin_block", subprogramID, '_', '_')
        blockstatements()

        # H halt emfanizetai mono sto kuriws programma. Topotheteitai prin apo to end_block.
        if subprogramID == program_name:
            genQuad("halt", '_', '_', '_')

        genQuad('end_block', subprogramID, '_', '_')

        if token != '}':
            printerror_parser("'}' expected, not found.", "block", linenum)
        """
        we need this token because blockstatements ends with '}'
        and the only non-terminal symbol which deploys block()
        needs 1 token on the exit for its while-loop. Else, 
        we will exit subprograms without noticing.
        """
        token = lexical()

    else:
        printerror_parser("'{' expected before block, not found.", "block", linenum)


def declarations(subprogramID: str):
    """ we can opt not to declare any variable whatsoever. """
    global token, main_program_declared_vars, offset

    while token == "declare":  # Kleene star implementation for "declare" non-terminal
        token = lexical()   # always a variable

        declared_varID = token

        if subprogramID == program_name:
            main_program_declared_vars.append(token)

        declared_var = Variable(declared_varID, "int", offset)
        offset += 4


        varlist(subprogramID)

        token = lexical()   # "declare" keyword or first token of next line.



def varlist(subprogramID: str):
    global token, main_program_declared_vars

    if not acceptable_varname(token):
        printerror_parser("variable's identifier must be an alphanumerical sequence, "
                          "mandatorily starting with a letter.", "varlist", linenum)

    token = lexical()  # comma or semicolon



    while token != ';':  # can leave only and only if token == ';'
        token = lexical()  # variable's id

        if subprogramID == program_name:
            main_program_declared_vars.append(token)


        if not acceptable_varname(token):
            printerror_parser("variable's identifier must be an alphanumerical sequence, "
                              "mandatorily starting with a letter.", "varlist", linenum)
        token = lexical()






def subprograms():
    subprogram()


def subprogram():

    global token

    while token in ("function", "procedure"):

        # subprogram_type = token     # function or procedure?

        token = lexical()  # subprogram's ID  (e.g. isPrime)

        subprogramID = token

        #################################### TESTING SYMBOL TABLE ####################################


        #if subprogram_type == "function":
            #func = Function()



        #################################### TESTING SYMBOL TABLE ####################################

        if not acceptable_varname(token):
            printerror_parser("subprogram's identifier must be an alphanumeric sequence, "
                              "mandatorily starting with a letter.", "subprogram", linenum)

        token = lexical()  # (

        if token != '(':
            printerror_parser("'(' expected before formal parameters declaration, not found.", "subprogram", linenum)

        parlist("formal")  # ends with ')'

        block(subprogramID)



def parlist(arg_type:str):
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
        return

    if token == "in":   # cv
        token = lexical()

        expressionParameter = expression()

        genQuad("par", expressionParameter, "cv", '_')



    elif token == "inout":  # ref
        token = lexical()  # parameter's ID
        parameterID = token

        if not acceptable_varname(token):
            printerror_parser("parameter's identifier must be an alphanumerical sequence, "
                              "mandatorily starting with a letter.", "actualparitem", linenum)

        genQuad("par", parameterID, "ref", '_')

        token = lexical()  # comma or closing parenthesis


def formalparitem():
    global token

    if token not in ('in', 'inout'):
        return

    token = lexical()  # parameter's ID

    if not acceptable_varname(token):
        printerror_parser("parameter's identifier must be an alphanumerical sequence, "
                          "mandatorily starting with a letter.", "formalparitem", linenum)

    token = lexical()  # comma or closing parenthesis


    if token not in (')', ','):
        printerror_parser("illegal formal parameter declaration syntax, no ')' or ',' found.", "formalparitem", linenum)


def statements():  # no unused token
    global token
    if token != ';':
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
    # after statement we have 1 leftover token

    if token == "if":  # ok
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

    # assignStat case
    elif token.isalnum():
        target_id = token

        if not acceptable_varname(token):
            printerror_parser("parameter's identifier must be an alphanumerical sequence, "
                              "mandatorily starting with a letter.", "statement", linenum)
        token = lexical()  # :=

        if token != ":=":
            printerror_parser("assignment syntax is incorrect.", "statement", linenum)

        token = lexical()


        source_expression = expression()

        genQuad(":=", source_expression, '_', target_id)



def inputStat():
    global token

    token = lexical()

    if token != '(':
        printerror_parser("'(' expected, not found.", "inputStat", linenum)

    token = lexical()  # ID

    inputID = token

    genQuad("in", inputID, '_', '_')

    if not acceptable_varname(token):
        printerror_parser("variable's identifier must be an alphanumerical sequence, "
                          "mandatorily starting with a letter.", "inputStat", linenum)

    token = lexical()  # )
    if token != ')':
        printerror_parser("')' expected, not found.", "inputStat", linenum)

    token = lexical()  # extra


def callStat():
    global token

    token = lexical()

    called_subprogram = token

    if not acceptable_varname(token):
        printerror_parser("subprogram's identifier must be an alphanumerical sequence, "
                          "mandatorily starting with a letter.", "callStat", linenum)

    token = lexical()  # (

    if token != '(':
        printerror_parser("'(' expected, not found.", "callStat", linenum)

    parlist("actual")  # TODO: I THINK that parlist retain an unused token so no need for an extra one, investigate

    # call subprogram after we have created the actual parameters.
    genQuad("call", called_subprogram, '_', '_')



def return_printStat(typ: str):
    global token

    token = lexical()

    if token != '(':
        printerror_parser("'(' expected, not found.", typ + "Stat", linenum)

    token = lexical()

    source = expression()

    if typ == "return":
        genQuad("ret", source, '_', '_')

    elif typ == "print":
        genQuad("out", source, '_', '_')


    if token != ')':
        printerror_parser("')' expected, not found.", typ + "Stat", linenum)

    token = lexical()  # extra


def if_whileStat(conditional: str):  # 1 unused token
    global token

    if conditional == "while":
        condQuad = nextQuad() # place where compiler returns if while condition is True.


    token = lexical()   # (

    if token != '(':
        printerror_parser("'(' expected, not found.", conditional + "Stat", linenum)

    token = lexical()

    (condition_True, condition_False) = condition()

    if token != ')':
        printerror_parser("')' expected, not found.", conditional + "Stat", linenum)

    backpatch(condition_True, nextQuad())

    token = lexical()
    statements()

    if conditional == "while":
        # only condition_True quads reach this
        genQuad("jump", '_', '_', condQuad)


    if conditional == "if":
        # stores the label of the quad that suceeds the else part
        ifList = makeList(nextQuad())
        genQuad("jump", '_', '_', '_')

    backpatch(condition_False, nextQuad())

    if conditional == "if":
        elsepart()
        backpatch(ifList, nextQuad())



def elsepart():  # 1 unused token
    global token

    # already has 1 token from statements()

    if token == "else":
        token = lexical()
        statements()


def switch_in_for_caseStat(selection_control: str):
    global token

    if selection_control == "switchcase":
        exitList = emptyList()

    if selection_control == "incase":
        flag = newTemp()

    if selection_control in ("forcase", "incase"):
        firstCondQuad = nextQuad()

    if selection_control == "incase":
        genQuad(':=', 0, '_', flag)


    token = lexical()

    while token == "case":

        token = lexical()  # '('

        if token != '(':
            printerror_parser("'(' expected, not found.", selection_control + "Stat", linenum)

        token = lexical()

        (condition_true, condition_false) = condition()

        backpatch(condition_true, nextQuad())       # switch, for, in


        if token != ')':
            printerror_parser("')' keyword expected, not found.", selection_control + "Stat", linenum)

        token = lexical()

        statements()

        if selection_control == "switchcase":
            t = makeList(nextQuad())
            genQuad("jump", '_', '_', '_')

        if selection_control == "forcase":
            genQuad("jump", '_', '_', firstCondQuad)


        if selection_control == "switchcase":
            exitList = mergeList(exitList, t)   # switch

        if selection_control == "incase":
            genQuad(':=', 1, '_', flag)

        backpatch(condition_false, nextQuad())  # switch, for, in



    if selection_control == "incase":
        # flag?
        genQuad('=', 1, flag, firstCondQuad)

    if token != "default" and selection_control in ("switchcase", "forcase"):
        printerror_parser("'default' keyword expected, not found.", selection_control + "Stat", linenum)

    if selection_control in ("switchcase", "forcase"):
        token = lexical()
        statements()

        if selection_control == "switchcase":
            backpatch(exitList, nextQuad())

######################## LOGICAL OPERATIONS (start) ########################


""" HOW LOGICAL OPERATIONS WORK IN INTERMEDIARY CODE: """

# 1) OR occassion:
# Backpatch all B.False quads (boolterms that failed) with label of the nextQuad().
# This will result the enforced check of the upcoming boolterm, in order for the rule
# to decide whether the condition is True or False.
#
# Merge all B.True quads (boolterms that succeeded).  # mergeList(B.True, Q2.True)
#
# Finally, at B.True we have all quads that participated in "or" sequence and at B.False
# we have the quad that succeeds the final quad of or sequence.
#
# 2) AND occassion:
# Lazy evaluation regarding AND operator is complementary to OR's one.
#
# That said, we deal with Q.True quads similarly as we did with B.False ones in OR.
#
#
#
#
#
"""                                                 """


def condition():  # 1 unused token after
    global token


    (Q1_True, Q1_False) = boolterm()  # Q1
    B_True = Q1_True
    B_False = Q1_False

    while token == "or":
        backpatch(B_False, nextQuad())

        token = lexical()

        (Q2_True, Q2_False) = boolterm()  # Q2

        B_True = mergeList(B_True, Q2_True)
        B_False = Q2_False

    return (B_True, B_False)  # later, will be used by case, while and if for condition evaluation.


def boolterm():  # 1 unused token after
    global token

    (R1_True, R1_False) = boolfactor()

    Q_True = R1_True
    Q_False = R1_False

    while token == "and":
        backpatch(Q_True, nextQuad())

        token = lexical()



        (R2_True, R2_False) = boolfactor()

        Q_False = mergeList(Q_False, R2_False)
        Q_True = R2_True

    return (Q_True, Q_False)


def boolfactor():  # 1 unused token after
    global token

    if token == "not":

        token = lexical()


        if token != '[':
            printerror_parser("'[' expected, not found.", "boolfactor", linenum)

        token = lexical()


        (B_True, B_False) = condition()

        R_True = B_False

        R_False = B_True

        if token != ']':
            printerror_parser("']' expected, not found.", "boolfactor", linenum)

        token = lexical()  # for boolterm

    elif token == "[":

        token = lexical()

        (B_True, B_False) = condition()

        R_True = B_True

        R_False = B_False

        if token != ']':
            printerror_parser("']' expected, not found.", "boolfactor", linenum)

        token = lexical()  # for boolterm

    else:
        E1 = expression()

        rel_op = token

        if token not in ('=', '<=', '>=', '>', '<', '<>'):
            printerror_parser("relational operator expected, not found.", "boolfactor", linenum)

        token = lexical()

        E2 = expression()

        R_True = makeList(nextQuad())

        genQuad(rel_op, E1, E2, '_')

        R_False = makeList(nextQuad())

        genQuad("jump", '_', '_', '_') # op = jump

    return (R_True, R_False)


######################## LOGICAL OPERATIONS (end) ########################


# used in expression non-terminal symbol
def reverseSign(term):
    negative_left_term_temp = newTemp()

    genQuad('-', 0, term, negative_left_term_temp)  # left_term = - left_term

    term = negative_left_term_temp

    return term


def expression():  # after expression we have 1 token left.
    # needs 1 token before entering
    global token

    opt_op = ''

    if token in ('+', '-'):  # optionalSign
        token = lexical()

        opt_op = token

    left_term = term()  # returns a multiplication expression ---- T(1).place

    if opt_op == '-':
        left_term = reverseSign(left_term)

    while token in ('+', '-'):  # Kleene star
        add_op = token

        token = lexical()  # integer, expression, variable or function call

        right_term = term()  # T(2).place

        factor_temp = newTemp()

        genQuad(add_op, left_term, right_term, factor_temp)

        left_term = factor_temp

    return left_term


def term():
    global token
    # after term we have 1 token left.
    # already have one unused token before calling term()
    left_factor = factor()  # T(1).place

    while token in ('*', '/'):  # MUL_OP
        mul_op = token

        token = lexical()

        right_factor = factor()  # T(2).place

        term_temp = newTemp()

        genQuad(mul_op, left_factor, right_factor, term_temp)

        left_factor = term_temp

    return left_factor


def factor():
    global token

    # already have one unused token before calling factor()
    # 1 token left after factor return

    if token.isdigit():  # INTEGER
        returned_int = token

        token = lexical()

        return returned_int  # terminal symbol

    elif token == '(':
        token = lexical()

        returned_expression = expression()

        if token != ')':
            printerror_parser("')' expected, not found.", "factor", linenum)

        token = lexical()

        return returned_expression

    else:  # variable or subprogram case
        if not acceptable_varname(token):
            printerror_parser("parameter's or subprogram's identifier must be an alphanumerical sequence, "
                              "mandatorily starting with a letter.", "factor", linenum)

        returned_var_or_func = token

        token = lexical()

        is_subprogram = idtail()

        if is_subprogram:
            returned_value = newTemp()
            genQuad("par", returned_value, "ret", '_')
            genQuad("call", returned_var_or_func, '_', '_')
            return returned_value


        return returned_var_or_func


def idtail():
    global token

    if token == '(':
        parlist("actual")

        return True  # indeed, we have a subprogram call


def check_file(path: str) -> bool:
    return path[-3:] == ".ci"


def get_extn(file: str) -> str:
    idx = file.rindex('.')
    return file[idx:]


def main():
    input_file = sys.argv[1]

    # check if file has .ci extension. check_file function.
    if not check_file(input_file):
        sys.exit("File extension '" + get_extn(input_file) + "' is not acceptable.")

    openfile(input_file)
    parser()
    create_int_file()
    create_c_file()
    for i in range(len(symbol_table)):
        for j in symbol_table[i]:
            print("Level " + str(i) + ": " + str(j))
            for formal in j.formalParameters:
                print(formal)

if __name__ == "__main__":
    main()


