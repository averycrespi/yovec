.PHONY: develop check test

all:
	@echo 'Please choose a make target from: develop, check, test'

develop:
	pip3 install -e .

check:
	pyre check

test:
	@python3 tools/test.py
