all: clean
	python setup.py build

install: clean
	python setup.py install

sdist: clean
	LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8 python setup.py sdist upload

clean:
	rm -fr build dist *.egg-info pyAMI/*.pyc
