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

import argparse
from typing import List, Dict
from gitlab_build_scripts.metadata import sentry
from gitlab_build_scripts.project_parsers.general import get_changelog_for_version
from gitlab_build_scripts.uploaders.github_release import upload_github_release
from gitlab_build_scripts.uploaders.gitlab_release import upload_gitlab_release


# noinspection PyUnresolvedReferences
def build(metadata_module: 'module', artifacts: List[Dict[str, str]]=None) -> None:
    """
    Starts the build script for a python project

    :param metadata_module: the metadata module of the project
    :param artifacts:       release assets for uploading to gitlab or github
    :return:                None
    """
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument("mode", help="The build mode.\n"
                                         "Available modes:   - github-release"
                                         "                   - gitlab-release")
        args = parser.parse_args()

        if args.mode == "github-release":
            github_release(metadata_module, artifacts)
        elif args.mode == "gitlab-release":
            gitlab_release(metadata_module, artifacts)
        else:
            print("Invalid mode. Enter --help for more information")

    except Exception as e:
        str(e)
        sentry.captureException()


# noinspection PyUnresolvedReferences
def gitlab_release(metadata_module: 'module', artifacts: List[Dict[str, str]]=None) -> None:
    """
    Creates a new Gitlab Release tag from the master branch

    :param metadata_module: the metadata module of the project
    :param artifacts:       release assets for uploading to gitlab
    :return:                None
    """
    artifacts = [] if artifacts is None else artifacts

    repository_name = metadata_module.project_url.rplit("/", 1)[1]
    repository_owner = metadata_module.project_url.rsplit("/", 2)[1]
    protocol = metadata_module.project_url.split(":", 1)[0]
    gitlab_url = protocol + "://" + metadata_module.project_url.split("/", 3)[2]

    personal_access_token = os.environ["GITLAB_ACCESS_TOKEN"]
    changelog = get_changelog_for_version(metadata_module.version_number)

    upload_gitlab_release(repository_owner,
                          repository_name,
                          gitlab_url,
                          metadata_module.version_number,
                          personal_access_token,
                          "Release " + metadata_module.version_number,
                          changelog,
                          artifacts,
                          "master")


# noinspection PyUnresolvedReferences
def github_release(metadata_module: 'module', artifacts: List[Dict[str, str]]=None) -> None:
    """
    Creates a new GitHub Release tag

    :param metadata_module: the metadata module of the project
    :param artifacts:       release assets for uploading to github
    :return:                None
    """
    artifacts = [] if artifacts is None else artifacts

    repository_name = metadata_module.project_url.rplit("/", 1)[1]
    repository_owner = metadata_module.project_url.rsplit("/", 2)[1]
    o_auth_token = os.environ["GITHUB_OAUTH_TOKEN"]

    changelog = get_changelog_for_version(metadata_module.version_number)

    upload_github_release(repository_owner,
                          repository_name,
                          metadata_module.version_number,
                          o_auth_token,
                          changelog,
                          artifacts)
