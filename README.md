# Changelog Reader [![build status](https://gitlab.namibsun.net/namboy94/changelog-reader/badges/master/build.svg)](https://gitlab.namibsun.net/namboy94/changelog-reader/commits/master)

![Logo](logo/logo-readme.png "Logo")

**Note**: Names surrounded by <> are variables, the <> are not part of the
changelog syntax. All Whitespace in a line before the first significant
character is ignored when reading.

This script reads a changelog file written in the following format:

    <VersionName>:
        <Description_Line_One>
        - <Description_Line_Two>
    V <OtherVersionName>:
        - <AnotherDescription>

and writes the most recent changelog entry to a file in the format:

    Changelog Version ```<ProcessedVersionName>```

        - <Description_Line_One>
        - <Description_Line_Two>

## Formatting the Changelog

```VersionName```s can be written with or without a leading ```V ``` or ```V.```
but needs to be seperated by those by at least one space. The case of the
```v```'s don't matter. The ```V```s may also be ```Version```, the behaviour
is the same. The line containing the ```VersionName``` may not
start with any kind of Whitespace.

The ```Description``` lines need to start with some form of whitespace. The 
Description may also start with a ```- ```. This will be removed and later
added back when writing to file.

Empty lines are ignored completely

## Usage

To use the script, a ```CHANGELOG``` file must be provided. If a ```CHANGELOG```
file is not provided via command line parameter, the script will automatically
look in the current directory for a file called ```CHANGELOG``` and use that if
it exists.

A destination file should also be provided. If not, the output will simply be
printed to the terminal. If the destination file already exists, the script
will refuse to execute as a safety mechanism.

An example of running this script would look like this:

    python changelog-reader.py -c CHANGELOG -d change_message

This will read the ```CHANGELOG``` file, extract the latest version entry
and write it formatted into the change_message file.

## Links

* [Github](https://github.com/namboy94/changelog-reader)
* [Gitlab](https://gitlab.namibsun.net/namboy94/changelog-reader)
* [Git Statistics (gitstats)](https://gitstats.namibsun.net/gitstats/changelog-reader/index.html)
* [Git Statistics (git_stats)](https://gitstats.namibsun.net/git_stats/changelog-reader/index.html)

