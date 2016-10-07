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


def get_changelog_for_version(version: str) -> str:
    """
    Extracts the changelog entry for the specified version number

    :param version: the version for which the changelog should be found
    :return:        the changelog entry, formatted like this:
                            Changelog Version <version>:
                                - Feature 1
                                - Feature 2
    """
    with open("/home/hermann/Documents/Programming/PyCharm/gitlab-build-scripts/CHANGELOG", 'r') as changelog_file:
        changelog = changelog_file.read()

    try:
        changelog = changelog.split(version)[1].split("\n", 1)[1]
        changelog = changelog.split(":")[0].rsplit("\n", 1)[0]
    except IndexError:
        changelog = ""

    changelog_lines = changelog.split("\n")

    if changelog:

        changelog = "Changelog Version " + version + ":\n"

        for line in changelog_lines:
            formatted_line = line.rstrip().lstrip()
            if not formatted_line.startswith("-"):
                formatted_line = "- " + formatted_line
            formatted_line = "    " + formatted_line
            changelog += formatted_line + "\n"

        changelog = changelog.rstrip().lstrip()

    else:
        changelog = "Changelog Version " + version + ":\n"

    return changelog
