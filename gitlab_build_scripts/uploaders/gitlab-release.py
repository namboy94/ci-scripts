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

import os
import json
import urllib.parse
import requests
from typing import Dict, List
from subprocess import check_output


def upload_github_release(repository_owner: str,
                          repository_name: str,
                          gitlab_url: str,
                          version_number: str,
                          personal_access_token: str,
                          release_notes: str,
                          release_assets: List[Dict[str, str]]) -> None:
    """
    Uploads a new release to a Gitlab instance

    First, a new release is created. Afterwards, the script uploads all specified release assets to that
    release tag.

    WARNING: Since the Gitlab API does not allow uploading of attachments via the API as of right now,
             the specified release assets will NOT be uploaded.

    :param repository_owner:      the destination repository owner
    :param repository_name:       the destination repository
    :param gitlab_url:            the URL of the gitlab instance
    :param version_number:        the project's current version number
    :param personal_access_token: the repository owner's personal access token
    :param release_notes:         release notes associated with this release
    :param release_assets:        the release assets, as a list of dictionaries with the following keys:
                                         file_path:     the file path to the asset
                                         content_type:  the asset's content type, for example
                                                            application/java-archive
                                                        for .jar files
    :return: None
    """

    gitlab_api_path = gitlab_url + "api/v3/" if gitlab_url.endswith("/") else gitlab_url + "/api/v3/"


def get_repository_id(repository_owner: str, repository_name: str, personal_access_token: str, gitlab_url: str) -> int:
    """
    Fetches a project's ID for use with the API

    :param repository_owner:       the owner of the repository
    :param repository_name:        the name of the repository
    :param personal_access_token:  the owner's personal access token
    :param gitlab_url:             the Gitlab instance's URL
    :return:                       the project's ID
    """
    gitlab_api_path = gitlab_url + "api/v3/" if gitlab_url.endswith("/") else gitlab_url + "/api/v3/"
    repository_path = gitlab_api_path + urllib.parse.urlencode(repository_owner + "/" + repository_name)
    query = repository_path + "?" + personal_access_token

    project_info = json.loads(requests.get(query).text)
    return int(project_info["id"])