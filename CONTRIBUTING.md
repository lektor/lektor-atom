# Contributing

## Development environment

Create a development environment with `Python>=3.6`.

You can then install the development and test dependencies with:

```bash
python -m pip install lektor
python -m pip install --editable .[test]
```

## Tests

To run the test suite, we use `pytest`:

```bash
pytest . --tb=long -svv
```

## Pre-commit

We use precommit hooks to ensure code style and format.

Install `precommit` from pip

```bash
pip install pre-commit
pre-commit install
```

Now after each commit, the style hooks will run and auto format the code.

You can also manually run the pre-commit hooks without a commit with `pre-commit run -a`.
