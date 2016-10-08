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
import argparse
from typing import List
from gitlab_build_scripts.metadata import SentryLogger
from gitlab_build_scripts.buildmodules.BuildModule import BuildModule
from gitlab_build_scripts.uploaders.github_release import upload_github_release
from gitlab_build_scripts.uploaders.gitlab_release import upload_gitlab_release
from gitlab_build_scripts.project_parsers.general import get_changelog_for_version


# noinspection PyUnresolvedReferences,PyDefaultArgument
def build(metadata_module: 'module', build_modules: List[BuildModule]=[]) -> None:
    """
    Starts the build script for a python project

    :param metadata_module: the metadata module of the project
    :param build_modules:   BuildModule implementations
    :return:                None
    """
    builds_location = os.path.join("build", "gitlab_build_scripts")
    if not os.path.isdir(builds_location):
        os.makedirs(builds_location)

    try:
        parser = argparse.ArgumentParser()
        parser.add_argument("mode", help="The build mode.\n"
                                         "Available modes:   - github-release\n"
                                         "                   - gitlab-release")
        parser.add_argument('module', nargs='?', default=None, help="Specifies the module to be run")

        args = parser.parse_args()

        if args.mode == "github-release":
            github_release(metadata_module, build_modules)

        elif args.mode == "gitlab-release":
            gitlab_release(metadata_module, build_modules)

        elif args.mode == "build":
            for module in build_modules:
                if module.get_identifier() == args.module:
                    module.build(metadata_module)
                    return
            print("No module '" + args.module + "' specified in builder.py")
        else:
            print("Invalid mode. Enter --help for more information")

    except Exception as e:
        SentryLogger.sentry.captureException()
        raise e


# noinspection PyUnresolvedReferences
def gitlab_release(metadata_module: 'module', build_modules: List[BuildModule]) -> None:
    """
    Creates a new Gitlab Release tag from the master branch

    :param metadata_module: the metadata module of the project
    :param build_modules:   BuildModule classes that specify where release artifacts are located
    :return:                None
    """
    artifacts = []
    for module in build_modules:
        artifacts += module.get_artifacts(metadata_module)

    repository_name = metadata_module.GitRepository.repository_name
    repository_owner = metadata_module.GitRepository.gitlab_owner
    gitlab_site_url = metadata_module.GitRepository.gitlab_site_url

    personal_access_token = os.environ["GITLAB_ACCESS_TOKEN"]
    version_number = metadata_module.General.version_number
    changelog = get_changelog_for_version(version_number)

    upload_gitlab_release(repository_owner,
                          repository_name,
                          gitlab_site_url,
                          version_number,
                          personal_access_token,
                          "Release " + version_number,
                          changelog,
                          artifacts,
                          "master")


# noinspection PyUnresolvedReferences
def github_release(metadata_module: 'module', build_modules: List[BuildModule]) -> None:
    """
    Creates a new GitHub Release tag

    :param metadata_module: the metadata module of the project
    :param build_modules:   BuildModule classes that specify where release artifacts are located
    :return:                None
    """
    artifacts = []
    for module in build_modules:
        artifacts += module.get_artifacts(metadata_module)

    repository_name = metadata_module.GitRepository.repository_name
    repository_owner = metadata_module.GitRepository.github_owner

    o_auth_token = os.environ["GITHUB_OAUTH_TOKEN"]

    version_number = metadata_module.General.version_number
    changelog = get_changelog_for_version(version_number)

    upload_github_release(repository_owner,
                          repository_name,
                          version_number,
                          o_auth_token,
                          changelog,
                          artifacts)
