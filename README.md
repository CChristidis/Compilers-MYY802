# Compilers-MYY802
Project for undergraduate compulsory course "Compliers-MYY802". 
The goal of this project is to create a compiler for the minimilastic programming lanuage "Cimple".
Cimple resembles C syntactically. 

; Cimple's syntax grammar in BNF
program → program ID
block
.

; a block consists of declarations , subprograms and statements
block → {
declarations
subprograms
blockstatements
}

; declaration of variables
; Kleene star implies zero or more " declare " statements
declarations → ( declare varlist ; )∗

; a list of variables following the declaration keyword
varlist → ID
( , ID )∗
| 𝜀

; zero or more subprograms
subprograms → ( subprogram )∗

; a subprogram is a function or a procedure ,
; followed by parameters and block
subprogram → function ID ( formalparlist )
block
| procedure ID ( formalparlist )
block

; list of formal parameters
; one or more parameters are allowed
formalparlist → formalparitem
( , formalparitem )∗
| 𝜀

; a formal parameter
; "in ": by value , " inout " by reference
formalparitem → in ID
| inout ID

; one or more statements
; more than one statements should be grouped with brackets
statements → statement ;
| {
blockstatements
}

; statements considered as block ( used in program and subprogram )
blockstatements→ statement
( ; statement )∗

; one statement
statement → assignStat
| ifStat
| whileStat
| switchcaseStat
| forcaseStat
| incaseStat
| callStat
| returnStat
| inputStat
| printStat
| 𝜀

; assignment statement
assignStat → ID := expression

; if statement
ifStat → if ( condition )
statements
elsepart

; else part is optional
elsepart → else
statements
| 𝜀

; while statement
whileStat → while ( condition )
statements

; switch statement
switchcaseStat → switchcase
( case ( condition ) statements )∗
default statements

; forcase statement
forcaseStat → forcase
( case ( condition ) statements )∗
default statements

; incase statement
incaseStat → incase
( case ( condition ) statements )∗

; return statement
returnStat → return( expression )

; call statement
callStat → call ID( actualparlist )

; print statement
printStat → print( expression )

; input statement
inputStat → input( ID )

; list of actual parameters
actualparlist → actualparitem
( , actualparitem )∗
| 𝜀

; an actual parameter
; "in ": by value , " inout " by reference
actualparitem → in expression
| inout ID

; boolean expression
condition → boolterm
( or boolterm )∗

; term in boolean expression
boolterm → boolfactor
( and boolfactor )∗

; factor in boolean expression
boolfactor → not [ condition ]
| [ condition ]
| expression REL_OP expression

; arithmetic expression
expression → optionalSign term
( ADD_OP term )∗

; term in arithmetic expression
term → factor
( MUL_OP factor )*

; factor in arithmetic expression
factor → INTEGER
| ( expression )
| ID idtail

; follows a function or procedure
;  describes parethneses and parameters
idtail → ( actualparlist )
| 𝜀

; symbols "+" and " ‐" (are optional )
optionalSign → ADD_OP
| 𝜀


; lexer rules : relational , arithentic operations ,
; integer values and ids
REL_OP → = | <= | >= | > | < | <>
ADD_OP → + | ‐
MUL_OP → * | /
INTEGER → [0‐9]+
ID → [a‐zA‐Z][a‐zA‐Z0‐9]*

