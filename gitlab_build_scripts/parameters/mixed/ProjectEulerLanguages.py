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
import time
from typing import Tuple, List, Dict
from subprocess import check_output, CalledProcessError


class Language(object):
    """
    Models a generic language
    """

    # The Language's parameters
    # For the *_command parameters, which are lists of instructions, ### and @@@ are special variables
    # @@@ := the script's full filename, e.g. script.py
    # ### := the script's name, without the extension, e.g. script

    name = None              # The Display name in the Readme of the language
    compile_command = None   # The command used for compiling
    run_command = None       # The command used for running the program
    cleanup_command = None   # The command used for returning the directory into its previous state
    directory_name = None    # The name of the directory in which the language resides in
    extension = None         # The file extension used by the programming language

    def get_name(self) -> str:
        """
        :return: the name of the language
        """
        return self.name

    @staticmethod
    def create_command(command_formula: List[str], script: Dict[str, str]) -> List[str]:
        """
        Creates a working command list for Popen from a command formula and a script

        :param command_formula: the command formula to use
        :param script:          the script to use
        :return:                the valied command list
        """
        command = []
        for directive in command_formula:
            command.append(directive.replace("@@@", script["filename"]).replace("###", script["filename_no_ext"]))
        return command

    def run(self, problem_number: int) -> (Tuple[float, str]) or None:
        """
        Runs the specified problem in this language
        If multiple script implementations are found, only the fastest one will be considered

        :param problem_number: the problem number to solve
        :return:               the time it took to solve the problem, the result of the computation
                                    or None if no script was executed
        """
        problem_lang_dir = os.path.join("problems", "problem-" + str(problem_number).zfill(4), self.directory_name)
        scripts = []

        if not os.path.isdir(problem_lang_dir):
            return None

        for script in os.listdir(problem_lang_dir):
            if script.endswith(self.extension):
                scripts.append({"filename": script,                            # @@@
                                "filename_no_ext": script.rsplit(".", 1)[0]})  # ###

        current_working_directory = os.getcwd()
        os.chdir(problem_lang_dir)

        fastest_script = None

        for script in scripts:
            start_time = time.time()

            if self.compile_command is not None:
                try:
                    check_output(self.create_command(self.compile_command, script))
                except (CalledProcessError, FileNotFoundError, Exception):
                    pass

            try:
                output = check_output(self.create_command(self.run_command, script)).decode().rstrip().lstrip()
            except (CalledProcessError, FileNotFoundError, Exception):
                output = ""

            if self.cleanup_command is not None:
                try:
                    check_output(self.create_command(self.cleanup_command, script))
                except (CalledProcessError, FileNotFoundError, Exception):
                    pass

            end_time = time.time()

            script["time_delta"] = end_time - start_time
            script["output"] = output

            if fastest_script is None:
                fastest_script = script
            else:
                if fastest_script["time_delta"] > script["time_delta"]:
                    fastest_script = script

        os.chdir(current_working_directory)

        if fastest_script is not None:
            return fastest_script["time_delta"], fastest_script["output"]
        else:
            return None


class C(Language):
    """
    The C Programming Language
    """

    name = "C"
    compile_command = ["gcc", "-o", "out", "-std=c99", "@@@"]
    run_command = ["./out"]
    cleanup_command = ["rm", "out"]
    directory_name = "c"
    extension = ".c"


class COptimized(C):
    """
    The C Programming Language, with compiler optimization
    """

    name = "C Optimized"
    compile_command = ["gcc", "-o", "out", "-O3", "-std=c99", "@@@"]


class Go(Language):
    """
    The Go Programming Language, interpreted
    """

    name = "Go"
    run_command = ["go", "run", "@@@"]
    directory_name = "go"
    extension = ".go"


class GoCompiled(Go):
    """
    The Go Programming Language, compiled
    """

    name = "Go Compiled"
    compile_command = ["go", "build", "-o", "out", "@@@"]
    run_command = ["./out"]
    cleanup_command = ["rm", "out"]


class Haskell(Language):
    """
    The Haskell Programming Language, compiled
    """

    name = "Haskell"
    compile_command = ["ghc", "-o", "out", "@@@"]
    run_command = ["./out"]
    cleanup_command = ["rm", "out", "###.hi", "###.o"]
    directory_name = "haskell"
    extension = ".hs"


class HaskellOptimized(Haskell):
    """
    The Haskell Programming Language, compiled with optimization flags
    """

    name = "Haskell Optimized"
    compile_command = ["ghc", "-o", "out", "-O2", "-optc-O3", "@@@"]


class Java(Language):
    """
    The Java Programming Language
    """

    name = "Java"
    compile_command = ["javac", "@@@"]
    run_command = ["java", "###"]
    cleanup_command = ["rm", "###.class"]
    directory_name = "java"
    extension = ".java"


class Python(Language):
    """
    The Python Programming Language
    """

    name = "Python"
    run_command = ["python", "@@@"]
    directory_name = "python"
    extension = ".py"


class PythonPyPy(Python):
    """
    The Python Programming Language, ran with the Pypy interpreter
    """

    name = "Python PyPy"
    run_command = ["pypy", "@@@"]


class Ruby(Language):
    """
    The Ruby Programming Language
    """

    name = "Ruby"
    run_command = ["ruby", "@@@"]
    directory_name = "ruby"
    extension = ".rb"


class Rust(Language):
    """
    The Rust Programming Language
    """

    name = "Rust"
    compile_command = ["rustc", "@@@"]
    run_command = ["./###"]
    cleanup_command = ["rm", "###"]
    directory_name = "rust"
    extension = ".rs"


class RustOptimized(Rust):
    """
    The Rust Programming Language, compiled with optimization flags
    """

    name = "Rust Optimized"
    compile_command = ["rustc", "-O", "@@@"]
