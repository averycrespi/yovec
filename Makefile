.PHONY: build clean install develop check test

all:
	@echo 'Please choose a make target from: build, clean, install, develop, check test'

build:
	pyinstaller yovec.spec

clean:
	rm -rf build dist

install:
	pip3 install --user lark-parser

develop:
	pip3 install --user pyre-check pyinstaller
	pip3 install -e .

check:
	pyre check

test:
	@python3 tools/test.py
