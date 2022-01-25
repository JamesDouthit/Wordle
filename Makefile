SOURCE_CODE=wordle-solver

deps:
	pip install -e .
	pip install -r requirements.txt

test:
	nosetests --cover-package $(SOURCE_CODE) --with-coverage
