# Project Euler Builder

The Project Euler Builder assumes a project structure like this:

    - project-euler
    --- builder.py
    --- problems
    ----- problem-0001
    ------- PROBLEM.md
    ------- python
    ------- c
    ------- etc.
    ----- problem-0002
    ----- etc
    

## File Structures

### builder.py

A typical builder.py file would look like this:

    from gitlab_build_scripts.project_builders.project_euler import build
    from gitlab_build_scripts.parameters.mixed.ProjectEulerLanguages import *
    
    
    if __name__ == "__main__":
        build([C, 
               COptimized, 
               Go, 
               GoCompiled,
               Haskell,
               HaskellOptimized,
               Java,
               Python,
               PythonPyPy,
               Ruby,
               Rust,
               RustOptimized], 
               "git@gitlab.namibsun.net:/namboy94/project-euler.git",
               "publish", master")
               
Where you can select the languages you would like project euler to use.
Additionally, you should specify the project's Git repository path so that the results
can be pushed over SSH. After the repository, you can optionally specify the source and
destination branches of the build.

### PROBLEM.md

The PROBLEM.md files contain the Project Euler problems in markdown format.
At the end of the file, there has to be a line like this:

    Answer: X
    
Which is used to check if the programs output the correct answer.

## Usage

To build the README files, run

    python builder.py refresh
    
    or
    
    python builder.py update
    
Where ```refresh``` runs all problems again, and ```update``` only the ones
that were not run before, or for which the JSON data is missing.

The build will automatically push to the specified branch. To disable this,
add the 'local' positional argument


Git statistics index can be built using ```python builder.py gitstats```