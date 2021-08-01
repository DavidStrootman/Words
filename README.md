# Words
[![Build](https://github.com/DavidStrootman/Words/actions/workflows/build.yml/badge.svg)](https://github.com/DavidStrootman/Words/actions/workflows/build.yml)

Words programming language

Contains my own programming language "Words".  
Includes a lexer/parser, an interpreter in python and (hopefully soon) a compiler for Cortex-M0

### Words

- Inspired by (the syntax of) Forth
- Stack based (stack, dictionary, local stack)

Should support:

- Functions/Subroutines
- Anonymous functions

- Goto:  
  `LABEL mylabel`  
  `GOTO mylabel`

### Syntax

- [Operators](#Operators):  
  `X Y ==` -> `x==y`
- [Stack Manipulation](#Stack Manipulation)  
  `DUP` -> `X Y -- X Y Y`
- Functions/Subroutines  
  `| NAME ( VALUE X, VALUE Y ) X Y == RETURN 1|`  
- Anonymous functions  
  `λ ( VALUE X, VALUE Y ) X Y == λ`  
  Takes the top element of the global stack for every argument and places it in the dictionary
  

### Keywords
Keywords must be placed on their own line.
#### BEGIN  
Marks the start of a while loop. It is followed by an expression, and then the `WHILE` keyword
```python
BEGIN
1 0 > # Loop while 1 is greater than 0
WHILE
```
#### WHILE  
Marks the start of the body of a while loop. Is preceded by an expression and followed by a block of code. 
```python
1 0 > # Loop while 1 is greater than 0
WHILE
1 0 +
```
#### REPEAT  
Marks the end of the body of a while loop. Goes back to the BEGIN, and if the following expression holds true, it loops again.
If the expression is false, it continues with the line below it.
```python
BEGIN
1 0 > # Loop while 1 is greater than 0
WHILE
1 0 +
REPEAT
```
#### Conditionals (IF ELSE THEN)  
Conditionals in Words are built up of three keywords: IF, ELSE and THEN. Conditionals work the same way
as they do in Forth. The IF is preceded by a boolean operator of some sort. If the result is true, the block of code following IF is called.
If a ELSE block is given, the execution continues at THEN. If the result if false, the else block is called. [Forth documentation](https://www.forth.com/starting-forth/4-conditional-if-then-statements/)
```python
12 12 == # Places 12 and 12 on the stack and checks if they are equal
IF # If the statement is true
# Do something and go to THEN
ELSE # If the statement is false
# Do something else and go to THEN
THEN
# Continue here
```
#### VARIABLE
global and local variables are defined using the `VARIABLE` keyword:
```python
VARIABLE count
```  
Words uses one dictionary for all variables, both local and global. Shadowing is not allowed, and all variables in functions
that are not defined in the local scope must be passed as parameters. Using a global variable in a local scope will cause a 
compile error.
#### ASSIGN
The `ASSIGN` keyword assigns the topmost value from the stack to the variable stored in the dictionary:
```python
40
count ASSIGN # Assigns the topmost value (40) to count (= in other languages)
```
#### RETURN
TODO
### Operators
Operators take between 0 and 2 arguments, depending on how many should be taken from the stack.
```python
20 10 - # subtracts 10 from 20 and places the result on the stack
10 - # subtracts 10 from the value on the top of the stack and places the result on the stack
- # If the stack is [5, 20, 30, 10], first takes 10, then 30 and places (30 - 10) back on the stack. 
```
The arguments could be seen as extending the stack with new values before executing the opration. For 
example the expression `20 /`, placing the complete operation between parentheses:  
if the stack is [10, 20, 30] the operation would be `[10, 20, (30], 20 /)`, taking only 30 from the stack and dividing it by 20.

### Macros
TODO