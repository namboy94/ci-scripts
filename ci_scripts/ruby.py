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
import glob
from ci_scripts.common import process_call


def make_sure_in_path():
    """
    Makes sure the ruby paths are in the system's PATH
    :return: None
    """
    rubydir = os.path.join(os.path.expanduser("~"), ".gem/ruby")
    for version in os.listdir(rubydir):
        ruby_path = os.path.join(rubydir, version, "bin")
        os.environ["PATH"] += ":" + ruby_path


def install_gem(gem: str):
    """
    Installs a gem
    :param gem: The gem to install
    :return: None
    """
    make_sure_in_path()
    process_call(["gem", "install", gem])


def rubocop_test():
    """
    Tests the style of the ruby project using rubocop
    :return: None
    """
    install_gem("rubocop")
    process_call(["rubocop"])


def rdoc():
    """
    Creates documentation using rdoc and rsync it for use in progstats
    :return: None
    """
    install_gem("rdoc")
    process_call(["rdoc"])

    destination = os.environ["PROGSTATS_DATA_PATH"]
    project = os.environ["CI_PROJECT_NAME"]
    dest = os.path.join(destination, "doc_html", project)

    process_call(["rsync", "-a", "--delete-after", "doc/", dest])


def gem_build():
    """
    Builds gem for project
    :return: None
    """
    if not os.path.isdir("artifacts"):
        os.mkdir("artifacts")

    project = os.environ["CI_PROJECT_NAME"]

    process_call(["gem", "build", project + ".gemspec"])

    for child in os.listdir("."):
        if child.endswith(".gem"):
            os.rename(child, os.path.join("artifacts", child))


def gem_publish():
    """
    Publishes a gem
    :return: None
    """
    gemdir = os.path.join(os.path.expanduser("~"), ".gem")
    if not os.path.isdir(gemdir):
        os.mkdir(gemdir)

    cred_file = os.path.join(gemdir, "credentials")
    with open(cred_file, "w") as f:
        f.write(os.environ["RUBYGEMS_CREDENTIALS"])
    process_call(["chmod", "0600", cred_file])

    process_call(["gem", "push", glob.glob("artifacts/*.gem")])

    os.remove(cred_file)
