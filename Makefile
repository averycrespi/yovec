.PHONY: install develop check test

all:
	@echo "Please specify a target: install, develop, check, test"

install:
	pip3 install --user -r requirements.txt

develop:
	pip3 install --user pyre-check
	pip3 install -e .

check:
	pyre check

test:
	@python3 tools/test.py
