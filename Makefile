.PHONY: build clean install check test

all: build

build:
	pyinstaller -F yovec.py

clean:
	rm -rf build dist yovec.spec

install:
	pip3 install --user lark-parser pyre-check pyinstaller
	pip3 install -e .

check:
	pyre check

test:
	@python3 tools/test.py
