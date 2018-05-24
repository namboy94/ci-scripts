"""LICENSE
Copyright 2017 Hermann Krumrey

This file is part of ci-scripts.

ci-scripts is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

ci-scripts is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with ci-scripts.  If not, see <http://www.gnu.org/licenses/>.
LICENSE"""

import os
import sys
import argparse
from enum import Enum
from typing import Dict, List


class SourceControlType(Enum):
    """
    An enum that specifies different source control types
    to which releases can be uploaded
    """
    GITHUB = "github"
    GITLAB = "gitlab"


def parse_args(source_control_type: SourceControlType) \
        -> Dict[str, str or List[Dict[str, str]]]:
    """
    Parses command line arguments
    :param source_control_type: The type of source control used
    :return: A dictionary containing data required for uploading a release
    """
    src_ctrl = source_control_type.value

    parser = argparse.ArgumentParser()

    if source_control_type == SourceControlType.GITHUB:
        parser.add_argument("username", help="The " + src_ctrl + " Username")

    parser.add_argument("auth_token",
                        help="The " + src_ctrl + "Authentication Token")
    parser.add_argument("tag_name",
                        help="The Tag name on which to base the release on")
    parser.add_argument("release_notes",
                        help="The Release Notes. Can be a file or a string")
    parser.add_argument("release_assets",
                        help="The release assets.", nargs="*", default=[])
    parser.add_argument("-b", "--branch", default="master",
                        help="The source branch or commit on which to base \
                        this release on")

    args = parser.parse_args()

    notes = args.notes
    if os.path.isfile(notes):
        with open(notes, 'r') as release_notes:
            notes = release_notes.read()

    assets = []
    for asset in args.release_assets:
        if not os.path.isfile(asset):
            print(asset + " does not exist")
            sys.exit(1)
        else:
            assets.append({
                "path": asset,
                "content_type": get_content_type(os.path.basename(asset))
            })

    data = {
        "auth_token": args.auth_token,
        "tag_name": args.tag_name,
        "notes": notes,
        "assets": assets,
        "branch": args.branch
    }

    if source_control_type == SourceControlType.GITHUB:
        data["username"] = args.username

    return data


def get_content_type(filename: str) -> str:
    """
    Retrieves a sensible content type for a file
    :param filename: The name of the file
    :return: The content type of the file
    """

    try:
        extension = filename.rsplit(".", 1)[1].lower()

        if extension == "jar":
            return "application/java-archive"
        else:
            return "application/octet-stream"

    except IndexError:
        return "application/octet-stream"
