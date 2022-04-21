# Compilers-MYY802
Project for undergraduate compulsory course "Compliers-MYY802". 
The goal of this project is to create a compiler for the minimilastic programming lanuage "Cimple".
Cimple resembles C syntactically. 

# Cimple's syntax grammar in BNF

program→programID <br>
block <br>
. <br>
 <br>
block→{ <br>
declarations <br>
subprograms <br>
blockstatements <br>
} <br>
 <br>
 <br>
declarations→(declarevarlist;)∗ <br>
 <br>
; alistofvariablesfollowingthedeclarationkeyword <br>
varlist→ID <br>
(,ID)∗ <br>
|𝜀 <br>
 <br>
; zeroormoresubprograms <br>
subprograms→(subprogram)∗ <br>
 <br>
; asubprogramisafunctionoraprocedure, <br>
; followedbyparametersandblock <br>
subprogram→functionID(formalparlist) <br>
block <br>
|procedureID(formalparlist) <br>
block <br>
 <br>
; listofformalparameters <br>
; oneormoreparametersareallowed <br>
formalparlist→formalparitem <br>
(,formalparitem)∗ <br>
|𝜀 <br>
 <br>
; aformalparameter <br>
; "in":byvalue,"inout"byreference <br>
formalparitem→inID <br>
|inoutID <br>
 <br>
; oneormorestatements <br>
; morethanonestatementsshouldbegroupedwithbrackets <br>
statements→statement; <br>
|{ <br>
blockstatements <br>
} <br>
 <br>
; statementsconsideredasblock(usedinprogramandsubprogram) <br>
blockstatements→statement <br>
(;statement)∗ <br>
 <br>
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
 <br>
; assignmentstatement <br>
assignStat→ID:=expression <br>
 <br>
; ifstatement <br>
ifStat→if(condition) <br>
statements <br>
elsepart <br>
 <br>
; elsepartisoptional <br>
elsepart→else <br>
statements <br>
|𝜀 <br>
 <br>
; whilestatement <br>
whileStat→while(condition) <br>
statements <br>
 <br>
; switchstatement <br>
switchcaseStat→switchcase <br>
(case(condition)statements)∗ <br>
defaultstatements <br>
 <br>
; forcasestatement <br>
forcaseStat→forcase <br>
(case(condition)statements)∗ <br>
defaultstatements <br>
 <br>
; incasestatement <br>
incaseStat→incase <br>
(case(condition)statements)∗ <br>
 <br>
; returnstatement <br>
returnStat→return(expression) <br>
 <br>
; callstatement <br>
callStat→callID(actualparlist) <br>
 <br>
; printstatement <br>
printStat→print(expression) <br>
 <br>
; inputstatement <br>
inputStat→input(ID) <br>
 <br>
; listofactualparameters <br>
actualparlist→actualparitem <br>
(,actualparitem)∗ <br>
|𝜀 <br>
 <br>
; anactualparameter <br>
; "in":byvalue,"inout"byreference <br>
actualparitem→inexpression <br>
|inoutID <br>
 <br>
; booleanexpression <br>
condition→boolterm <br>
(orboolterm)∗ <br>
 <br>
; terminbooleanexpression <br>
boolterm→boolfactor <br>
(andboolfactor)∗ <br>
 <br>
; factorinbooleanexpression <br>
boolfactor→not[condition] <br>
|[condition] <br>
|expressionREL_OPexpression <br>
 <br>
; arithmeticexpression <br>
expression→optionalSignterm <br>
(ADD_OPterm)∗ <br>
 <br>
; terminarithmeticexpression <br>
term→factor <br>
(MUL_OPfactor)* <br>
 <br>
; factorinarithmeticexpression <br>
factor→INTEGER <br>
|(expression) <br>
|IDidtail <br>
 <br>
; followsafunctionorprocedure <br>
; describesparethnesesandparameters <br>
idtail→(actualparlist) <br>
|𝜀 <br>
 <br>
; symbols"+"and"‐"(areoptional) <br>
optionalSign→ADD_OP <br>
|𝜀 <br>
 <br>
; ######################### <br>
; lexerrules:relational,arithenticoperations, <br>
; integervaluesandids <br>
REL_OP→=|<=|>=|>|<|<> <br>
ADD_OP→+|‐ <br>
MUL_OP→*|/ <br>
INTEGER→[0‐9]+ <br>
ID→[a‐zA‐Z][a‐zA‐Z0‐9]* <br>
 <br>
