.PHONY: install check test

all: check test

install:
	pip3 install --user -r requirements.txt

check:
	pyre check

test:
	pytest
