# Yovec Language Specification

## Table of Contents

- [Terminology](#terminology)
- [General Notes](#general-notes)
- [Variables](#variables)
- [Numbers](#numbers)
- [Vectors](#vectors)
- [Matrices](#matrices)
- [Macros](#macros)
- [Libraries](#libraries)
- [Imports](#imports)
- [Exports](#exports)
- [Comments](#comments)
- [Whitespace](#whitespace)
- [Errors](#errors)

## Terminology

- An **alias** is an alternative identifier for a variable or external
- An **external** is a value that has been imported from YOLOL
- A **function** performs an operation on values
- An **identifier** is a name given to a variable, external, or function
- A **literal** is a fixed numeric value, such as `0`
- A **macro** is a limited, user-defined function
- A **matrix** is a non-empty sequence of vectors
- A **number** is a limited-precision decimal
- A **variable** stores a number, vector, or matrix
- A **vector** is a non-empty sequence of numbers

## General Notes

Unary functions are evaluated right-to-left, while binary functions are evaluated left-to-right. Parentheses may be used to enforce precedence.

```
sin cos 0
// Evaluates as sin(cos(0))

1 + 2 * 3 / 4
// Evaluates as ((1 + 2) * 3) / 4

1 + (2 * (3 / 4))
// Evaluates as 1 + (2 * (3 / 4))
```

Yovec is 0-indexed.

```
let vector V = [4, 5, 6]

elem V 1
// Returns 5
```

Trig. functions operate on degrees, not radians.

```
let number A = sin 90
// A == 1
```

`0` is false and all other numbers are true. The default truth value is `1`.

```
let number A = 0 or 47
// A == 1
```

## Variables

A variable stores a number, vector, or matrix.

Variable identifiers may contain uppercase letters and underscores.

```
A
LONG_NAME
```

The `let` statement assigns a value to a variable. The type of the variable must be specified.

```
let number A = 0
let vector V = [1, 2]
let matrix M = [[0, 1], [2, 3]]
```

Variables cannot be redefined.

```
let number A = 0
let number A = 1
// Error: cannot redefine variable A
```

## Numbers

A number is a [limited-precision decimal](https://wiki.starbasegame.com/index.php/YOLOL#Decimals).

Numbers may be represented:

- directly, with a literal (e.g. `1`)
- indirectly, with an external (e.g. `$n`)
- indirectly, with a variable (e.g. `A`)

Numbers may be assigned to variables.

```
let number A = 0
```

Unary functions operate on a single number:

- `neg A`: negate `A`
- `not A`: return true if `A` is false, otherwise false
- `abs A`: calculate the absolute value of `A`
- `sqrt A`: calculate the square root of `A`
- `sin A`: calculate the sine of `A` (in degrees)
- `cos A`: calculate the cosine of `A` (in degrees)
- `tan A`: calculate the tangent of `A` (in degrees)
- `arcsin A`: calculate the inverse sine of `A` (in degrees)
- `arccos A`: calculate the inverse cosine of `A` (in degrees)
- `arctan A`: calculate the inverse tangent of `A` (in degrees)

Unary functions may cause [undefined behaviour](#errors):

- `sqrt A` where `A < 0`
- Trig. functions where the operand is outside of the domain
- Any unary function that causes out-of-bounds

Binary functions operate on two numbers:

- `A + B`: add `A` and `B`
- `A - B`: subtract `B` from `A`
- `A * B`: multiply `A` by `B`
- `A / B`: divide `A` by `B`
- `A % B`: calculate the modulus of `A` and `B`
- `A ^ B`: raise `A` to the power of `B`
- `A < B`: return true if `A` is less than `B`, otherwise false
- `A <= B`: return true if `A` is less than or equal to `B`, otherwise false
- `A > B`: return true if `A` is greater than `B`, otherwise false
- `A >= B`: return true if `A` is greater than or equal to `B`, otherwise false
- `A == B`: return true if `A` is equal to `B`, otherwise false
- `A != B`: return true if `A` is not equal to `B`, otherwise false
- `A and B`: return true if `A` is true and `B` is true, otherwise false
- `A or B`: return true if `A` is true or `B` is true, otherwise false

Binary functions may cause [undefined behaviour](#errors):

- `A / 0`
- `A % 0`
- `0 ^ -1`
- Any binary function that causes out-of-bounds

## Vectors

A vector is a non-empty sequence of numbers.

Vectors may be represented:

- directly, with a list of numbers (e.g. `[1, $n, A]`)
- indirectly, with a variable (e.g. `V`)

Vectors may be assigned to variables.

```
let vector V = [0, 1, 2]
```

The `map` function maps a function element-wise to a vector.

`map` may apply a unary function with no arguments provided, or a binary function with one argument provided.

```
let vector V = [0, 1, 2]

map neg
// Returns [0, -1, -2]

map 1+ V
// Returns [1, 2, 3]

map ^2 V
// Returns [0, 1, 4]
```

The `apply` function applies a binary function element-wise to two or more vectors. All vectors must have the same length.

```
let vector V = [0, 1, 2]
let vector W = [3, 4, 5]

apply + V W
// Returns [3, 5, 7]

let vector X = [6, 7, 8]

apply * V W X
// Returns [0, 28, 80]
```

The `+` and `-` functions provide shorthands for `apply +` and `apply -` respectively.

```
V + W
// Equivalent to: apply + V W

V - W - X
// Equivalent to: apply - V W X
```

The `concat` function concatenates two or more vectors.

```
let vector V = [0, 1, 2]
let vector W = [3, 4, 5]

concat V W
// Returns [0, 1, 2, 3, 4, 5]
```

The `reverse` function reverses the order of the elements in a vector.

```
let vector V = [0, 1, 2]

reverse V
// Returns [2, 1, 0]
```

The `reduce` function [left folds](https://wiki.haskell.org/Fold) the elements of a vector into a number.

```
let vector V = [0, 1, 2]

reduce + V
// Returns 3
```

The `dot` function calculates the dot product of two vectors. Both vectors must have the same length.

```
let vector V = [0, 1, 2]
let vector W = [3, 4, 5]

V dot W
// Returns (0 * 3) + (1 * 4) + (2 * 5)
```

The `len` function returns the length of a vector.

```
let vector V = [0, 1, 2]

len V
// Returns 3
```

The `elem` function gets an element from a vector by index. The index must be a literal.

```
let vector V = [0, 1, 2]

elem V 0
// Returns 0

let number A = 0
elem V A
// Error: index is not a literal
```

## Matrices

A matrix is a non-empty sequence of vectors. Each vector is a row in the matrix.

Matrices may be represented:

- directly, with a literal (e.g. `[[0, 1, 2], [3, 4, 5]`)
- indirectly, with a variable (e.g. `M`)

Matrices may be assigned to variables.

```
let matrix M = [
	[0, 1, 2],
	[3, 4, 5]
]
// Creates a 2 (rows) by 3 (columns) matrix
```

The `map` function maps a function element-wise to a matrix.

`map` may apply a unary function with no arguments provided, or a binary function with one argument provided.

```
let matrix M = [
	[0, 1, 2],
	[3, 4, 5]
]

map neg
// Returns [[0, -1, -2], [-3, -4, -5]]

map 1+ M
// Returns [[1, 2, 3], [4, 5, 6]]

map ^2 M
// Returns [[0, 1, 4], [9, 16, 25]]
```

The `apply` function applies a binary function element-wise to two or more matrices. All matrices must have the same size.

```
let matrix M = [
    [0, 1],
    [2, 3]
]
let matrix N = [
    [4, 5],
    [6, 7]
]

apply + M N
// Returns [[4, 6], [8, 10]]

apply * M M N
// Returns [[0, 5], [24, 147]]
```

The `+` and `-` functions provide shorthands for `apply +` and `apply -` respectively.

```
M + N
// Equivalent to: apply + M N

M - N - O
// Equivalent to: apply - M N O
```

The `transpose` function swaps the rows and columns in a matrix.

```
let matrix M = [
	[0, 1, 2],
	[3, 4, 5]
]

transpose M
// Returns [[0, 3], [1, 4], [2, 5]]
```

The `@` function [multiplies two matrices](https://en.wikipedia.org/wiki/Matrix_multiplication). The number of columns in the first matrix must be equal to the number of rows in the second matrix.

```
M @ N
```

The `rows` function returns the number of rows in a matrix.

```
let matrix M = [
	[0, 1, 2],
	[3, 4, 5]
]

rows M
// Returns 2
```

The `cols` function returns the number of columns in a matrix.

```
let matrix M = [
	[0, 1, 2],
	[3, 4, 5]
]

cols M
// Returns 3
```

The `elem` function gets an element of a matrix by row and column index. The indices must be literals.

```
let matrix M = [
	[0, 1, 2],
	[3, 4, 5]
]

elem M 1 2
// Returns 5

let number A = 1
elem M A 2
// Error: index is not a literal
```

The `row` function gets a row of a matrix by index. The index must be a literal.

```
let matrix M = [
	[0, 1, 2],
	[3, 4, 5]
]

row M 0
// Returns [0, 1, 2]

let number A = 0
row M A
// Error: index is not a literal
```

The `col` function gets a column of a matrix by index. The index must be a literal.

```
let matrix M = [
	[0, 1, 2],
	[3, 4, 5]
]

col M 0
// Returns [0, 3]

let number A = 0
col M A
// Error: index is not a literal
```

## Macros

The `define` statement defines a macro.

A macro must accept one or more arguments, and must return a number, vector, or matrix.

Macro identifiers may contain letters, numbers, underscores.

```
define neg_sum (number A, number B) -> number = (neg A) + (neg B)
// Accepts two numbers, and returns a number

define second (matrix M) -> vector = row M 1
// Accepts a matrix, and return a vector.
```

Macros may not access variables other than their parameters.

```
let number B = 1
define add (number A) -> number = A + B
// Error: variable B is not defined
```

Macros may be called with arguments. An exclamation point (`!`) must follow the name of the macro. Arguments must be enclosed in parentheses.

```
define add (number A, number B) -> number = A + B
let number C = add!(1, 2)
// C == 3
```

Macros must not call themselves.

```
define add (number A, number B) -> number = foo!(A, B)
// Error: recursion is not allowed
```

## Libraries

Libraries are special Yovec files that only contain `define` statements (and comments).

Library identifiers may contain letters, numbers, and underscores.

Library files must have the extension `.lib.yovec`

The `using` statement loads macros from a library.

```
using trig

let number A = sec!(90)
```

Yovec will recursively search for library files in the current working directory.

## Imports

The `import` statement imports a variable from YOLOL. Imported variables are called externals.

The value of an external must be a valid number (i.e. Yovec literal). Importing a string causes [undefined behaviour](#errors). Data fields cannot be imported.

External identifiers must be valid [YOLOL identifiers](https://wiki.starbasegame.com/index.php/YOLOL#Variables).

External identifiers must be prefixed with `$` when used.

```
import n

let variable A = $n + 1
```

External identifiers may be aliased.

```
import long_name as n

let variable A = $n + 1
```

Multiple externals may be imported in a single `import` statement.

```
import m, long_name as n, o, p
```

## Exports

The `export` statement exports a variable to YOLOL.

Exported identifiers must be valid [YOLOL identifiers](https://wiki.starbasegame.com/index.php/YOLOL#Variables).

Vectors and matrices will be expanded to multiple YOLOL variables.

```
let number N = 0
export N
// Result in YOLOL: n=0

let vector V = [0, 1, 2]
export V
// Result in YOLOL: v_e0=0 v_e1=1 v_e2=2

let matrix M = [
    [0, 1, 2],
    [3, 4, 5]
]
export M
// Result in YOLOL: m_r0c0=0 m_r0c1=1 m_r0c2=2 m_r1c0=3 m_r1c1=4 m_r1c2=5
```

Exported identifiers may be aliased.

```
let vector V = [0, 1, 2]
export V as list
// Result in YOLOL: list_e0=0 list_e1=1 list_e2=2
```

## Comments

A comment must start with `//` and must be on its own line.

Inline comments are not allowed.

```
// This is a comment
```

## Whitespace

Arbitrary whitespace may be inserted between tokens.

```
let number A = 0
   ^      ^ ^ ^
// Valid whitespace locations

let   number   A   =   0

let
number
A
=
0
```

Whitespace must not be inserted inside a token.

```
l e t number A = 0
// Error: invalid syntax
```

Separating statements with newlines is recommended, but not required.

```
let number A = 0 let number B = 1
```

## Errors

Syntax errors occur when a Yovec program has invalid syntax.

```
let vector V = [0, 1, 2
// Error: missing closing bracket
```

Transpilation errors occur when a program performs illegal operations during transpilation.

```
let number A = 0
let vector V = A
// Error: cannot assign number to vector
```

Undefined behaviour occurs when a program performs illegal operations at runtime. Anything may happen!

```
// Yovec
import n
let variable A = 1/$n
export A

// YOLOL: assume n == 0
a=1/n
// Uh oh!
```
