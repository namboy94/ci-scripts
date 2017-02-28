# Github Release Uploader [![build status](https://gitlab.namibsun.net/namboy94/github-release-uploader/badges/master/build.svg)](https://gitlab.namibsun.net/namboy94/github-release-uploader/commits/master)

![Logo](logo/logo-readme.png "Logo")

This is a script that creates a Github release. It also allows uploading
release assets like compiled binaries.

The script uses Github's
[Personal Access Tokens](https://github.com/settings/tokens) to
authenticate via HTTPS, which means creating one is necessary.

# Usage

The script expects all of the following information(in that exact order):

* The Github User's username
* The repository name
* The Personal Access Token
* The tag name
* The release notes. Can be either a string or a filepath. 
If a file path is passed, the contents of that file are used
* A directory path in which all release assets are located in.
* (Optional) The target branch or commit off which to base the release on

## Current Limitations:

* The script will fail if the release already exists

## Links

* [Github](https://github.com/namboy94/github-release-uploader)
* [Gitlab](https://gitlab.namibsun.net/namboy94/github-release-uploader)