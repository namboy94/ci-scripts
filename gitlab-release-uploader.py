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
import json
import argparse
import requests

try:
    import urllib.parse
    quote = urllib.parse.quote
except ImportError:
    import urllib
    quote = urllib.quote



def upload_gitlab_release(repository_owner,                # str
                          repository_name,                 # str
                          version_number,                  # str
                          personal_access_token,           # str
                          release_notes,                   # str (or file)
                          release_assets,                 # List[Dict[str, str]]
                          gitlab_url="https://gitlab.com", # str
                          branch='master'):                # str
    """
    Uploads a new release to a Gitlab instance

    First, a new release is created. Afterwards, the script uploads all
    specified release assets to that release tag.

    WARNING: Since the Gitlab API does not allow uploading of attachments via
             the API as of right now, the specified release assets will NOT be
             uploaded. They will have to be uploaded by hand.

    :param repository_owner:      the destination repository owner
    :param repository_name:       the destination repository
    :param gitlab_url:            the URL of the gitlab instance
    :param version_number:        the project's current version number
    :param personal_access_token: the repository owner's personal access token
    :param release_notes:         release notes associated with this release
    :param release_assets:        the release assets, as a list of dictionaries
                                  with the following keys:
                                      file_path:     the file path to the asset
                                      content_type:  the asset's content type,
                                                     for example
                                                        application/java-archive
                                                     for .jar files
    :param branch:                the branch to base the release on.
                                  Defaults to master
    :return: None
    """
    tag_annotation = "Release " + version_number

    if gitlab_url.endswith("/"):
        gitlab_api_path = gitlab_url + "api/v3/"
    else:
        gitlab_api_path = gitlab_url + "/api/v3/"

    project_id = get_repository_id(repository_owner,
                                   repository_name,
                                   personal_access_token,
                                   gitlab_url)

    project_path = str(project_id) + "/repository/tags"
    project_url = gitlab_api_path + "projects/" + project_path

    query = project_url + "?private_token=" + personal_access_token + "&ref="
    query += branch + "&message=" + tag_annotation + "&release_description="
    query += release_notes + "&tag_name=" + version_number

    requests.post(query)


def get_repository_id(repository_owner,       # str
                      repository_name,        # str
                      personal_access_token,  # str
                      gitlab_url):            # str   -> int
    """
    Fetches a project's ID for use with the API

    :param repository_owner:       the owner of the repository
    :param repository_name:        the name of the repository
    :param personal_access_token:  the owner's personal access token
    :param gitlab_url:             the Gitlab instance's URL
    :return:                       the project's ID
    """

    if gitlab_url.endswith("/"):
        gitlab_api_path = gitlab_url + "api/v3/"
    else:
        gitlab_api_path = gitlab_url + "/api/v3/"

    repository_path = gitlab_api_path + "projects/" + quote(
        (repository_owner + "/" + repository_name), safe="")
    query = repository_path + "?private_token=" + personal_access_token

    project_info = json.loads(requests.get(query).text)
    return int(project_info["id"])

def parse_args():   # -> username, reponame, auth token, release notes, assets,
                    #    source branch, gitlab_address

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
    parser.add_argument("gitlab_url", default="https://gitlab.com", nargs='?',
                        help="The URL of the Gitlab instance")
    parser.add_argument("source_branch", default="master", nargs='?',
                        help="The source branch or commit on which to base \
                        this release on")

    args = parser.parse_args()

    username = args.username
    reponame = args.reponame
    auth_token = args.auth_token
    tag_name = args.tag_name
    notes = args.release_notes
    assets = args.release_assets
    url = args.gitlab_url
    branch = args.source_branch

    if os.path.isfile(notes):
        with open(notes, 'r') as release_notes:
            notes = release_notes.read()

    if not os.path.isdir(assets):
        print(assets + " is not a directory")
        exit()

    return username, reponame, auth_token, tag_name, notes, assets, url, branch

def get_content_type(filename):

    try:
        extension = filename.rsplit(".", 1)[1].lower()

        if extension == "jar":
            return "application/java-archive"
        else:
            return "application/octet-stream"

    except IndexError:
        return "application/octet-stream"

if __name__ == "__main__":

    user, repo, auth, tag, notes, assets, url, branch = parse_args()
    asset_info = []

    for asset in os.listdir(assets):

        asset_dict = {}

        asset_dict["file_path"] = os.path.join(assets, asset)
        asset_dict["content_type"] = get_content_type(asset)

        asset_info.append(asset_dict)

    upload_gitlab_release(user, repo, tag, auth, notes, asset_info, url, branch)
