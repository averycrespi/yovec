<h1 align="center">
    <br>
    <img src="https://raw.githubusercontent.com/averycrespi/yovec/master/images/logo_full.png" width="200"</img>
    <br>
    Yovec
    <br>
</h1>

<h4 align="center">A functional, vector-based language that transpiles to <a href="https://wiki.starbasegame.com/index.php/YOLOL">YOLOL</a>.</h4>

<p align="center">
    <a href="#what-is-yovec">What</a> •
    <a href="#why-should-i-use-yovec">Why</a> •
    <a href="#how-do-i-get-started">How</a> •
    <a href="#faq">FAQ</a> •
	<a href="#license">License</a>
</p>

## What is Yovec?

Yovec is a specialized language for working with vectors (arrays of numbers).

Vectors are extremely useful in [Starbase](https://starbasegame.com/) for navigation and targeting.

## Why should I use Yovec?

#### Simplicity

Complex YOLOL code can be difficult to understand.

Yovec has simple, declarative syntax that's friendly to beginners.

```
import n
let vector V = [$n, 2, 3]
let number A = V dot V
export A
```

#### Convenience

YOLOL doesn't support arrays, so each array element must be a separate variable.

Yovec handles vector expansion so that you don't have to.

```
// YOLOL
v0=1 v1=2 v2=4 v3=8 v4=16 v5=32

// Yovec
let vector V = [1, 2, 4, 8, 16, 32]
```

#### Efficiency

YOLOL chips execute slowly and have a limited amount of space.

Yovec aggressively optimizes your code to make it faster and smaller.

```
// Without optimization: 255 characters
> python3 yovec-cli.py -i programs/axis.yovec --no-elim --no-reduce --no-mangle | wc -c
255

// With optimization: 105 characters
$ python3 yovec-cli.py -i programs/axis.yovec | wc -c
105
```

## How do I get started?

#### Install the guided user interface: Linux only

Download and run the latest [release](https://github.com/averycrespi/yovec/releases/latest).

#### Install the command line interface: Windows, Mac OS, and Linux

Requires [Git](https://git-scm.com/) and [Python 3.5+](https://www.python.org/).

```bash
# Clone the repository
git clone https://github.com/averycrespi/yovec.git && cd yovec

# Install dependencies
pip3 install --user -r requirements.txt

# Run the Yovec CLI
python3 yovec-cli.py
```

#### Learn Yovec

To learn the Yovec language, check out some [example programs](programs/) or read the [language specification](docs/spec.md).

## FAQ

**Q**: Why is the output of Yovec empty?

**A**: If no variables are exported, Yovec will eliminate the entire program. Export a variable or disable dead code elimination.

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

---

**Q**: Why is the GUI only available for Linux?

**A**: PyInstaller cannot cross-compile executables. For Windows and Mac OS, use the CLI instead.

## License

[AGPLv3](https://choosealicense.com/licenses/agpl-3.0/)
