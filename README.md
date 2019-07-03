# yodsl

`yodsl` is a collection of DSLs (domain-specific languages) that transpile to [YOLOL](https://wiki.starbasegame.com/index.php/YOLOL).

## yovec

`yovec` is a functional, vector-based DSL that transpiles to YOLOL.

Example:

```
// Calculate the Euclidean distance between two vectors.

import n

let A = [1, 2, 3]
let B = [$n + 1, $n + 2, $n + 3]
let C = map ^2 (A - B)
let D = [reduce + C]
let E = map ^0.5 D

export E as dist
```

Output:

```
v0e0=1 v0e1=2 v0e2=3
v1e0=n+1 v1e1=n+2 v1e2=n+3
v2e0=(v0e0-v1e0)^2 v2e1=(v0e1-v1e1)^2 v2e2=(v0e2-v1e2)^2
v3e0=v2e0+v2e1+v2e2
dist0=v3e0^0.5
```
