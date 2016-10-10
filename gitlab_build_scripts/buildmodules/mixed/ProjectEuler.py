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
from typing import List, Dict, Tuple
from gitlab_build_scripts.parameters.mixed.ProjectEulerLanguages import Language

# JSON Format:
# [{language: str, runtime: float, answer: str}, ...]


class ProjectEuler(object):
    """
    Class that handles building Project Euler Readme files
    """

    build_passed = "[![Wercker]" \
                   "(https://img.shields.io/wercker/ci/wercker/docs.svg?maxAge=2592000)]()"
    build_failed = "[![Codeship]" \
                   "(https://img.shields.io/codeship/d6c1ddd0-16a3-0132-5f85-2e35c05e22b1.svg?maxAge=2592000)]()"
    build_invalid = "[![TeamCity CodeBetter]" \
                    "(https://img.shields.io/teamcity/codebetter/bt428.svg?maxAge=2592000)]()"

    # noinspection PyCallingNonCallable
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
            problem_number = int(problem.split("-")[1])

            if not os.path.isfile(json_file_path) or refresh:
                problem_states[problem_number] = {}
            else:
                with open(json_file_path, 'r') as json_file:
                    json_content = json.load(json_file)
                    problem_states[problem_number] = json_content

        for problem in problem_states:

            problem_state = problem_states[problem]

            for language in languages:

                if not language().get_name() in problem_states:

                    run_result = language().run(problem)
                    if run_result is not None:

                        runtime, result = run_result
                        problem_state[language().get_name()] = {"runtime": runtime,
                                                                "result": result}

            json_file_path = os.path.join("problems", "problem-" + str(problem).zfill(4), "state.json")
            with open(json_file_path, 'w') as json_file:
                json.dump(problem_state, json_file)

        ProjectEuler.generate_readmes(languages, problem_states)

    @staticmethod
    def generate_language_header(language_names: List[str]) -> str:
        """
        Generates a language table header for a list of language names

        :param language_names: the languages to use
        :return:               the language markdown header
        """
        header = "|"
        subheader = "|"
        for language in sorted(language_names):
            header += language.ljust(5) + "|"
            subheader += ":" + (max(3, len(language) - 2) * "-") + ":|"

        return header + "\n" + subheader

    @staticmethod
    def generate_badge_and_runtime(problem: Dict[str, Dict[str, str or float]],
                                   language: str,
                                   correct_result: str,
                                   decimals: int) -> Tuple[str, str]:
        """
        Generates the build badge and the runtime for the specified

        :param problem:        the problem for whom to generate this information
        :param language:       the language to consider
        :param correct_result: the correct result of the problem
        :param decimals:       amount of decimal numbers after the '.' in the runtime number
        :return:               the build, badge, the formatted runtime
        """
        badge = ProjectEuler.build_invalid
        runtime = "---"

        if language in problem:
            if problem[language]["result"] == correct_result:
                badge = ProjectEuler.build_passed
            else:
                badge = ProjectEuler.build_failed

            '{0:.{1}%}'.format(problem[language]["runtime"], decimals)

        return badge, runtime

    @staticmethod
    def generate_readmes(languages: List[Language], problem_states: Dict[int, Dict[str, Dict[str, str or float]]]) \
            -> None:
        """
        Generates the README files from the previously established problem states.

        :param languages:      list of languages used in this project
        :param problem_states: the problem states: Dict[problem_#: Dict["language": Dict["runtime", "results"]]]
        :return:               None
        """
        # noinspection PyCallingNonCallable
        language_names = list(language().get_name() for language in languages)

        main_readme = "# Project Euler\n\nImplementations of Project Euler problems in various languages\n\n"
        main_readme += "## Problem Status:\n\n|Problem" + ProjectEuler.generate_language_header(language_names) + "\n"
        runtime_table = "\n## Runtimes:\n\n|:-----:" + ProjectEuler.generate_language_header(language_names) + "\n"

        for problem in sorted(problem_states):

            problem_state = problem_states[problem]
            correct_result = ProjectEuler.generate_problem_readme(problem_state, problem, language_names)
            problem_link = "[" + str(problem) + "](" + os.path.join("problems",
                                                                    "problem-" + str(problem).zfill(4),
                                                                    "README.md") + ")"

            main_table_entry = "|" + problem_link + "|"
            runtime_table_entry = "|" + problem_link + "|"

            for language in language_names:

                badge, runtime = ProjectEuler.generate_badge_and_runtime(problem_state, language, correct_result, 4)
                main_table_entry += badge + "|"
                runtime_table_entry += runtime + "|"

            main_readme += main_table_entry + "\n"
            runtime_table += runtime_table_entry + "\n"

        with open("README.md", 'w') as readme:
            readme.write(main_readme + runtime_table)

    @staticmethod
    def generate_problem_readme(problem: Dict[str, Dict[str, str or float]],
                                problem_number: int,
                                language_names: List[str]) -> str:
        """
        Generates the Readme for a single problem

        :param problem:        the problem to turn into a readme file
        :param problem_number: the problem's number
        :param language_names: list of language names to be displayed in the readme
        :return:               the result of the readme
        """
        problem_readme = "# Problem " + str(problem_number) + "\n\n"

        problem_directory = os.path.join("problems", "problem-" + str(problem_number).zfill(4))
        with open(os.path.join(problem_directory, "PROBLEM.md"), 'r') as template:
            problem_readme += template.read() + "\n\n"

        problem_readme = problem_readme.rstrip().lstrip()
        correct_result = problem_readme.rsplit("Answer: ", 1)[1]

        problem_readme += "## Stats:\n\n"
        problem_readme += "|Language|Status|Answer|Runtime|\n"
        problem_readme += "|:---:|:---:|:---:|:---:|\n"

        for language in sorted(language_names):

            badge, runtime = ProjectEuler.generate_badge_and_runtime(problem, language, correct_result, 6)
            result = "---" if runtime == "---" else problem[language]["result"]
            # noinspection PyTypeChecker
            problem_readme += "|" + language + "|" + badge + "|" + result + "|" + runtime + "|\n"

        with open(os.path.join(problem_directory, "README.md"), 'w') as readme:
            readme.write(problem_readme)

        return correct_result
