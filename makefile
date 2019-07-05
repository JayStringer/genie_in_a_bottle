.PHONY: all
all: package-py

# Update Dev Environment - called by build.sh by default
##########################################################
.PHONY: update-dev-env
update-dev-env:
	pip install -e .


# Python Packaging
##########################################################
.PHONY: package-py
package-py:
	python setup.py sdist
