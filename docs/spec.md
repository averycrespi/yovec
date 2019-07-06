# Yovec Language Specification

## Types

#### Numbers

Yovec numbers are limited-precision decimals (like [YOLOL](https://wiki.starbasegame.com/index.php/YOLOL#Decimals)).

```
0
200
1.0
-3
1.2345
A
LONG_NAME
$n
```

```
// Bad: too many decimal places
1.23456
```

Unary operations are evaluated right-to-left.

- Functions: `neg`, `abs`, `sqrt`, `sin`, `cos`, `tan`, `arcsin`, `arccos`, `arctan`

```
// Evaluates as sin(cos(0))
sin cos 0
```

Binary operations are evaluated left-to-right. Use parentheses to enforce precedence.

Logical operations return `0` (if false) or `1` (if true).

- Arithmetic: `+`, `-`, `*`, `/`, `%`, `^`
- Logic: `<`, `<=`, `>`, `>=`, `==`, `!=`

```
1 + 2 - 3
4 ^ (8 + 7)
7 < 3
A + 1
3 % $n
```

```
// Bad: missing second operand
1 +
```

#### Vectors

Yovec vectors are ordered sequences of numbers.

```
[0]
[1, 2, 3]
[A, $n]
```

```
// Bad: empty vector
[]
```

The `map` function applies operations element-wise to a vector.

```
map abs [0, -1, 1]
map +1 V
map 1+ V
```

The `concat` function concatenates vectors.

```
concat V W X
```

The `reduce` function reduces a vector to a number.

```
reduce + V
```

The binary operator `dot` calculates the dot product of two vectors.

```
V dot W
```

The binary operators `+` and `-` add and subtract vectors element-wise.

```
V + W - X
```

The `len` function returns the length of a vector.

```
len V
```

#### Matrices

Yovec matrices are ordered sequences of vectors. Each vector in a matrix is treated as a row, and all vectors must have the same length.

```
[
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]
```

```
// Bad: mismatching lengths
[
    [1, 2],
    [3, 4, 5]
]
```

```
// Bad: empty matrix
[]
```

The `map` function applies operations element-wise to a matrix.

```
map abs M
map +1 M
map 1+ M
```

The transpose function switches the rows and columns of a matrix.

````
transpose M
````

The binary operators `+` and `-` add and subtract matrices element-wise.

```
M + N - O
```

The `rows` function returns the number of rows in a matrix.

```
rows M
```

The `cols` function returns the number of columns in a matrix.

```
cols M
```

The binary operation `*` performs matrix multiplication. The number of columns in the first matrix must be equal to the number of rows in the second matrix.

```
M * N
```

## Statements

#### Let

`let` statements assign to number, vector, and matrix variables. Variable names must be upper-case, but can include underscores.

```
let number N = 0
let vector V = [1, 2, N]
let matrix M = [
    [1, 2, 3],
    [4, 5, 6]
]
let number LONG_NAME = 1
```

```
// Bad: lowercase letters in variable name
let number camelCase = 1
```

#### Import

`import` statements allow external YOLOL variables to be used as numbers. External names cannot contain uppercase letters. External names can optionally be aliased.

**WARNING**: Yovec assumes that externals are constant numbers. Importing a string will cause undefined behaviour. Importing a dynamic number will cause undefined behaviour.

```
import n
import :foo
import long_name
import a123
```

```
// Alias: external is called "long_name", but will be addressed as "n"
import long_name as n
```

```
// Bad: uppercase letters in external name
import N
```

After being imported, externals must be prefixed with a `$`.

```
import n
let number A = $n + 1
```

```
// Bad: missing $
import n
let number A = n + 1
```

#### Export

`export` statements allow Yovec variables to be used in YOLOL. The YOLOL variable names will be prefixed with the provided alias.

```
export N as count
export V as dist
export M as data
```

```
// Bad: uppercase letters in alias name
export N as COUNT
```

#### Comments

Comments start with `//` and must be on their own line.

```
// This is a comment
```

```
// Bad: inline comment
let number A = 0    // Inline comment
```

## Errors

#### Compile time

Syntax errors (e.g missing bracket) will halt compilation and print a message.

```
let vector V = [1, 2, 3
```

Type errors (e.g. adding a vector and a number) will halt compilation and print a message.

```
let vector V = 0 + [1, 2, 3]
```

If no errors are raised during compilation, Yovec will always generate syntactically-valid YOLOL.

#### Runtime

Some operations can cause runtime errors when the output YOLOL is interpreted:

- Dividing by 0
- Calculating the modulus of a number with 0
- Raising 0 to the power of -1
- Calling `arccos` or `arcsin` with a number outside of the range `[-1, 1]`
