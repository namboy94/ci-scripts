# play-upload.py  [![build status](https://gitlab.namibsun.net/namboy94/play-upload/badges/master/build.svg)](https://gitlab.namibsun.net/namboy94/play-upload/commits/master)

![Logo](logo/logo-readme.png "Logo")

play-upload is a script that streamlines uploading releases to the Google Play
store.

##Dependencies

To use this script, you will have to install the python packages
```google-api-python-client``` and ```pyOpenSSL```,
which can easily be installed via ```pip``` using the following command:

    pip install google-api-python-client pyOpenSSL --user --upgrade
    
##Usage

The script requires the following positional arguments:

* package: This is the name of the app uploaded to the play store, 
           for example: ```com.android.example```. Substitute this
           with your own package name.
* track: The track to which the new release should be uploaded. May
         be any of the following: ```rollout```, ```production```,
         ```beta```, ```alpha```.
* email: This is the email address of the Google Service Account
         which is used to authenticate via the Play Store API.
         More information under the section ```Prepare The API Credentials```.
* keyfile: The file path to the ```.p12``` key file used to authenticate with
           the Play Store API.
           More information under the section ```Prepare The API Credentials```.
* apks: The path to the APK file to upload. Can also contain a wildcard
        character to upload multiple files.

These all have to be provided, otherwise the script will fail. Additionally,
the ```--changes``` option may be passed to upload release notes. To do this,
create a text file containing the release notes. The file name of this file
should be the language/country code of the release notes, for example
```en-US``` for US English or ```de-DE``` for German.

If you want to upload multiple release notes (for different languages),
you can pass the files as a comma seperated string (example: "en-US,de-DE")

## Prepare the API credentials

To make use of the script, you will have to generate API credentials for use
with the Play Store API first.

First, go to
[https://console.developers.google.com](https://console.developers.google.com).
Then make sure you activate the ```Google Play Android Developer API``` in the
Dashboard.

Afterwards, if you have not done so previously, create a new project for your
app. Once that has been done, go to the
[https://console.developers.google.com/iam-admin](https://console.developers.google.com/iam-admin)
page and select the ```Service Accounts``` option and create a new Service
account. Enter the personalized values you want, make sure to
give the account the necessary privileges and check the
```Furnish a new private key ``` option while selecting ```P12```.

Your browser will now download a ```.p12``` file, which you need to
keep safe, there is no way to regenerate that key. This is the private
key file used by the script to authenticate with the API. The generated email
address of the service account is the ```email``` option.

Once this configuration is done, you will have to grant that service
account access to your Play Store project. To do this, go to
[https://play.google.com/apps/publish/](https://play.google.com/apps/publish/)
and follow the menu options: ```Settings -> API access```.

Here you can grant the service account access to your app.

Once this is done, you're all set!

## Links

* [Github](https://github.com/namboy94/play-upload)
* [Gitlab](https://gitlab.namibsun.net/namboy94/play-upload)
* [Git Statistics (gitstats)](https://gitstats.namibsun.net/gitstats/play-upload/index.html)
* [Git Statistics (git_stats)](https://gitstats.namibsun.net/git_stats/play-upload/index.html)
