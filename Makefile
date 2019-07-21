.PHONY: build clean develop check test

all:
	@echo 'Please choose a make target from: build, clean, develop, check, test'

build:
	pyinstaller yovec.spec

clean:
	rm -rf build dist

develop:
	pip3 install --user pyre-check pyinstaller
	pip3 install -e .

check:
	pyre check

test:
	@python3 tools/test.py
