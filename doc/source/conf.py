#!/usr/bin/env python3

import os
import sys
# noinspection PyPackageRequirements
import sphinx_rtd_theme
# noinspection PyPackageRequirements
from sphinx.ext.autodoc import between

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

# HTML Config
html_theme = 'sphinx_rtd_theme'
html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]
html_static_path = ['.static']
htmlhelp_basename = 'gitlab-build-scriptsdoc'

# Latex
latex_elements = {
}
latex_documents = [
    (master_doc, 'gitlab-build-scripts.tex', 'gitlab-build-scripts Documentation',
     'Hermann Krumrey', 'manual'),
]

# Man Pages
man_pages = [
    (master_doc, 'gitlab-build-scripts', 'gitlab-build-scripts Documentation',
     [author], 1)
]

# Tex
texinfo_documents = [
    (master_doc, 'gitlab-build-scripts', 'gitlab-build-scripts Documentation',
     author, 'gitlab-build-scripts', 'One line description of project.',
     'Miscellaneous'),
]

# Epub
epub_title = project
epub_author = author
epub_publisher = author
epub_copyright = copyright
epub_exclude_files = ['search.html']

intersphinx_mapping = {'https://docs.python.org/': None}


def setup(app) -> None:
    """
    Registers an autodoc between listener to igore License texts

    :param app: The sphinx app
    :return:    None
    """
    app.connect('autodoc-process-docstring', between('^.*LICENSE.*$', exclude=True))
    app.connect("autodoc-skip-member", lambda a, b, name, d, skipper, f: False if name == "__init__" else skipper)
    return app
