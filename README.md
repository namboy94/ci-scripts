# Gitlab Build Scripts

![Logo](gitlab_build_scripts/resources/logo/logo_256.png)

A collection of configurable scripts for use with gitlab CI builds.

## Installation

    pip install gitlab_build_scripts
    
    or 
    
    python setup.py install
    
You can also use the ```--user``` flag to install the scripts as a user

## Usage

The scripts are configured via a builder.py file in the top-level directory of
a project. In this file, the builder(s) are configured by importing the appropriate
modules and executing them. For example, a python project that builds
executables using PyInstaller would have a builder.py file like this:

    from gitlab_build_scripts.project_builders.python import build
    from gitlab_build_scripts.buildmodules.python.PyInstallerLinux import PyInstallerLinux
    
    if __name__ == "__main__":
        build([PyInstallerLinux])

Since different project types require different build setups, each builder type needs to be
documented seperately. Follow any of these links to learn more:

  - [Python Builder](doc/markdown/python.md)
  - [Project Euler Builder](doc/markdown/project_euler.md)

## Additional Links

* [Changelog](https://gitlab.namibsun.net/namboy94/gitlab-buils-scripts/raw/master/CHANGELOG)
* [Gitlab](https://gitlab.namibsun.net/namboy94/gitlab-build-scripts)
* [Github](https://github.com/namboy94/gitlab-build-scripts)
* [Python Package Index Site](https://pypi.python.org/pypi/gitlab_build_scripts)
* [Documentation(HTML)](https://docs.namibsun.net/html_docs/gitlab_buils_scripts/index.html)
* [Documentation(PDF)](https://docs.namibsun.net/pdf_docs/gitlab_buils_scripts.pdf)
* [Git Statistics (gitstats)](https://gitstats.namibsun.net/gitstats/gitlab_buils_scripts/index.html)
* [Git Statistics (git_stats)](https://gitstats.namibsun.net/gitstats/gitlab_buils_scripts/index.html)
* [Test Coverage](https://coverage.namibsun.net/gitlab-build-scripts/index.html)
