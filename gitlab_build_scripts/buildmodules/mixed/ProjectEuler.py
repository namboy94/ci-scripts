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
import json
from subprocess import Popen
from typing import List, Dict
from gitlab_build_scripts.parameters.mixed.ProjectEulerLanguages import Language

# JSON Format:
# [{language: str, runtime: float, answer: str}, ...]


class ProjectEuler(object):
    """
    Class that handles building Project Euler Readme files
    """

    @staticmethod
    def build(languages: List[Language], refresh: bool = True) -> None:
        """
        Starts the build process for the Project Euler readmes
        This method runs all programs to check

        :param languages: The languages to build
        :param refresh:   Flag that can be set to rebuild all problems. If False, will only build new ones
        :return:          None
        """
        problem_states = {}

        for problem in os.listdir("problems"):
            json_file_path = os.path.join("problems", problem, "state.json")
            if not os.path.isfile(json_file_path) or refresh:
                problem_states[problem] = {}
            else:
                with open(json_file_path, 'r') as json_file:
                    json_content = json.load(json_file)
                    problem_states[problem] = json_content

        for problem in problem_states:

            problem_state = problem_states[problem]
            problem_number = int(problem.split("-")[1])

            for language in languages:

                if not language.get_name() in problem_states:

                    # noinspection PyCallingNonCallable
                    runtime, result = language().run(problem_number)

                    problem_state[language.get_name] = {"runtime": runtime,
                                                                  "result": result}

            json_file_path = os.path.join("problems", problem, "state.json")
            with open(json_file_path, 'w') as json_file:
                json.dump(problem_state, json_file)

        ProjectEuler.generate_readmes(problem_states)








