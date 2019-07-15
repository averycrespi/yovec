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
    <a href="#faq">FAQ</a> •
	<a href="#development">Development</a> •
	<a href="#license">License</a>
</p>

## Features

- Simple, declarative syntax
- Supports numbers, vectors, and matrices
- Interoperable with YOLOL

Turns this ...

```
// Determine which axis a vector should be routed to.

import vx, vy, vz

let number X = abs $vx
let number Y = abs $vy
let number Z = abs $vz

let vector AXIS = [
    $vx * ((X >= Y) and (X >= Z)),
    $vy * ((Y > X) and (Y >= Z)),
    $vz * ((Z > X) and (Z > Y))
]

export AXIS
```

... into this:

```
a=abs vx b=abs vy c=abs vz axis_e0=vx*(a>=b and a>=c)
axis_e1=vy*(b>a and b>=c) axis_e2=vz*(c>a and c>b)
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

## FAQ

**Q**: Why is the output of Yovec empty?

**A**: If no variables are exported, Yovec will eliminate the entire program. Export a variable, or use `--no-elim` to disable dead code elimination.

---

**Q**: What's the difference between `map` and `apply`?

**A**: `map` works with unary functions (e.g. `map neg`), and with binary functions where one operand is "empty" (e.g. `map 1+`). `apply` works with binary functions where both operands are "empty" (e.g. `apply +`)

---

**Q**: Why doesn't Yovec support conditionals?

**A**: YOLOL conditionals take up large amounts of space on a line. Evaluating a conditional for each element of a vector would quickly fill an entire chip.

---

**Q**: Why do indices have to be literals?

**A**: All indexing operations must be resolved at compile time. Variable indices would require conditionals.

---

**Q**: Why is there no `filter` function?

**A**: `filter` would return a vector of variable length. Variable-length vectors would require conditionals.

## Development

After cloning the repository, run `make develop` to setup a development environment.

Run `make test` to run tests, and `make check` to check type annotations.

## License

[AGPLv3](https://choosealicense.com/licenses/agpl-3.0/)
