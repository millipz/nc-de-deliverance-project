# Comments and Documentation

- Write docstrings for each function _before_ writing any tests or code. This will define the arguments, output format, and any possible errors the function can be expected to raise.
- Use type hinting wherever possible to assist in code completion and type checking.
- We will use the Google format of docstring:

```python
def myfunc(param1: str, param2: int) -> dict[float]:
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
## Steps

#### 1. Create doc_src Folder: Create a folder named doc_src for source documentation.

#### 2. Create docs Folder: Create a folder named docs for generated documentation.
Then install [mkdocs](https://www.mkdocs.org/) to create documentation from docstrings

#### 3. Create mkdocs.yml File: Create a file named mkdocs.yml in the root of the project folder.

#### 4. Add the following YAML configuration in mkdocs.yml:

```
yaml
Copy code
site_name: Team Deliverance Totesys Documentation
docs_dir: doc_src

nav:
  - Home: index.md
  - Ingestion:
      - Ingestion Lambda Utils: ingestion/lambda_utils.md
  - Processing:
      - Processing Lambda Utils: processing/lambda_utils.md
  - Loading:
      - Loading Lambda Utils: loading/lambda_utils.md
theme:
  name: material
```

#### 5. Extract and Merge Ingestion Docstrings:
Run the command `python scripts/extract_and_merge_docstrings.py python/src/ingestion_function/lambda_utils.py doc_src/ingestion/lambda_utils.md`.

#### 6. Extract and Merge Processing Docstrings:
Run the command `python scripts/extract_and_merge_docstrings.py python/src/processing_function/lambda_utils.py doc_src/processing/lambda_utils.md`.

#### 7. Extract and Merge Loading Docstrings:
Run the command `python scripts/extract_and_merge_docstrings.py python/src/loading_function/lambda_utils.py doc_src/loading/lambda_utils.md`.

#### 8. Build HTML Documentation:
Run the command `mkdocs build -d docs` to generate the documentation in HTML format.

#### 9. Preview Documentation Locally:
Use `mkdocs serve` to preview the documentation locally.