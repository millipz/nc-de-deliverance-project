# conf.py
# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys
from recommonmark.transform import AutoStructify
from recommonmark.parser import CommonMarkParser
sys.path.insert(0, os.path.abspath('../python/src/ingestion_function'))

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'docs'
copyright = '2024, azmol'
author = 'azmol, prubh'
release = '1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'recommonmark',
    'sphinx_markdown_tables',
]

source_suffix = ['.rst', '.md']
source_parsers = {
    '.md': CommonMarkParser,
}

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
# Enable the AutoStructify transform to process your markdown files
def setup(app):
    app.add_config_value('recommonmark_config', {
            'url_resolver': lambda url: 'https://github.com/millipz/nc-de-deliverance-project',
            'auto_toc_tree_section': 'Contents',
        }, True)
    app.add_transform(AutoStructify)