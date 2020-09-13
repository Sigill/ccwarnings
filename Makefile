dependencies:
	pip install -r requirements.txt

dependencies-all: dependencies
	pip install flake8

test:
	./test/test.py

package:
	python setup.py bdist_wheel --universal

flake8:
	flake8 . --count --exit-zero --max-complexity=10 --max-line-length=150 --per-file-ignores='test/test.py:E402' --exclude venv*

.PHONY: dependencies dependencies-all test package flake8