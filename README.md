# yovec

`yovec` is a functional, vector-based language that transpiles to [YOLOL](https://wiki.starbasegame.com/index.php/YOLOL).

Note: `yovec` is currently in development, so the language may change **without warning**. Stay tuned for the v1.0 release!

## Requirements

- Python 3.7 (or greater)
- Lark parser (`pip3 install lark-parser`)

## Why?

Would you rather write this ...

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

... or this?

```
v0e0=1 v0e1=2 v0e2=3
v1e0=n+1 v1e1=n+2 v1e2=n+3
v2e0=(v0e0-v1e0)^2 v2e1=(v0e1-v1e1)^2 v2e2=(v0e2-v1e2)^2
v3e0=v2e0+v2e1+v2e2
dist0=v3e0^0.5
```

## How?

Clone this repo, then run `python3 yovec.py source > out`
