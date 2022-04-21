# Compilers-MYY802
Project for undergraduate compulsory course "Compliers-MYY802". 
The goal of this project is to create a compiler for the minimilastic programming lanuage "Cimple".
Cimple resembles C syntactically. 

# Cimple's syntax grammar in BNF

program→programID <br>
block <br>
. <br>
block→{ <br>
declarations <br>
subprograms <br>
blockstatements <br>
} <br>
declarations→(declarevarlist;)∗ <br>
; alistofvariablesfollowingthedeclarationkeyword <br>
varlist→ID <br>
(,ID)∗ <br>
|𝜀 <br>
; zeroormoresubprograms <br>
subprograms→(subprogram)∗ <br>
; asubprogramisafunctionoraprocedure, <br>
; followedbyparametersandblock <br>
subprogram→functionID(formalparlist) <br>
block <br>
|procedureID(formalparlist) <br>
block <br>
; listofformalparameters <br>
; oneormoreparametersareallowed <br>
formalparlist→formalparitem <br>
(,formalparitem)∗ <br>
|𝜀 <br>
; aformalparameter <br>
; "in":byvalue,"inout"byreference <br>
formalparitem→inID <br>
|inoutID <br>
; oneormorestatements <br>
; morethanonestatementsshouldbegroupedwithbrackets <br>
statements→statement; <br>
|{ <br>
blockstatements <br>
} <br>
; statementsconsideredasblock(usedinprogramandsubprogram) <br>
blockstatements→statement <br>
(;statement)∗ <br>
; onestatement <br>
statement→assignStat <br>
|ifStat <br>
|whileStat <br>
|switchcaseStat <br>
|forcaseStat <br>
|incaseStat <br>
|callStat <br>
|returnStat <br>
|inputStat <br>
|printStat <br>
|𝜀 <br>
; assignmentstatement <br>
assignStat→ID:=expression <br>
; ifstatement <br>
ifStat→if(condition) <br>
statements <br>
elsepart <br>
; elsepartisoptional <br>
elsepart→else <br>
statements <br>
|𝜀 <br>
; whilestatement <br>
whileStat→while(condition) <br>
statements <br>
; switchstatement <br>
switchcaseStat→switchcase <br>
(case(condition)statements)∗ <br>
defaultstatements <br>
; forcasestatement <br>
forcaseStat→forcase <br>
(case(condition)statements)∗ <br>
defaultstatements <br>
; incasestatement <br>
incaseStat→incase <br>
(case(condition)statements)∗ <br>
; returnstatement <br>
returnStat→return(expression) <br>
; callstatement <br>
callStat→callID(actualparlist) <br>
; printstatement <br>
printStat→print(expression) <br>
; inputstatement <br>
inputStat→input(ID) <br>
; listofactualparameters <br>
actualparlist→actualparitem <br>
(,actualparitem)∗ <br>
|𝜀 <br>
; anactualparameter <br>
; "in":byvalue,"inout"byreference <br>
actualparitem→inexpression <br>
|inoutID <br>
; booleanexpression <br>
condition→boolterm <br>
(orboolterm)∗ <br>
; terminbooleanexpression <br>
boolterm→boolfactor <br>
(andboolfactor)∗ <br>
; factorinbooleanexpression <br>
boolfactor→not[condition] <br>
|[condition] <br>
|expressionREL_OPexpression <br>
; arithmeticexpression <br>
expression→optionalSignterm <br>
(ADD_OPterm)∗ <br>
; terminarithmeticexpression <br>
term→factor <br>
(MUL_OPfactor)* <br>
; factorinarithmeticexpression <br>
factor→INTEGER <br>
|(expression) <br>
|IDidtail <br>
; followsafunctionorprocedure <br>
; describesparethnesesandparameters <br>
idtail→(actualparlist) <br>
|𝜀 <br>
; symbols"+"and"‐"(areoptional) <br>
optionalSign→ADD_OP <br>
|𝜀 <br>
; ######################### <br>
; lexerrules:relational,arithenticoperations, <br>
; integervaluesandids <br>
REL_OP→=|<=|>=|>|<|<> <br>
ADD_OP→+|‐ <br>
MUL_OP→*|/ <br>
INTEGER→[0‐9]+ <br>
ID→[a‐zA‐Z][a‐zA‐Z0‐9]* <br>
