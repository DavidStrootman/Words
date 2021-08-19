# Words
[![Build](https://github.com/DavidStrootman/Words/actions/workflows/build.yml/badge.svg)](https://github.com/DavidStrootman/Words/actions/workflows/build.yml)
[![codecov](https://codecov.io/gh/DavidStrootman/Words/branch/main/graph/badge.svg?token=H9ZX3DWZQA)](https://codecov.io/gh/DavidStrootman/Words)
[![License](https://img.shields.io/github/license/davidstrootman/words)](https://github.com/DavidStrootman/Words/blob/main/LICENSE)

Words programming language

Contains my own programming language "Words".  
Includes a lexer/parser, an interpreter in python and (hopefully soon) a compiler for Cortex-M0

## Words

- Inspired by (the syntax of) Forth
- Stack based (stack, dictionary, local stack)


## Stack based
Words is a stack based language. This means that it's operations are done using a stack machine.
Words consists of two main parts: the stack, and the dictionary. The stack is used to store values, while the dictionary 
holds variables or functions.  
All Words code boils down to a few basic operations: changing the state of the stack by removing or adding values,
creating new variables or changing their values.  
One main way Words differs from Forth, is that variable retrieval is implicit, making it easier to use variables.



## Syntax
All parts of the syntax must be separated with whitespace. There is no limit on the amount or location of line-breaks.

### Operators
Words has three types of operators: 
##### Arithmetic Operators
Arithmetic operators are used to calculate a new value using the stack. For example, the `-` operator subtracts the
topmost value from the value beneath it:
```text
10 20 -  # place 10 and 20 on the stack and subtract 20 from 10, resulting in -10
```
| **Arithmetic Operators** | Syntax | Description         |
|--------------------------|--------|---------------------|
| +                        | X Y +  | Add Y and X*        |
| -                        | X Y -  | Subtracts Y from X* |
&ast;The result gets placed back on the stack
##### Boolean Operators
Boolean operators are used to compare values on the stack, resulting in a boolean value, for example the `>` operator
compares the second value on the stack with the topmost one.
```text
30 7000 >  # place 30 and 7000 on the stack and check if 30 > 7000, resulting in False
```
| **Boolean Operators** | Syntax | Description                               |
|-----------------------|--------|-------------------------------------------|
| ==                    | X Y == | Check if Y and X are equal*               |
| \>                    | X Y >  | Check if Y is greater than X*             |
| <                     | X Y <  | Check if Y is lesser than X*              |
| >=                    | X Y >= | Check if Y is greater than or equal to X* |
| <=                    | X Y <= | Check if Y is lesser than or equal to X*  |
&ast;The result gets placed back on the stack

##### Dictionary Operators
Dictionary Operators are used to interact with the dictionary. For example the ASSIGN operator assigns the topmost value
on the stack to the provided variable:
```text
VARIABLE X  # create a variable named X
5           # Place the value 5 on the stack
ASSIGN X    # Assign 5 to X, removing it from the stack
```
| **Dictionary Operators** | Syntax   | Description                                  |
|--------------------------|----------|----------------------------------------------|
| ASSIGN                   | ASSIGN X | Assign the topmost value from the stack to X |

### Functions
Functions in Words behave like in most languages. They are first defined, and can be called later.
Function syntax is as follows:
```text
|                   # Start of function declaration, using a pipe
SOME_FUNC           # Function name
(                   # Start of parameters
VALUE X             # First parameter
VALUE Y             # Second parameter
                    # etc.
)                   # End of parameters
20 Y + 35 X + +     # Some body for the function
RETURN              # Return statement
1                   # Return count (either 1, 2 or 3)
|                   # End of function declaration, another pipe
```
While this is completely valid Words code, it might be more readable to not spread it out so much:
```text
| SOME_FUNC ( VALUE X VALUE Y ) 
20 Y +
35 X + 
+
RETURN 1 |
```

### Loops
Words supports while loops. While are defined using three keywords:
#### BEGIN  
Marks the start of a while loop. It is followed by an expression, and then the `WHILE` keyword

#### WHILE  
Marks the start of the body of a while loop. Is preceded by an expression and followed by a block of code. 

#### REPEAT  
Marks the end of the body of a while loop. Goes back to the BEGIN, and if the following expression holds true, it loops again.
If the expression is false, it continues with the line below it.
```text
BEGIN
1 0 > # Loop while 1 is greater than 0
WHILE
1 0 +
REPEAT
```
### Conditionals (if else)  
Conditionals in Words are built up of three keywords: IF, ELSE and THEN. The IF requires a boolean value to be on top of
the stack. If the value on top of the stack is True, the block of code following IF is run. If a ELSE block is given and
the result is false, the else block is called. After running either of the blocks, the code continues after the THEN 
keyword.
```text
12 12 ==        # Places 12 and 12 on the stack and checks if they are equal
IF              # If the statement is true
1 __PRINT__     # print 1
ELSE            # If the statement is false
0 __PRINT__     # Do something else and go to THEN
THEN            # Continue after this line
```

### VARIABLES
global and local variables are defined using the `VARIABLE` keyword:
```text
VARIABLE count
```
Words uses one dictionary for all variables, both local and global. Shadowing is not allowed, and all variables in functions
that are not defined in the local scope must be passed as parameters using the `VALUE` keyword. Using a global variable in a local scope will cause a 
compile error.

### MACROS
Macros are used to execute some predefined program. The only implemented macro is the `__PRINT__` macro, which 
prints the topmost value on the stack to stdout.