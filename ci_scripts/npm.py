"""LICENSE
Copyright 2017 Hermann Krumrey <hermann@krumreyh.com>

This file is part of ci-scripts.

ci-scripts is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

ci-scripts is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with ci-scripts.  If not, see <http://www.gnu.org/licenses/>.
LICENSE"""

from ci_scripts.common import process_call


def install_package(package: str):
    """
    Installs an npm package
    :param package: The name of the package to install
    :return: None
    """
    process_call(["npm", "install", package])
