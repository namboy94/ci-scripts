"""LICENSE
Copyright 2017 Hermann Krumrey <hermann@krumreyh.com>

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
from typing import Dict, List


def parse_args() -> Dict[str, str or List[Dict[str, str]]]:
    """
    Parses command line arguments
    :return: A dictionary containing data required for uploading a release
    """

    parser = argparse.ArgumentParser()

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

    notes = args.release_notes
    if os.path.isfile(notes):
        with open(notes, 'r') as release_notes:
            notes = release_notes.read()

    # Add files in artifacts directory to release assets
    all_asset_paths = args.release_assets
    if os.path.isdir("artifacts"):
        for child in os.listdir("artifacts"):
            child_path = os.path.join("artifacts", child)
            if os.path.isfile(child_path):
                all_asset_paths.append(child_path)

    assets = []
    for asset in all_asset_paths:
        if not os.path.isfile(asset):
            print(asset + " does not exist")
            sys.exit(1)
        else:
            assets.append({
                "path": asset,
                "content_type": get_content_type(os.path.basename(asset))
            })

    return {
        "tag_name": args.tag_name.strip(),
        "notes": notes,
        "assets": assets,
        "branch": args.branch
    }


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
        elif extension == "txt":
            return "text/plain"
        else:
            return "application/octet-stream"

    except IndexError:
        return "application/octet-stream"
