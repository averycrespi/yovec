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
    <a href="#getting-started">Getting Started</a> •
	<a href="#development">Development</a> •
	<a href="#license">License</a>
</p>

## Features

- Simple, declarative syntax
- Supports numbers, vectors, and matrices
- Interoperable with YOLOL

Input:

```
// Calculate the Euclidean distance between two vectors.

import n

let vector A = [1, 2, 3]
let vector B = [$n, $n, $n]
let vector C = map ^2 (A - B)
let vector D = [reduce + C]
let vector E = map sqrt D

export E as dist
```

Output:

```
v0e0=1 v0e1=2 v0e2=3
v1e0=n+1 v1e1=n+2 v1e2=n+3
v2e0=(v0e0-v1e0)^2 v2e1=(v0e1-v1e1)^2 v2e2=(v0e2-v1e2)^2
v3e0=v2e0+v2e1+v2e2
dist_0=sqrt v3e0
```

## Getting Started

To run Yovec, you'll need [Git](https://git-scm.com/), [Make](https://www.gnu.org/software/make), and [Python 3.5](https://www.python.org/) (or newer).

```bash
# Clone the repository
git clone https://github.com/averycrespi/yovec.git && cd yovec

# Install dependencies
make install

# Run Yovec
python3 yovec.py -i in.yovec -o out.yolol
```

To learn the Yovec language, check out some [example programs](programs/) or read the [language guide](docs/guide.md).

## Development

After cloning the repository, run `make develop` to setup a development environment.

Run `make test` to run tests, and `make check` to check type annotations.

## License

[AGPLv3](https://choosealicense.com/licenses/agpl-3.0/)
