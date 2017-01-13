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

    parser = ArgumentParser()
    parser.add_argument("directory", help="The directory for which to create \
                                           an HTML index page for.")


def generate_html(source_directory, template_file, destination_file):

    with open(template_file, 'r') as template:
        html = template.read()


if __name__ == "__main__":

    source_directory, template_file, destination_file = parse_args()
    generate_html(source_directory, template_file, destination_file)
