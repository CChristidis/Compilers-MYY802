# Compilers-MYY802
Project for undergraduate compulsory course "Compliers-MYY802". 
The goal of this project is to create a compiler for the minimilastic programming lanuage "Cimple".
Cimple resembles C syntactically. 

# Cimple's syntax grammar in BNF

program → program ID   <br>
block   <br>
.   <br>
  <br>
block → {   <br>
declarations   <br>
subprograms   <br>
blockstatements   <br>
}   <br>
  <br>
  <br>
declarations → ( declare varlist ; )∗   <br>
  <br>
;   a list of variables following the declaration keyword   <br> <br>
varlist → ID   <br>
( , ID )∗   <br>
| 𝜀   <br>
  <br>
;   zero or more subprograms   <br> <br>
subprograms → ( subprogram )∗   <br>
  <br>
;   a subprogram is a function or a procedure ,   <br> <br>
;   followed by parameters and block   <br> <br>
subprogram → function ID ( formalparlist )   <br>
block   <br>
| procedure ID ( formalparlist )   <br>
block   <br>
  <br>
;   list of formal parameters   <br> <br>
;   one or more parameters are allowed   <br> <br>
formalparlist → formalparitem   <br>
( , formalparitem )∗   <br>
| 𝜀   <br>
  <br>
;   a formal parameter   <br> <br>
;   "in ": by value , " inout " by reference   <br> <br>
formalparitem → in ID   <br>
| inout ID   <br>
  <br>
;   one or more statements   <br> <br>
;   more than one statements should be grouped with brackets   <br> <br>
statements → statement ;   <br>
| {   <br>
blockstatements   <br>
}   <br>
  <br>
;   statements considered as block ( used in program and subprogram )   <br> <br>
blockstatements→ statement   <br>
( ; statement )∗   <br>
  <br>
;   one statement   <br> <br>
statement → assignStat   <br>
| ifStat   <br>
| whileStat   <br>
| switchcaseStat   <br>
| forcaseStat   <br>
| incaseStat   <br>
| callStat   <br>
| returnStat   <br>
| inputStat   <br>
| printStat   <br>
| 𝜀   <br>
  <br>
;   assignment statement   <br> <br>
assignStat → ID := expression   <br>
  <br>
;   if statement   <br> <br>
ifStat → if ( condition )   <br>
statements   <br>
elsepart   <br>
  <br>
;   else part is optional   <br> <br>
elsepart → else   <br>
statements   <br>
| 𝜀   <br>
  <br>
;   while statement   <br> <br>
whileStat → while ( condition )   <br>
statements   <br>
  <br>
;   switch statement   <br> <br>
switchcaseStat → switchcase   <br>
( case ( condition ) statements )∗   <br>
default statements   <br>
  <br>
;   forcase statement   <br> <br>
forcaseStat → forcase   <br>
( case ( condition ) statements )∗   <br>
default statements   <br>
  <br>
;   incase statement   <br> <br>
incaseStat → incase   <br>
( case ( condition ) statements )∗   <br>
  <br>
;   return statement   <br> <br>
returnStat → return( expression )   <br>
  <br>
;   call statement   <br> <br>
callStat → call ID( actualparlist )   <br>
  <br>
;   print statement   <br> <br>
printStat → print( expression )   <br>
  <br>
;   input statement   <br> <br>
inputStat → input( ID )   <br>
  <br>
;   list of actual parameters   <br> <br>
actualparlist → actualparitem   <br>
( , actualparitem )∗   <br>
| 𝜀   <br>
  <br>
;   an actual parameter   <br> <br>
;   "in ": by value , " inout " by reference   <br> <br>
actualparitem → in expression   <br>
| inout ID   <br>
  <br>
;   boolean expression   <br> <br>
condition → boolterm   <br>
( or boolterm )∗   <br>
  <br>
;   term in boolean expression   <br> <br>
boolterm → boolfactor   <br>
( and boolfactor )∗   <br>
  <br>
;   factor in boolean expression   <br> <br>
boolfactor → not [ condition ]   <br>
| [ condition ]   <br>
| expression REL_OP expression   <br>
  <br>
;   arithmetic expression   <br> <br>
expression → optionalSign term   <br>
( ADD_OP term )∗   <br>
  <br>
;   term in arithmetic expression   <br> <br>
term → factor   <br>
( MUL_OP factor )*   <br>
  <br>
;   factor in arithmetic expression   <br> <br>
factor → INTEGER   <br>
| ( expression )   <br>
| ID idtail   <br>
  <br>
;   follows a function or procedure   <br> <br>
;   describes parethneses and parameters   <br> <br>
idtail → ( actualparlist )   <br>
| 𝜀   <br>
  <br>
;   symbols "+" and " ‐" (are optional )   <br> <br>
optionalSign → ADD_OP   <br>
| 𝜀   <br>
  <br>
;   #########################   <br> <br>
;   lexer rules : relational , arithentic operations ,   <br> <br>
;   integer values and ids   <br> <br>
REL_OP → = | <= | >= | > | < | <>   <br>
ADD_OP → + | ‐   <br>
MUL_OP → * | /   <br>
INTEGER → [0‐9]+   <br>
ID → [a‐zA‐Z][a‐zA‐Z0‐9]*   <br>
  <br>


