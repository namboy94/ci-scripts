# Gitlab Build Scripts

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

[Python Package Index Site](https://pypi.python.org/pypi/gitlab_build_scripts)

[PDF Documentation](https://docs.namibsun.net/pdf_docs/gitlab_buils_scripts/index.html)

[HTML Documentation](https://docs.namibsun.net/html_docs/gitlab_buils_scripts/index.html)

[gitstats statistics](https://gitstats.namibsun.net/gitstats/gitlab_buils_scripts/index.html)

[git_stats statistics](https://gitstats.namibsun.net/gitstats/gitlab_buils_scripts/index.html)

[Changelog](https://gitlab.namibsun.net/namboy94/gitlab_buils_scripts/raw/master/CHANGELOG)
