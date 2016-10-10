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
import os
from typing import List, Dict


class BuildModule(object):
    """
    Class that models an abstract python BuildModule that can be extended by other classes to create custom build
    steps
    """

    build_path = os.path.join("build", "gitlab_build_scripts")

    @staticmethod
    def get_identifier() -> str:
        """
        :return: A unique string identifier for this build module
        """

    # noinspection PyUnresolvedReferences
    @staticmethod
    def get_artifacts(metadata_module: 'module') -> List[Dict[str, str]]:
        """
        :param metadata_module: The metadata module of the project
        :return:                The build's release artifacts:
                                    List(Dict(file_path: content_type))
        """
        raise NotImplementedError()

    # noinspection PyUnresolvedReferences
    @staticmethod
    def build(metadata_module: 'module') -> None:
        """
        Starts the build process for this module

        :param metadata_module: The matadata module of the project
        :return:                None
        """
        raise NotImplementedError()