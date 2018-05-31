#!/usr/bin/env python
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

from typing import List
from base64 import b64decode
from colorama import Fore, Style
from subprocess import check_output


def process_call(command: List[str]) -> str:
    """
    Prints a command and executes it.
    If the exit code is not 0, the program will crash.
    :param command: The command to run
    :return: The output of the command call, stripped of whitespace
    """
    print(Fore.CYAN + " ".join(command) + Style.RESET_ALL)
    output = check_output(command).decode()
    print(Fore.MAGENTA + output + Style.RESET_ALL)
    return output.strip()


def decode_base64_string_to_file(content: str, dest: str):
    """
    Decodes a base64-encoded string and writes the result to a file
    :param content: The string to decode
    :param dest: The destination file path
    :return: None
    """
    with open(dest, "wb") as f:
        f.write(b64decode(bytes(content, "utf-8")))
