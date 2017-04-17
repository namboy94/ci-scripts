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

import argparse


def parse_args():
    """
    Parses the command line arguments
    :return: The parsed arguments as an argparse Namespace
    """

    parser = argparse.ArgumentParser()
    parser.add_argument("package_name",
                        help="The name of the package to upload to,"
                             "for example: com.android.example")
    parser.add_argument("track",
                        help="The track to which to upload the release to. May"
                             " be 'rollout', 'production', 'beta' or 'alpha'")
    parser.add_argument("email",
                        help="The Google API Service Account Email address")
    parser.add_argument("keyfile",
                        help="The p12 keyfile provided by the Google API")
    parser.add_argument("apks",
                        help="The APK file(s) to upload")
    parser.add_argument("-c", "--changes",
                        help="Can be used to specify a file containing changes"
                             " to the new version of the app. The file must"
                             " be called 'en-US' or 'de-DE' or similar."
                             " Multiple of these files can be provided by"
                             " seperating the file paths with commas")
    return parser.parse_args()

def main():

    args = parse_args()

