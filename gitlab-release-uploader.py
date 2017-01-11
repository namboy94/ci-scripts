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

import json
import urllib.parse
import requests


def upload_gitlab_release(repository_owner,                # str
                          repository_name,                 # str
                          gitlab_url="https://gitlab.com", # str
                          version_number,                  # str
                          personal_access_token,           # str
                          tag_annotation,                  # str
                          release_notes,                   # str (or file)
                          release_assets,                 # List[Dict[str, str]]
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
    :param tag_annotation:        the tag's annotation
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
	                  gitlab_url)             # str   -> int
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

    repository_path = gitlab_api_path + "projects/" + urllib.parse.quote(
        (repository_owner + "/" + repository_name), safe="")
    query = repository_path + "?private_token=" + personal_access_token

    project_info = json.loads(requests.get(query).text)
    return int(project_info["id"])

if __name__ == "__main__":
	pass
