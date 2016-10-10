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
from subprocess import Popen
from gitlab_build_scripts.buildmodules.mixed.ProjectEuler import ProjectEuler


def build(source_branch: str = "publish", target_branch: str = "master") -> None:
    """
    Builds project Euler's Readme files after running the implemented solutions of one branch and then pushes
    the results to another branch

    Note: This assumes that you have three branches: master, publish and develop.
              Develop is used to implement the solutions
              Publish gets pushed to once a problem is completed. It gets called bi Gitlab CI
              Master only gets pushed to by Gitlab Ci from the publish branch once the Readmes were completed

    :param source_branch: The source branch (Publish)
    :param target_branch: The target branch (Master)
    :return:              None
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", help="Defines the build mode. Avaliable modes are:\n"
                                     "        - refresh:  Runs all problem solutions"
                                     "        - update:   Only Runs problem solutions without a previously successful"
                                     "                    run.")
    args = parser.parse_args()

    checkout(target_branch, source_branch)

    if args.mode == "refresh":
        ProjectEuler.build(refresh=True)
    elif args.mode == "update":
        ProjectEuler.build(refresh=False)
    else:
        print("Incorrect mode specified. Use the --help flag to see the available options")
        sys.exit(1)

    push(target_branch)


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


def push(branch: str) -> None:
    """
    Git-adds all, then commits, then pushes the branch

    :param branch: the branch to push
    :return:       None
    """
    Popen(["git", "add", "--all"]).wait()
    Popen(["git", "commit", "-m", "Updated Readme"]).wait()
    Popen(["git", "push", "origin", branch]).wait()
