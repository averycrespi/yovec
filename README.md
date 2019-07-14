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

Turns this ...

```
import n

let matrix M = [
    [$n, 1],
    [2, 3]
]

let matrix N = M * M

export N as product
```

... into this:

```
product_r0c0=n*n+2 product_r0c1=3+n product_r1c0=2*n+6 product_r1c1=11
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
