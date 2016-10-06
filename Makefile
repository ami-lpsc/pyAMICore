all: clean
	python setup.py build

install: clean
	python setup.py install

sdist: clean
	python setup.py sdist upload

clean:
	rm -fr build dist *.egg-info pyAMI/*.pyc
