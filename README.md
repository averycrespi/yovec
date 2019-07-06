<h1 align="center">
    <br>
    <img src="https://raw.githubusercontent.com/averycrespi/yovec/master/images/logo_full.png" width="200"</img>
    <br>
    Yovec
    <br>
</h1>

<h4 align="center">A functional, vector-based language that transpiles to <a href="https://wiki.starbasegame.com/index.php/YOLOL">YOLOL</a>.</h4>

<p align="center">
    <a href="#features">Features</a> •
    <a href="#example">Example</a> •
    <a href="#how-to-use">How to Use</a> •
	<a href="#license">License</a>
</p>

## Features

- Simple, unambiguous syntax
- Supports numbers, vectors, and matrices
- Interoperable with YOLOL (via imports and exports)

## Example

```
// Calculate the Euclidean distance between two vectors.

import n

let vector A = [1, 2, 3]
let vector B = [$n + 1, $n + 2, $n + 3]
let vector C = map ^2 (A - B)
let vector D = [reduce + C]
let vector E = map sqrt D

export E as dist
```

## How to Use

To clone and run Yovec, you'll need [Git](https://git-scm.com/) and [Python 3.5 (or newer)](https://www.python.org/).

```bash
# Clone the repository
git clone https://github.com/averycrespi/yovec.git

# Install dependencies
pip3 install lark-parser

# Run Yovec
python3 yovec.py in.yovec > out.yolol
```

## License

[AGPLv3](https://choosealicense.com/licenses/agpl-3.0/)
