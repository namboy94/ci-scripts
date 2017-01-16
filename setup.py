"""
LICENSE:
Copyright 2016 Hermann Krumrey

This file is part of gitlab-build-scripts.

    gitlab-build-scripts is a collection of scripts, importable via pip/setuptools,
    that act as helpers for gitlab CI builds.

    gitlab-build-scripts is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    gitlab-build-scripts is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with gitlab-build-scripts.  If not, see <http://www.gnu.org/licenses/>.
LICENSE
"""

# imports
import os
from setuptools import setup, find_packages


def readme():
    """
    Reads the readme file.

    :return: the readme file as a string
    """
    # noinspection PyBroadException
    try:
        # noinspection PyPackageRequirements
        import pypandoc
        with open('README.md') as f:
            # Convert markdown file to rst
            markdown = f.read()
            rst = pypandoc.convert(markdown, 'rst', format='md')
            return rst
    except:
        # If pandoc is not installed, just return the raw markdown text
        with open('README.md') as f:
            return f.read()


def find_scripts():
    """
    Returns a list of scripts in the bin directory

    :return: the list of scripts
    """
    try:
        scripts = []
        for file_name in os.listdir("bin"):
            if not file_name == "__init__.py" and os.path.isfile(os.path.join("bin", file_name)):
                scripts.append(os.path.join("bin", file_name))
        return scripts
    except OSError:
        return []

setup(name="gitlab_build_scripts",
      version="0.8.0",
      description="Python Build Scripts for Gitlab CI",
      long_description=readme(),
      classifiers=[
          "Topic :: Utilities",
          "Environment :: Console",
          "Natural Language :: English",
          "Development Status :: 1 - Planning",
          "Operating System :: OS Independent",
          "Programming Language :: Python :: 3",
          "Programming Language :: Python :: 2",
          "License :: OSI Approved :: GNU General Public License v3 (GPLv3)"
      ],
      url="https://gitlab.namibsun.net/namboy94/gitlab-build-scripts",
      download_url="https://gitlab.namibsun.net/namboy94/gitlab-build-scripts/repository/archive.zip?ref=master",
      author="Hermann Krumrey",
      author_email="hermann@krumreyh.com",
      license="GNU GPL3",
      packages=find_packages(),
      install_requires=[],
      test_suite='nose.collector',
      tests_require=['nose'],
      scripts=find_scripts(),
      zip_safe=False)
