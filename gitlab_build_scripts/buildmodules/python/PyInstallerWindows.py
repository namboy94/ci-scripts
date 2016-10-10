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
from subprocess import Popen
from typing import List, Dict
from gitlab_build_scripts.buildmodules.BuildModule import BuildModule


class PyInstallerWindows(BuildModule):
    """
    Class that handles compiling a python program to a single Windows executable file
    """

    @staticmethod
    def get_identifier() -> str:
        """
        :return: pyinstaller_linux
        """
        return "pyinstaller_windows"

    # noinspection PyUnresolvedReferences
    @staticmethod
    def get_artifacts(metadata_module: 'module') -> List[Dict[str, str]]:
        """
        :param metadata_module: The metadata module of the project
        :return:                The build's release artifacts:
                                    List(Dict(file_path: content_type))
        """
        file_name = metadata_module.General.project_name + "-windows-" + metadata_module.General.version_number + ".exe"
        return [{
            "file_path": os.path.join(BuildModule.build_path, file_name),
            "content_type": "application/octet-stream"
        }]

    # noinspection PyUnresolvedReferences
    @staticmethod
    def build(metadata_module: 'module') -> None:
        """
        Starts the build process for this module

        :param metadata_module: The matadata module of the project
        :return:                None
        """
        main_py = os.path.join(metadata_module.PypiVariables.name, "main.py")
        icon_file = os.path.join(metadata_module.PypiVariables.name, "resources", "logo", "logo.ico")

        Popen(["pyinstaller",
               main_py,
               "--onefile",
               "--windowed",
               "--icon=" + icon_file]).wait()

        file_name = metadata_module.General.project_name + "-windows-" + metadata_module.General.version_number + ".exe"
        file_origin = os.path.join("dist", "main.exe")
        file_destination = os.path.join(BuildModule.build_path, file_name)

        os.rename(file_origin, file_destination)
