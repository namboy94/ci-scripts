#!/usr/bin/env python
"""
Copyright Hermann Krumrey <hermann@krumreyh.com>, 2017

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import os
import sys
import argparse
import httplib2
from oauth2client import client
# noinspection PyUnresolvedReferences
from apiclient.discovery import build as build_google_service
from oauth2client.service_account import ServiceAccountCredentials


def parse_args():
    """
    Parses the command line arguments
    :return: The parsed arguments as an argparse Namespace
    """

    parser = argparse.ArgumentParser()
    parser.add_argument("package",
                        help="The name of the package to upload to,"
                             "for example: com.android.example")
    parser.add_argument("track",
                        help="The track to which to upload the release to. May"
                             " be 'rollout', 'production', 'beta' or 'alpha'")
    parser.add_argument("email",
                        help="The Google API Service Account Email address")
    parser.add_argument("keyfile",
                        help="The p12 keyfile provided by the Google API")
    parser.add_argument("apks",
                        help="The APK file(s) to upload")
    parser.add_argument("-c", "--changes",
                        help="Can be used to specify a file containing changes"
                             " to the new version of the app. The file must"
                             " be called 'en-US' or 'de-DE' or similar."
                             " Multiple of these files can be provided by"
                             " seperating the file paths with commas")
    args = parser.parse_args()

    if args.track not in ["rollout", "production", "beta", "alpha"]:
        print("Invalid track " + args.track + " selected.")
        sys.exit(1)

    return args


def main():
    """
    The main method of the script. Parses the arguments and then attempts to
    upload the release to the Google Play Store
    :return: None
    """

    args = parse_args()

    try:
        service_info = build_service(args.email, args.keyfile, args.package)
        version_code = upload_apks(service_info, args.apks)
        set_apk_track_info(service_info, args.track, version_code)
        upload_release_notes(service_info, version_code, args.changes)

        commit_request = service_info["service"].edits().commit(
            editId=service_info["edit_id"], packageName=args.package).execute()

        print("Edit " + commit_request['id'] + " has been committed")

    except client.AccessTokenRefreshError:
        print("Authentication Failed")
        sys.exit(1)


def build_service(email, keyfile, package_name):
    """
    Builds the Google API service used for all further API interactions
    :param email: The API Service Account email address
    :param keyfile: The p12 keyfile location
    :param package_name: The name of the package to upload to
    :return: The Service, the edit request ID and the package name
             as a dictionary for convenient further use
    """

    credentials = ServiceAccountCredentials.from_p12_keyfile(
        email, keyfile,
        scopes="https://www.googleapis.com/auth/androidpublisher"
    )

    http = httplib2.Http()
    http = credentials.authorize(http)
    service = build_google_service("androidpublisher", "v2", http=http)

    edit_request = service.edits().insert(body={}, packageName=package_name)
    return {"service": service,
            "edit_id": edit_request.execute()["id"],
            "package": package_name}


def upload_apks(service_info, apks):
    """
    Uploads any APK files provided via the command line arguments
    :param service_info: The previously established service info dictionary
    :param apks: The APK files to upload
    :return: The uploaded version code for the APK
    """
    apk_response = service_info["service"].edits().apks().upload(
        editId=service_info["edit_id"],
        packageName=service_info["package"],
        media_body=apks).execute()

    version_code = apk_response['versionCode']
    print("Uploaded APK for version " + str(version_code))
    return version_code


def set_apk_track_info(service_info, track, version_code):
    """
    Sets the specified track to include the specified version
    :param service_info: The previously generated API service dictionary
    :param track: The track to apply these changes to
    :param version_code: The version code to add to the track
    :return: None
    """
    service_info["service"].edits().tracks().update(
        editId=service_info["edit_id"],
        track=track,
        packageName=service_info["package"],
        body={"versionCodes": [version_code]}).execute()

    print("Version " + str(version_code) + " has been assigned "
                                           "to track " + track + ".")


def upload_release_notes(service_info, version_code, change_notes):
    """
    Uploads release notes for various languages
    :param service_info: The service dictionary
    :param version_code: The version code of the APK
    :param change_notes: The release notes to upload, stored in files,
                         whose paths are provided in a comma-separated string.
                         The language is determined by the name of the file
    :return: None
    """

    for notes in change_notes.rstrip().lstrip().split(","):

        language = os.path.basename(notes)
        with open(notes, 'r') as notes_file:
            changes = notes_file.read()

        service_info["service"].edits().apklistings().update(
            editId=service_info["edit_id"],
            packageName=service_info["package"],
            language=language,
            apkVersionCode=version_code,
            body={'recentChanges': changes}).execute()

        print("Release Notes for language " + language + " were updated.")


if __name__ == "__main__":
    main()
    print("Done")
    sys.exit(0)
