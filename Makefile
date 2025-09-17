# Makefile for GSP project

help: ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sed 's/:.*##/:/' | column -t -s:


# Test targets

test: ## Run all tests
	cd tests
	pytest

test_verbose: ## Run all tests with verbose output
	cd tests
	pytest -v

test_examples:
	(cd examples && python run_all_examples.py)


# Linting targets

lint_checker: lint_checker_src lint_checker_examples ## Run lint checker on source and examples
	@echo "Linting completed."

lint_checker_src: ## Run lint checker on source files
	pyright gsp/**/*.py

lint_checker_examples: ## Run lint checker on example files
	pyright examples/**/*.py


# ./examples/output is gitignored, so we need to force add and commit any changes

examples_output_force_commit: ## Force add and commit changes in examples/output
	git add -f examples/output
	git commit -m "Force commit of recent examples/output images"


# Documentation targets

doc_build: ## Build the documentation using MkDocs
	# Build the documentation using MkDocs
	mkdocs build

doc_deploy: ## Deploy the documentation to GitHub Pages
	# Deploy the documentation to GitHub Pages
	mkdocs gh-deploy

doc_open: doc_build ## Open the built documentation in the default web browser
	# Open the documentation in the default web browser
	open site/index.html

doc_serve: ## Serve the documentation locally - useful for development
	# Serve the documentation locally - useful for development - open in browser with http://localhost:8000
	mkdocs serve