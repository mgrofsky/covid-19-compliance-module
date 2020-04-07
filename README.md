# Covid-19 Compliance Module

## Table of contents
- [Covid-19 Compliance Module](#covid-19-compliance-module)
  - [Table of contents](#table-of-contents)
  - [General info](#general-info)
  - [Technologies](#technologies)
  - [Setup](#setup)

## General info
Designed to be a Google Cloud Function that is triggered off a file upload to a Google Cloud Storage bucket and notify a slack channel if certain Covid-19 keywords are detected within the audio.

https://ask.ytel.com/covid-19-carrier-compliance

---

## Technologies
Project is created with:
* Google Cloud Functions
* Google Cloud Storage
* Gitlab CI/CD
* Python 3.x

---

## Setup
Recommended setup options:

**Option 1**

1. Utilize the included .gitlab-ci.yml in your project by renaming `example.gitlab-ci.yml` to `.gitlab-ci.yml`
2. Create a service account with the proper permissions and enable the cloud functions API
3. Set your Gitlab CI/CD variables
   1. $PROJECT_ID - Project this will be deployed to
   2. $SLACK_URL - Your slack url that was set up for the channel you want to post to
   3. $BUCKET_NAME = The name of the bucket where audio will be uploaded. (You do not need the `gs://` prefix)


**Option 2**

Deploying from source control
https://cloud.google.com/functions/docs/deploying/repo

For this option just remember that there are environment variables that will need to be set in the gcloud command.

```
gcloud --quiet --project $PROJECT_ID functions deploy covid_check --entry-point transcribe_audio --runtime python37 --trigger-resource $BUCKET_NAME --trigger-event google.storage.object.finalize --set-env-vars bucket_name=$BUCKET_NAME, slack_url=$SLACK_URL
```
