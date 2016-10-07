#!/usr/bin/env python3

import os
import sys
sys.path.insert(0, os.path.abspath("../.."))
from gitlab_build_scripts.metadata import General

extensions = [
    'sphinx.ext.autodoc',
]

templates_path = ['.templates']
source_suffix = '.rst'
master_doc = 'index'

# noinspection PyShadowingBuiltins
copyright = '2016, Hermann Krumrey'
author = 'Hermann Krumrey'
project = 'gitlab-build-scripts'

version = General.version_number
release = General.version_number

language = None
exclude_patterns = []
pygments_style = 'sphinx'
todo_include_todos = False

html_theme = 'alabaster'
html_static_path = ['.static']
htmlhelp_basename = 'gitlab-build-scriptsdoc'

latex_elements = {
}
latex_documents = [
    (master_doc, 'gitlab-build-scripts.tex', 'gitlab-build-scripts Documentation',
     'Hermann Krumrey', 'manual'),
]

man_pages = [
    (master_doc, 'gitlab-build-scripts', 'gitlab-build-scripts Documentation',
     [author], 1)
]

texinfo_documents = [
    (master_doc, 'gitlab-build-scripts', 'gitlab-build-scripts Documentation',
     author, 'gitlab-build-scripts', 'One line description of project.',
     'Miscellaneous'),
]

epub_title = project
epub_author = author
epub_publisher = author
epub_copyright = copyright
epub_exclude_files = ['search.html']

intersphinx_mapping = {'https://docs.python.org/': None}

from sphinx.ext.autodoc import between


def skip(app, what, name, obj, skipper, options):
    str(app)
    str(what)
    str(obj)
    str(options)
    if name == "__init__":
        return False
    return skipper


def setup(app):
    # Register a sphinx.ext.autodoc.between listener to ignore everything
    # between lines that contain the word IGNORE
    app.connect('autodoc-process-docstring', between('^.*LICENSE.*$', exclude=True))
    app.connect("autodoc-skip-member", skip)
    return app
