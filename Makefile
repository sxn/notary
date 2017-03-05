.PHONY: tests

tests:
	python -m pytest

coverage:
	python -m codecov

release:
	python setup.py sdist bdist_wheel upload
