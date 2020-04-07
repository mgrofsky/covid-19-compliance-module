import requests
import json
import os
from google.cloud import speech_v1
from google.cloud.speech_v1 import enums

def transcribe_audio(event, context):
    # Pull in your GCF environment variables for use
    bucket_name = os.environ.get('bucket_url', 'bucket_url environment variable is not set.')
    slack_url = os.environ.get('slack_url', 'slack_url environment variable is not set.')

    file = event
    storage_uri = 'gs://' + bucket_name +'/' + file['name']
    # Change this to suit your needs.  If you are using MP3 vs wav you will need to use the speech beta imports fro your client
    # from google.cloud import speech_v1p1beta1
    # from google.cloud.speech_v1p1beta1 import enums
    if storage_uri[-4:] ==".wav":
        print(f"Processing file: {file['name']}.")
        client = speech_v1.SpeechClient()

        # Sample rate in Hertz of the audio data sent
        sample_rate_hertz = 8000

        # The language of the supplied audio
        language_code = "en-US"

        # Encoding of audio data sent. This sample sets this explicitly.
        # This field is optional for FLAC and WAV audio formats.
        encoding = enums.RecognitionConfig.AudioEncoding.MULAW
        config = {
            "sample_rate_hertz": sample_rate_hertz,
            "language_code": language_code,
            "encoding": encoding,
        }
        audio = {"uri": storage_uri}

        operation = client.long_running_recognize(config, audio)

        #print(u"Waiting for operation to complete...")
        response = operation.result()
        transcript = ""
        sendtrans = False
        keyword = "Empty Audio"

        for result in response.results:
            # First alternative is the most probable result
            alternative = result.alternatives[0]
            transcript = transcript + " " + alternative.transcript

        # Blank audio can be common.  You can choose to  send that to slack or not.  If not just set `sendtrans = False`
        if transcript.strip() == "":
            transcript = "No Sound"
            sendtrans = True
        else:
            # This is a list of keywords you will search through to find Covid-19 related terms.
            list = ["oxygen","ventilator","irs","social security","government","internal revenue","covid", "world health", "national institute", "virus", "corona","quarantine","stimulus","relief","cdc","disease", "china","pandemic","epidemic","sickness"] 
            # Using for loop 
            for i in list: 
                if i.lower() in transcript.lower():
                    keyword = i.lower()
                    sendtrans = True
                    break

        # print("Audio: '" + transcript.strip() + "'")
        if sendtrans == True:
            print(f"Sending to Slack: {file['name']}.")
            filename = file['name']
            send_slack(transcript.strip(),filename,keyword,slack_url)
        


def send_slack(transcript,filename,keyword,slack_url):
    try:
        response = requests.post(
            url=slack_url,
            headers={
                "Content-Type": "application/json",
            },
            data=json.dumps({
            "text": "*Audio:* " + filename + "\n*Transcription:* Contains *" + keyword + "*\n```" + transcript + "```"
        })
        )
        print('Response HTTP Status Code: {status_code}'.format(
            status_code=response.status_code))
        print('Response HTTP Response Body: {content}'.format(
            content=response.content))
    except requests.exceptions.RequestException:
        print('HTTP Request failed')