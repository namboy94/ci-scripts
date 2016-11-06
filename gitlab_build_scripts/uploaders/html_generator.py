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


def create_gitstats_html(gitstats_root_directory: str) -> None:
    """
    Creates a Gitstats Index page

    :param gitstats_root_directory: The root directory of the gitstats site/vhost
    :return:                        None
    """
    html = open(os.path.join(gitstats_root_directory, "index.html"), 'w')
    html.write("<!DOCTYPE html><html><head><title>Git Statistics</title><meta charset=\"UTF-8\"></head><body>")
    html.write("<h1><a href=\"http://gitstats.sourceforge.net/\">gitstats</a>:</h1>")

    for project in os.listdir(os.path.join(gitstats_root_directory, "gitstats")):
        if os.path.isdir(project):
            html.write("<h3><a href=\"gitstats/" + project + "/index.html\">" + project + "</h3>")

    html.write("<h1><a href=\"https://github.com/tomgi/git_stats\">git_stats</a>:</h1>")

    for project in os.listdir(os.path.join(gitstats_root_directory, "git_stats")):
        if os.path.isdir(project):
            html.write("<h3><a href=\"git_stats/" + project + "/index.html\">" + project + "</h3>")
    html.close()


def create_documentation_html(documentation_root_directory: str) -> None:
    """
    Creates a Documentation Index Page

    :param documentation_root_directory: The root directory of the documntation site/vhost
    :return:                             None
    """
    html = open(os.path.join(documentation_root_directory, "index.html"), 'w')
    html.write("<!DOCTYPE html><html><head><title>Documentation</title><meta charset=\"UTF-8\"></head><body>")
    html.write("<h1>HTML:</h1>")

    for project in os.listdir(os.path.join(documentation_root_directory, "html_docs")):
        if os.path.isdir(project):
            html.write("<h3><a href=\"html_docs/" + project + "/index.html\">" + project + "</h3>")

    html.write("<h1>PDF:</h1>")

    for project in os.listdir(os.path.join(documentation_root_directory, "pdf_docs")):
        html.write("<h3><a href=\"pdf_docs/" + project + "\">" + project + "</h3>")
    html.close()


def create_test_coverage_html(coverage_root_directory: str) -> None:
    """
    Creates a test coverage Index Page

    :param coverage_root_directory: The root directory of the coverage site/vhost
    :return:                        None
    """
    html = open(os.path.join(coverage_root_directory, "index.html"), 'w')
    html.write("<!DOCTYPE html><html><head><title>Coverage</title><meta charset=\"UTF-8\"></head><body>")
    html.write("<h1>HTML:</h1>")

    for project in os.listdir(coverage_root_directory):
        if os.path.isdir(project):
            html.write("<h3><a href=\"" + project + "/index.html\">" + project + "</h3>")

    html.close()
