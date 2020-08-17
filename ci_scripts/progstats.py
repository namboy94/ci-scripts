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
from ci_scripts.common import process_call


def progstats_transfer(data: str, topic: str, project: str):
    """
    Transfers progstats contents to the progstats instance using rsync
    :param data: The path to the data to transfer
    :param topic: The progstats topic name
    :param project: The progstats project name
    :return: None
    """

    progstats_data_path = os.environ["PROGSTATS_DATA_PATH"]
    progstats_data_port = os.environ["PROGSTATS_DATA_PORT"]
    progstats_host = progstats_data_path.split(":")[0]
    destination = os.path.join(progstats_data_path, topic, project)
    project_path = destination.split(":")[1]

    if os.path.isdir(data) and not data.endswith("/"):
        data += "/"
    elif os.path.isfile(data):
        destination += "." + data.rsplit(".")[1]

    mkdir_cmd = [
        "ssh",
        "-p", progstats_data_port,
        progstats_host,
        "mkdir -p " + project_path
    ]
    rsync_cmd = [
        "rsync",
        "-a",
        "--delete-after",
        "-e", "ssh -p " + progstats_data_port,
        data,
        destination
    ]
    process_call(mkdir_cmd)
    process_call(rsync_cmd)
