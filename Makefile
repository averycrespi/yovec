.PHONY: build clean install check test

all: build

build:
	pyinstaller yovec.spec

clean:
	rm -rf build dist

install:
	pip3 install --user lark-parser pyre-check pyinstaller
	pip3 install -e .

check:
	pyre check

test:
	@python3 tools/test.py
