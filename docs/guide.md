# Yovec Language Guide

## Table of Contents

- [Terminology](#terminology)
- [General Notes](#general-notes)
- [Numbers](#numbers)
- [Vectors](#vectors)
- [Matrices](#matrices)
- [Imports](#imports)
- [Exports](#exports)
- [Comments](#comments)
- [Errors](#errors)
- [Limitations](#limitations)

## Terminology

- An **alias** is an alternative identifier for an external or variable
- An **external** is a value which has been imported from YOLOL
- A **function** performs an operation on values
- A **literal** is a fixed numeric value, such as `0`
- A **matrix** is a non-empty sequence of vectors
- A **number** is a limited-precision decimal
- A **variable** stores a number, vector, or matrix
- A **vector** is a non-empty sequence of numbers

## General Notes

Yovec does not have function precedence. All functions are evaluated left-to-right. Parentheses must be used to enforce precedence.

```
1 + 2 * 3 / 4
// Evaluates as ((1 + 2) * 3) / 4

1 + (2 * (3 / 4))
// Evaluates as 1 + (2 * (3 / 4))
```

Yovec is a functional language. All objects are immutable. Variables may not be updated after definition.

Yovec is 0-indexed.

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
- `abs A`: calculate the absolute value of `A`
- `sqrt A`: calculate the square root of `A`
- `sin A`: calculate the sine of `A` (in degrees)
- `cos A`: calculate the cosine of `A` (in degrees)
- `tan A`: calculate the tangent of `A` (in degrees)
- `arcsin A`: calculate the inverse sine of `A` (in degrees)
- `arccos A`: calculate the inverse cosine of `A` (in degrees)
- `arctan A`: calculate the inverse tangent of `A` (in degrees)
- `csc A`: calculate the cosecant of `A` (in degrees)
- `sec A`: calculate the secant of `A` (in degrees)
- `cot A`: calculate the cotangent of `A` (in degrees)
- `arccsc A`: calculate the inverse cosecant of `A` (in degrees)
- `arcsec A`: calculate the inverse secant of `A` (in degrees)
- `arccot A`: calculate the inverse cotangent of `A` (in degrees)
- `ln A`: approximate the natural logarithm of `A`

Certain unary functions may cause undefined behaviour:

- `sqrt A` where `A < 0`
- `ln A` where `A < 0`
- Trig. functions where the operand is outside of the domain

Binary functions operate on two numbers:

- `A + B`: add `A` and `B` (commutative)
- `A - B`: subtract `B` from `A`
- `A * B`: multiply `A` by `B` (commutative)
- `A / B`: divide `A` by `B`
- `A % B`: calculate the modulus of `A` and `B`
- `A ^ B`: raise `A` to the power of `B`
- `A < B`: return `1` if `A` is less than `B`, otherwise `0`
- `A <= B`: return `1` if `A` is less than or equal to `B`, otherwise `0`
- `A > B`: return `1` if `A` is greater than `B`, otherwise `0`
- `A >= B`: return `1` if `A` is greater than or equal to `B`, otherwise `0`
- `A == B`: return `1` is `A` is equal to `B`, otherwise `0` (commutative)
- `A != B`: return `1` is `A` is not equal to `B`, otherwise `0` (commutative)

Certain binary functions may cause undefined behaviour:

- `A / 0`
- `A % 0`
- `0 ^ -1`

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
let vector X = [6, 7, 8]

apply + V W
// Returns [9, 12, 15]

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
```

The `map` function maps a function element-wise to a matrix.

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
apply + M N

apply * M N O
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

The `*` function multiples two matrices. The number of columns in the first matrix must be equal to the number of rows in the second matrix.

```
M * N
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
```

The `row` function gets a row of a matrix by index. The index must be a literal.

```
let matrix M = [
	[0, 1, 2],
	[3, 4, 5]
]

row M 0
// Returns [0, 1, 2]
```

The `col` function gets a column of a matrix by index. The index must be a literal.

```
let matrix M = [
	[0, 1, 2],
	[3, 4, 5]
]

col M 0
// Returns [0, 3]
```

## Imports

The `import` statement imports external values from YOLOL.

An external value must be a valid number. Importing a string causes undefined behaviour.

Imported names must not include uppercase letters, and must be valid [YOLOL identifiers](https://wiki.starbasegame.com/index.php/YOLOL#Variables).

Imported names must be prefixed with `$` when used.

```
import n

let variable A = $n + 1
```

Imported names may optionally be aliased.

```
import long_name as n

let variable A = $n + 1
```

## Exports

The `export` statement exports variables to YOLOL.

Exported names must not included uppercase letters, and must be valid [YOLOL identifiers](https://wiki.starbasegame.com/index.php/YOLOL#Variables).

```
let number N = 0
export N as num
// Result: num_0=0

let vector V = [0, 1, 2]
export V as vec
// Result: vec_0=0 vec_1=1 vec_2=2

let matrix M = [
    [0, 1, 2],
    [3, 4, 5]
]
export M as mat
// Result: mat_0_0=0 mat_0_1=1 mat_0_2=2 mat_1_0=3 mat_1_1=4 mat_1_2=5
```

## Comments

A comment must start with `//` and must be on its own line.

```
// This is a comment
```

## Errors

Syntax errors occur when a program has invalid Yovec syntax.

```
let vector V = [0, 1, 2
// Missing closing bracket
```

Transpilation errors occur when a program performs illegal operations during transpilation.

```
let number A = 0
let vector V = A
// Cannot assign number to vector
```

Undefined behaviour occurs when a program performs illegal operations at runtime. Anything may happen!

```
n0 = 1 / 0
// Generated YOLOL divided by zero
```

## Limitations
