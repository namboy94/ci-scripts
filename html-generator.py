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

    args = parser.parse_args()

    if not os.path.isdir(args.directory):
        print(args.directory + " is not a directory")
        exit()
    if not os.path.isfile(args.template_file):
        print(args.template_file + " does not exist")
        exit()

    return args.directory, args.template_file, args.target_file


def generate_html(source_directory, template_file, destination_file):

    with open(template_file, 'r') as template:
        html = template.read()

    title = "Title"
    content = ""

    for child in sorted(os.listdir(source_directory)):
        child_path = os.path.join(source_directory, child)

        if child == "title":
            with open(child_path, 'r') as title_file:
                title = title_file.read().rstrip().lstrip()

        elif os.path.isfile(child_path):
            content += format_html(child_path, child)

        elif os.path.isdir(child_path):
            content += process_directory(child_path)

    html = html.replace("@TITLE", title)
    html = html.replace("@CONTENT", content)

    with open(destination_file, 'w') as destination:
        destination.write(html)


def process_directory(directory_path):

    directory_name = os.path.basename(directory_path)
    index_file = os.path.join(directory_path, "index.html")

    if os.path.isfile(index_file):
        return format_html(index_file, directory_name)

    else:

        html = "<li><ul>"

        for child in os.listdir(directory_path):

            child_path = os.path.join(directory_path, child)

            if os.path.isfile(child_path):
                html += format_html(child_path, child)

            elif os.path.isdir(child_path):
                html += process_directory(child_path)

        html += "</ul></li>"
        return html


def format_html(path, display_name):
    return "<li><a href=\"" + path + "\">" + display_name + "</a></li>"


if __name__ == "__main__":

    source_directory, template_file, destination_file = parse_args()
    generate_html(source_directory, template_file, destination_file)
