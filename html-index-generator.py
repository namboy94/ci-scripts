#!/usr/bin/env python
"""
Copyright Hermann Krumrey <hermann@krumreyh.com>, 2017

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import os
import argparse


def parse_args():

    parser = argparse.ArgumentParser()
    parser.add_argument("directory", help="The directory for which to create \
                                           an HTML index page for.")
    parser.add_argument("target_file", help="The path to the generated \
                                             index.html file")
    parser.add_argument("-t", "--template_file", default="template.html",
                        help="The template HTML file to use")
    parser.add_argument("-n", "--name", default="Title",
                        help="The title of the directory to be displayed")
    parser.add_argument("-v", "--verbose", 
                        help="If set, the program outputs status messages")

    args = parser.parse_args()

    if not os.path.isdir(args.directory):
        print(args.directory + " is not a directory")
        exit()
    if not os.path.isfile(args.template_file):
        print(args.template_file + " does not exist")
        exit()

    return args.directory, 
           args.template_file, 
           args.target_file, 
           args.name, 
           args.verbose


def generate_html(source_directory,
                  template_file, 
                  destination_file, 
                  name, 
                  verbose):

    if verbose:
        print("Generating Index file for " + source_directory)

    with open(template_file, 'r') as template:
        html = template.read()

    title = name
    if name == "Title":
        title = os.path.basename(source_directory)

    content = ""

    for child in sorted(os.listdir(source_directory)):
        child_path = os.path.join(source_directory, child)

        if child == "title":
            with open(child_path, 'r') as title_file:
                title = title_file.read().rstrip().lstrip()

        elif child == "index.html" or child == "style.css":
            pass

        elif child == ".well-known":
            pass

        elif os.path.isfile(child_path):
            content += format_html(child_path, child, source_directory)

        elif os.path.isdir(child_path):
            content += process_directory(child_path, source_directory)

    html = html.replace("@TITLE", title)
    html = html.replace("@CONTENT", content)

    with open(destination_file, 'w') as destination:
        destination.write(html)


def process_directory(directory_path, source_directory):

    directory_name = os.path.basename(directory_path)
    index_file = os.path.join(directory_path, "index.html")

    if os.path.isfile(index_file):
        return format_html(index_file, directory_name, source_directory)

    else:

        html = "<li><h2>" + directory_name + "</h2><ul>"

        for child in sorted(os.listdir(directory_path)):

            child_path = os.path.join(directory_path, child)

            if os.path.isfile(child_path):

                if child == "style.css":
                    pass
                else:
                    html += format_html(child_path, child, source_directory)

            elif os.path.isdir(child_path):
                html += process_directory(child_path, source_directory)

        html += "</ul></li>"
        return html


def format_html(path, display_name, root_directory):
    relative = os.path.relpath(path, root_directory)
    return "<li><a href=\"" + relative + "\">" + display_name + "</a></li>"


if __name__ == "__main__":

    source_directory, template_file, destination_file, name, verbose \
        = parse_args()

    generate_html(source_directory,
                  template_file,
                  destination_file,
                  name, 
                  verbose)
