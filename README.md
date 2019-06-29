# githeatmap


## Testing

Tox is being used for multiversion testing. Tests are run on python 2.7 and 3.6. You should have
both of these installed locally. To run tests, install the requirements.txt and then run tox.

```
$ pip install -r requirements.txt
$ tox
```

To get code coverage information, you can run pytest directly.

```
$ pip install -r requirements.txt
$ pytest --cov=src --cov-report=html
```

This will generate an html coverage report in `htmlcov/` directory.
