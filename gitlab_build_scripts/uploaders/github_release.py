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
from typing import Dict, List
from subprocess import check_output


def upload_github_release(repository_owner: str,
                          repository_name: str,
                          version_number: str,
                          o_auth_token: str,
                          release_notes: str,
                          release_assets: List[Dict[str, str]]) -> None:
    """
    Uploads a new release to github.com

    First, a new release is created. Afterwards, the script uploads all specified release assets to that
    Github release

    :param repository_owner: the destination repository owner
    :param repository_name:  the destination repository
    :param version_number:   the project's current version number
    :param o_auth_token:     the repository owner's oauth token
    :param release_notes:    release notes associated with this release
    :param release_assets:   the release assets, as a list of dictionaries with the following keys:
                                     file_path:              the file path to the asset
                                     content_type:           the asset's content type, for example
                                                                 application/java-archive
                                                             for .jar files
    :return: None
    """

    repository_path = "repos/" + repository_owner + "/" + repository_name + "/releases"
    repository_api_url = "https://api.github.com/" + repository_path
    repository_upload_url = "https://uploads.github.com/" + repository_path
    o_auth_parameter = "access_token=" + o_auth_token

    create_release = ["curl",
                      "-X",
                      "POST",
                      repository_api_url + "?" + o_auth_parameter,
                      "-d",
                      "{\"tag_name\": \"" + version_number + "\"," +
                      " \"target_commitish\": \"master\"," +
                      "\"name\":\"" + version_number + "\"," +
                      "\"body\": \"" + release_notes + "\"," +
                      "\"draft\": false," +
                      "\"prerelease\": false}"]

    response = check_output(create_release).decode()
    print(response)
    tag_id = response.split("\"id\": ")[1].split(",")[0]

    for asset in release_assets:

        file_path = asset["file_path"]
        file_name = os.path.basename(file_path).split(".")[0]
        content_type = asset["content_type"]

        upload_binary = ["curl",
                         "-X",
                         "POST",
                         "--header",
                         "\"Content-Type:" + content_type + "\"",
                         "--data-binary",
                         "@" + file_path,
                         "'" + repository_upload_url + "/" + tag_id + "/assets?name=" +
                         file_name + "&" + o_auth_parameter + "'"]

        # No Idea why this doesn't just work with Popen
        params = ""
        for param in upload_binary:
            params += param + " "
        params = params[0:-1]
        os.system(params)
