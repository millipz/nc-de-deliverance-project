# Comments and Documentation

- Write docstrings for each function _before_ writing any tests or code. This will define the arguments, output format, and any possible errors the function can be expected to raise.
- Use type hinting wherever possible to assist in code completion and type checking
- We will use the Google format of docstring:

```py
def myfunc(param1: str, param2: int) -> dict(float):
    """
    This is an example of Google style.

    Args:
        param1: This is the first param.
        param2: This is a second param.

    Returns:
        This is a description of what is returned.

    Raises:
        KeyError: Raises an exception.
    """
    pass
```

- We will use [pdoc](https://pdoc.dev) to create documentation from docstrings