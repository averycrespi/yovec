.PHONY: check

all: check

install:
	pip3 install --user -r requirements.txt

check:
	pyre check
