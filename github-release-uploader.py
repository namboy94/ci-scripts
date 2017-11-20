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
import sys
import json
import argparse
import requests


def upload_github_release(repository_owner,  # str
                          repository_name,   # str,
                          version_number,    # str,
                          o_auth_token,      # str,
                          release_notes,     # str,
                          release_assets,    # List[Dict[str, str]],
                          branch):  # str
    """
    Uploads a new release to github.com

    First, a new release is created. Afterwards, the script uploads all
    specified release assets to that Github release

    Does not work if the Release Tag already exists

    :param repository_owner: the destination repository owner
    :param repository_name:  the destination repository
    :param version_number:   the project's current version number
    :param o_auth_token:     the repository owner's oauth token
    :param release_notes:    release notes associated with this release
    :param release_assets:   the release assets, as a list of dictionaries
                             with the following keys:
                                file_path:    the file path to the asset
                                content_type: the asset's content type,
                                              for example
                                                  'application/java-archive'
                                              for .jar files
    :param branch:           the branch on which the release will be based on,
                             defaults to the master branch
    :return: None
    """

    # Format Strings for HTTP requests
    repository_identifier = repository_owner + "/" + repository_name
    repository_path = "repos/" + repository_identifier + "/releases"
    repository_api_url = "https://api.github.com/" + repository_path
    repository_upload_url = "https://uploads.github.com/" + repository_path
    o_auth_parameter = "access_token=" + o_auth_token

    post_url = repository_api_url + "?" + o_auth_parameter
    json_payload = {
        "tag_name": version_number,
        "target_commitish": branch,
        "name": "Release " + version_number,
        "body": release_notes,
        "draft": False,
        "prerelease": False
    }

    # Create Tag and get Tag ID
    response = json.loads(requests.post(post_url, json=json_payload).text)
    try:
        tag_id = response["id"]
    except KeyError:
        print(response)

    for asset in release_assets:

        file_path = asset["file_path"]
        file_name = os.path.basename(file_path)
        content_type = asset["content_type"]

        with open(file_path, "rb") as bytefile:
            data = bytefile.read()

        tag_api_url = repository_upload_url + "/" + str(tag_id)
        tag_api_url += "/assets?name=" + file_name + "&" + o_auth_parameter
        headers = {"Content-Type": content_type}

        # Upload Asset
        requests.post(url=tag_api_url, data=data, headers=headers)


def get_content_type(filename):

    try:
        extension = filename.rsplit(".", 1)[1].lower()

        if extension == "jar":
            return "application/java-archive"
        else:
            return "application/octet-stream"

    except IndexError:
        return "application/octet-stream"


def parse_args():   # -> username, reponame, auth token, release notes, assets,
                    #    source branch

    parser = argparse.ArgumentParser()
    parser.add_argument("username",
                        help="The Github Username")
    parser.add_argument("reponame",
                        help="The Repository Name")
    parser.add_argument("auth_token",
                        help="The Authentication Token")
    parser.add_argument("tag_name",
                        help="The Tag name on which to base the release on")
    parser.add_argument("release_notes",
                        help="The Release Notes. Can be a file or a string")
    parser.add_argument("release_assets",
                        help="The Release Asset directory. \
                        Every file in this directory will be uploaded")
    parser.add_argument("-b", "--branch", default="master",
                        help="The source branch or commit on which to base \
                        this release on")

    args = parser.parse_args()

    username = args.username
    reponame = args.reponame
    auth_token = args.auth_token
    tag_name = args.tag_name
    notes = args.release_notes
    assets = args.release_assets
    branch = args.branch

    if os.path.isfile(notes):
        with open(notes, 'r') as release_notes:
            notes = release_notes.read()

    if not os.path.isdir(assets):
        print(assets + " is not a directory")
        exit()

    return username, reponame, auth_token, tag_name, notes, assets, branch


if __name__ == "__main__":

    username, reponame, auth_token, tag_name, release_notes, assets, branch \
        = parse_args()

    asset_info = []

    for asset in os.listdir(assets):

        asset_dict = {}

        asset_dict["file_path"] = os.path.join(assets, asset)
        asset_dict["content_type"] = get_content_type(asset)

        asset_info.append(asset_dict)

    upload_github_release(username, reponame, tag_name, auth_token,
                          release_notes, asset_info, branch)
