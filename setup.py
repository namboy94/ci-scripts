"""LICENSE
Copyright 2017 Hermann Krumrey

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

# imports
import os
from setuptools import setup, find_packages


if __name__ == "__main__":

    setup(
        name="ci-scripts",
        version=open("version", "r").read(),
        description="Scripts to streamline Gitlab CI builds",
        long_description=open("README.md", "r").read(),
        author="Hermann Krumrey",
        author_email="hermann@krumreyh.com",
        classifiers=[
            "License :: OSI Approved :: GNU General Public License v3 (GPLv3)"
        ],
        url="https://gitlab.namibsun.net/namibsun/python/ci-scripts",
        license="GNU GPL3",
        packages=find_packages(),
        scripts=list(map(lambda x: os.path.join("bin", x), os.listdir("bin"))),
        install_requires=[
            "requests",
            "typing"
            # These are needed for play-upload
            # "google-api-python-client",
            # "pyOpenSSL",
            # "httplib2"
        ],
        include_package_data=True,
        zip_safe=False
    )
