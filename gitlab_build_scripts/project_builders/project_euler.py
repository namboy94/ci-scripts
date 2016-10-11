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

# imports
import sys
import argparse
from typing import List
from subprocess import Popen
from gitlab_build_scripts.metadata import SentryLogger
from gitlab_build_scripts.buildmodules.mixed.ProjectEuler import ProjectEuler
from gitlab_build_scripts.uploaders.html_generator import create_gitstats_html
from gitlab_build_scripts.parameters.mixed.ProjectEulerLanguages import Language


def build(languages: List[Language], git_repository_path: str,
          source_branch: str = "publish", target_branch: str = "master") -> None:
    """
    Builds project Euler's Readme files after running the implemented solutions of one branch and then pushes
    the results to another branch

    Note: This assumes that you have three branches: master, publish and develop.
              Develop is used to implement the solutions
              Publish gets pushed to once a problem is completed. It gets called bi Gitlab CI
              Master only gets pushed to by Gitlab Ci from the publish branch once the Readmes were completed

    :param languages:           The languages to use when generating readmes
    :param git_repository_path: The path to the (SSH) git repository
    :param source_branch:       The source branch (Publish)
    :param target_branch:       The target branch (Master)
    :return:                    None
    """
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument("mode", help="Defines the build mode. Avaliable modes are:\n"
                                         "        - refresh (local):  Runs all problem solutions. Local does not push\n"
                                         "        - update  (local):  Only Runs problem solutions without "
                                         "                            a previously successful run. Local doesn't push\n"
                                         "        - gitstats <root-html-directory>: Updates Gitstats HTML Index")
        parser.add_argument('additional', nargs='?', default=None, help="Additonal options like local or root-html-dir")
        args = parser.parse_args()

        if not (args.additional == "local"):
            checkout(target_branch, source_branch)

        if args.mode == "refresh":
            ProjectEuler.build(languages, refresh=True)
        elif args.mode == "update":
            ProjectEuler.build(languages, refresh=False)
        elif args.mode == "gitstats":
            if args.additional:
                create_gitstats_html(args.additional)
            else:
                print("Must specify gitstats HTML root directory as command line parameter")
        else:
            print("Incorrect mode specified. Use the --help flag to see the available options")
            sys.exit(1)

        if not (args.additional == "local"):
            push(target_branch, git_repository_path)

    except Exception as e:
        SentryLogger.sentry.captureException()
        raise e


def checkout(target: str, source: str) -> None:
    """
    Chacks out the target branch, then merges it with the source branch

    :param target: the target branch
    :param source: the target branch
    :return:       None
    """
    Popen(["git", "checkout", target]).wait()
    Popen(["git", "pull", "origin", target]).wait()
    Popen(["git", "merge", source, "--no-edit", "no-ff"]).wait()


def push(branch: str, repository: str) -> None:
    """
    Git-adds all, then commits, then pushes the branch

    :param branch:     the branch to push
    :param repository: the remote repository to which to push to
    :return:       None
    """
    Popen(["git", "add", "--all"]).wait()
    Popen(["git", "commit", "-m", "Updated Readme"]).wait()
    Popen(["git", "push", repository, branch]).wait()
