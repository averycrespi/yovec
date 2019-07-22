# Yovec Tutorial

Welcome to Yovec! In this tutorial, you're going to write your first Yovec program.

## Defining coordinates

You want to find the distance between your ship and a starbase.

Space is 3-dimensional, so we need `x`, `y`, and `z` coordinates.

The position of the starbase is fixed. Let's use `-500`, `10`, and `50`.

The position of your ship changes, so we need to import variables from YOLOL.

Assume the YOLOL variables `x`, `y`, and `z` hold the current position of your ship.

```
import x, y, z
let vector SHIP = [$x, $y, $z]
let vector BASE = [-500, 10, 50]
```

## Using the distance formula

Next, we need to know the [distance formula](https://en.wikipedia.org/wiki/Euclidean_distance#Three_dimensions).

The distance formula has 4 steps:

1) Subtract the coordinates, element by element
2) Square the results of the subtractions
3) Add all of the results together
4) Take the square root of the sum

#### Step 1: subtract the coordinates

To perform element-wise subtraction, we can use `-`.

```
// Subtract SHIP and BASE, element by element
let vector V = SHIP - BASE
```

#### Step 2: square the results

To square the results, we can use the `map` statement to apply a function to a vector.

```
// Square each element of V
let vector W = map ^2 V
```

#### Step 3: add the results together

To add all of the results into a single number, we can use the `reduce` function with `+`.

```
// Add the elements of W together to make a single number
let number A = reduce + W
```

#### Step 4: take the square root

To take the square root of a number, we can use the `sqrt` function.

```
// Take the square root of A
let number B = sqrt A
```

## Exporting the result

Yovec automatically removes all "dead" (unused) code. To use the result, we need to export it.

```
// Export B and call it "dist"
export B as dist
```

## Putting it all together

The whole program (without comments) looks like this:

```
import x, y, z
let vector SHIP = [$x, $y, $z]
let vector BASE = [-500, 10, 50]
let vector V = SHIP - BASE
let vector W = map ^2 V
let number A = reduce + W
let number B = sqrt A
export B as dist
```

You're done! Run this program through Yovec, and you'll get YOLOL that you can run in-game.
