# Gitlab Release Uploader [![build status](https://gitlab.namibsun.net/namboy94/gitlab-release-uploader/badges/master/build.svg)](https://gitlab.namibsun.net/namboy94/gitlab-release-uploader/commits/master)

![Logo](logo/logo-readme.png "Logo")

This is a script that creates a Gitlab release. Once the Gitlab API
allows for it, uploading of release assets should be incorporated as well.

The script uses Gitlab's
[Personal Access Tokens](https://gitlab.com//profile/personal_access_tokens) to
authenticate via HTTPS, which means creating one is necessary.

# Usage

The script expects all of the following information(in that exact order):

* The Gitlab User's username
* The repository name
* The Personal Access Token
* The tag name
* The release notes. Can be either a string or a filepath.
If a file path is passed, the contents of that file are used
* A directory path in which all release assets are located in.
* (Optional) The Gitlab Host URL (When using a self-hosted Gitlab instance)
* (Optional) The target branch or commit off which to base the release on

## Current Limitations:

* The script will fail if the release already exists
* The script does not currently upload the release assets due to an API 
limitation

## Links

* [Github](https://github.com/namboy94/gitlab-release-uploader)
* [Gitlab](https://gitlab.namibsun.net/namboy94/gitlab-release-uploader)