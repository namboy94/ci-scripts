#!/usr/bin/env python
"""
Copyright 2017 Hermann Krumrey <hermann@krumreyh.com>

This file is part of gitlab-build-scripts.

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
"""

import os
import argparse


def parse_args():

    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--changelog", nargs='?', default="CHANGELOG",
                        help="The path to the Changelog file")
    parser.add_argument("-d", "--destination", nargs='?', default=None,
                        help="The destination file")

    args = parser.parse_args()

    source = args.changelog
    dest = args.destination

    if not os.path.isfile(source):
        print("Changelog File not found")
        exit()
    if dest is not None and os.path.isfile(dest):
        print("Destination file already exists")
        exit()

    return source, dest


def read(source_file):
    with open(source_file, 'r') as f:
        source = f.read().split("\n")

    version_name = None
    version_description = []

    for line in source:

        if line == "":
            continue

        if not line.startswith(" ") and not line.startswith("\t"):

            if version_name is None:
                version_name = format_version_name(line)
            else:
                break

        else:
            version_description.append(format_version_description(line))

    return format_changelog_entry(version_name, version_description)


def format_version_name(version_name):

    if version_name.lower().startswith("v ") or \
            version_name.lower().startswith("version "):
        version_name = version_name.split(" ", 1)[1]

    if version_name.endswith(":"):
        version_name = version_name.rsplit(":", 1)[0]

    return version_name


def format_version_description(version_description):

    while version_description.startswith(" "):
        version_description = version_description.split(" ", 1)[1]
    while version_description.startswith("\t"):
        version_description = version_description.split("\t", 1)[1]

    if version_description.startswith("- "):
        version_description = version_description.split("- ", 1)[1]
    elif version_description.startswith("-"):
        version_description = version_description.split("-", 1)[1]

    return version_description


def format_changelog_entry(version_name, version_description):

    formatted = "Changelog Version ```" + version_name + "```:\n\n"

    for description in version_description:
        formatted += "    - " + description + "\n"

    return formatted


if __name__ == "__main__":

    source, destination = parse_args()
    content = read(source)

    if destination is None:
        print(content)
    else:
        with open(destination, 'w') as f:
            f.write(content)
