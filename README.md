
# Graphic Server Protocol (GSP)

The Graphic Server Protocol (GSP) defines the protocol used between a visualization library or a visualization software a language server that provides graphical features.

## How to install the project

Potentially create a virtual environment

```bash
python -m venv venv
source venv/bin/activate
```

To install the project itself, you can use pip:

```bash
pip install -e .
```

## How to test the project

To test the project, you can use the provided Makefile. Here are the available commands:

- `make test`: Run the tests using pytest.
- `make test_verbose`: Run the tests with verbose output.

## How to build the documentation

To build the documentation, you can use the provided Makefile. Here are the available commands:

- `make doc_build`: Build the documentation using MkDocs.
- `make doc_deploy`: Deploy the documentation to GitHub Pages.
- `make doc_open`: Open the documentation in the default web browser.
- `make doc_serve`: Serve the documentation locally.