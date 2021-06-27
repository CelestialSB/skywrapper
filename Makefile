all: build sign

clean:
	rm -vfr dist *.egg-info build docs/build/*

requires:
	pip3 install -r requirements-dev.txt

build: requires
	python3 -m build

sign:
	@for pkg in $(wildcard dist/*); do	\
    	echo "Signing $$pkg";			\
    	gpg2 --detach-sign -a $$pkg;	\
    done

upload-test:
	twine upload -r testpypi dist/* --verbose

.PHONY: docs-serve
docs-serve: requires
	cd docs && make serve

.PHONY: docs
docs: requires
	cd docs && make html
