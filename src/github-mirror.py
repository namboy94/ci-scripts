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
import sys
import argparse
from subprocess import Popen


def main():
    """
    Mirrors the specified branches to a github.com repository

    Requires the following environment variables to be set:

        GITHUB_USERNAME
        GITHUB_ACCESS_TOKEN
        CI_PROJECT_NAME

    :return: None
    """

    parser = argparse.ArgumentParser()
    parser.add_argument("branches", nargs="+")
    args = parser.parse_args()

    github_push_url = "https://" + os.environ["GITHUB_USERNAME"] + \
                      ":" + os.environ["GITHUB_ACCESS_TOKEN"] + "@" + \
                      "github.com/" + os.environ["GITHUB_USERNAME"] + "/" + \
                      os.environ["CI_PROJECT_NAME"]

    print("Mirroring to " + github_push_url)

    for branch in args.branches:
        print("Mirroring " + branch)
        Popen(["git", "checkout", branch]).wait()
        Popen(["git", "pull"]).wait()
        Popen(["git", "push", github_push_url])


if __name__ == "__main__":

    try:
        main()
    except Exception as e:
        print(e)
        sys.exit(1)
