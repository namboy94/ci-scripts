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


import os
from shutil import copyfile
from urllib.request import urlretrieve
from ci_scripts.common import process_call


def install_composer():
    """
    Installs composer locally
    :return: None
    """
    urlretrieve("https://getcomposer.org/installer", "install-composer")
    process_call(["php", "install-composer"])
    os.remove("install-composer")


def checkstyle():
    """
    Runs checkstyle on the PHP project
    :return: None
    """
    process_call(["./composer.phar", "update"])
    process_call([
        "php", "vendor/phpcheckstyle/phpcheckstyle/run.php",
        "--src", "src", "--src", "test", "--config", "config/checkstyle.xml"
    ])


def unittest():
    """
    Runs PHP unit tests
    :return: None
    """
    process_call(["./composer.phar", "update"])
    copyfile("config/phpunit.xml", "phpunit.xml")
    process_call([
        "vendor/bin/phpunit", "test", "--coverage-html=coverage"
    ])
    os.remove("phpunit.xml")

    dest = os.path.join(
        os.environ["PROGSTATS_DATA_PATH"],
        "coverage",
        os.environ["CI_PROJECT_NAME"]
    )
    process_call(["rsync", "-a", "--delete-after", "coverage/", dest])
