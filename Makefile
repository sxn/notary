.PHONY: tests

tests:
	python -m pytest

release:
	python setup.py sdist bdist_wheel upload
