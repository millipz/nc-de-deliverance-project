import os
import sys
import ast

def extract_docstrings(file_path):
    with open(file_path, 'r') as f:
        tree = ast.parse(f.read())

    docstrings = []

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if node.body and isinstance(node.body[0], ast.Expr) and isinstance(node.body[0].value, ast.Str):
                docstrings.append({
                    'name': node.name,
                    'docstring': node.body[0].value.s
                })

    return docstrings

def write_to_single_markdown(docstrings, output_file):
    with open(output_file, 'w') as f:
        for item in docstrings:
            f.write(f"# {item['name']}\n\n")
            f.write(f"{item['docstring']}\n\n")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python extract_and_merge_docstrings.py <path_to_python_file> <output_markdown_file>")
        sys.exit(1)

    file_path = sys.argv[1]
    output_file = sys.argv[2]

    docstrings = extract_docstrings(file_path)
    write_to_single_markdown(docstrings, output_file)

    print(f"Docstrings merged into: {output_file}")