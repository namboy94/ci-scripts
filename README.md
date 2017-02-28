# HTML Index Generator [![build status](https://gitlab.namibsun.net/namboy94/html-index-generator/badges/master/build.svg)](https://gitlab.namibsun.net/namboy94/html-index-generator/commits/master)

![Logo](logo/logo-readme.png "Logo")

This script creates a bootstrap-powered HTML index page for a directory.
The content of the directory is shown as a nested unordered list.

## Usage

The script is used by running

   python html-index-generator.py <target directory> <target index.html file>

A parameter ```-t``` may be passed to specify a template file (by default
[template.html](template.html) is used) to be used when generating the
index.html file.

The title of the HTML page can be specified using the ```-n``` parameter.
If it is not supplied, the directory is searched for a file called ```title```
and uses its contents as the title. If this file does not exist, the
title will default to "Title"

### Formatting the template file

The script replaces all instances of ```@TITLE``` with the title of the
directory and all ```@CONTENT```s with the unordered nested list of the
directory structure.

## Links

* [Github](https://github.com/namboy94/html-index-generator)
* [Gitlab](https://gitlab.namibsun.net/namboy94/html-index-generator)
* [Git Statistics (gitstats)](https://gitstats.namibsun.net/gitstats/html-index-generator/index.html)
* [Git Statistics (git_stats)](https://gitstats.namibsun.net/git_stats/html-index-generator/index.html)
