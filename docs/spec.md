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
```

```
// Bad: too many decimal places
1.23456
```

Unary operations are evaluated right-to-left.

- Functions: `neg`, `abs`, `sqrt`, `sin`, `cos`, `tan`, `arcsin`, `arccos`, `arctan`.

```
// Evaluates as sin(cos(0))
sin cos 0
```

Binary operations are evaluated left-to-right. Use parentheses to enforce precedence.

Logical operations return `0` (if false) or `1` (if true).

- Arithmetic: `+`, `-`, `*`, `/`, `%`, `^`.
- Logic: `<`, `<=`, `>`, `>=`, `==`, `!=`.

```
1 + 2
4 ^ (8 + 7)
7 < 3
```

```
// Bad: missing second operand
1 +
```

#### Vectors

#### Matrices

## Statements

#### Let

#### Import

#### Export

#### Comments

## Minutiae
