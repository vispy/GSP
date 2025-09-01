##########################################################################
# Makefile for GSP project


##########################################################################
# Test targets

test:
	cd tests
	pytest

test_verbose:
	cd tests
	pytest -v

##########################################################################

examples_output_force_commit:
	git add -f examples/output
	git commit -m "Force commit of recent examples/output images"

##########################################################################
# Documentation targets
#

doc_build:
	# Build the documentation using MkDocs
	mkdocs build

doc_deploy:
	# Deploy the documentation to GitHub Pages
	mkdocs gh-deploy

doc_open: doc_build
	# Open the documentation in the default web browser
	open site/index.html

doc_serve:
	# Serve the documentation locally - useful for development - open in browser with http://localhost:8000
	mkdocs serve