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
    <a href="#installation">Installation</a> •
    <a href="#learning">Learning</a> •
    <a href="#faq">FAQ</a> •
	<a href="#license">License</a>
</p>

## Features

- Simple, declarative syntax
- Supports numbers, vectors, and matrices
- Interoperable with YOLOL

<p>
    <img src="https://raw.githubusercontent.com/averycrespi/yovec/master/images/gui.png" width="400"</img>
</p>

## Installation

#### Guided User Interface: Linux only

Download and run the latest Linux GUI [release](https://github.com/averycrespi/yovec/releases/latest).

#### Command Line Interface: Windows, Mac OS, or Linux

Requires [Git](https://git-scm.com/) and [Python 3.5+](https://www.python.org/).

```bash
# Clone the repository
git clone https://github.com/averycrespi/yovec.git && cd yovec

# Install parser
pip3 install --user lark-parser

# Run the Yovec CLI
python3 yovec-cli.py -i source.yovec -o out.yolol
```

## Learning

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

## License

[AGPLv3](https://choosealicense.com/licenses/agpl-3.0/)
