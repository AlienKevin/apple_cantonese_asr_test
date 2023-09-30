import os
import azure.cognitiveservices.speech as speechsdk
import json
from pydub import AudioSegment
from tqdm import tqdm

tmp_wav_filename = "tmp.wav"

def recognize(filename):
    # This example requires environment variables named "SPEECH_KEY" and "SPEECH_REGION"
    speech_config = speechsdk.SpeechConfig(subscription=os.environ.get('SPEECH_KEY'), region=os.environ.get('SPEECH_REGION'))
    speech_config.speech_recognition_language="zh-HK"
    speech_config.output_format = speechsdk.OutputFormat.Detailed
    speech_config.set_profanity(speechsdk.ProfanityOption.Raw)

    if filename.endswith(".mp3"):
        audio = AudioSegment.from_mp3(filename)
        audio.export(tmp_wav_filename, format="wav")
        audio_config = speechsdk.audio.AudioConfig(filename=tmp_wav_filename)
    else:
        assert(filename.endswith(".wav"))
        audio_config = speechsdk.audio.AudioConfig(filename=filename)

    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
    speech_recognition_result = speech_recognizer.recognize_once()

    os.remove(tmp_wav_filename)

    if speech_recognition_result.reason == speechsdk.ResultReason.RecognizedSpeech:
        return json.loads(speech_recognition_result.json)
    elif speech_recognition_result.reason == speechsdk.ResultReason.NoMatch:
        print("No speech could be recognized: {}".format(speech_recognition_result.no_match_details))
    elif speech_recognition_result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = speech_recognition_result.cancellation_details
        print("Speech Recognition canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))
            print("Did you set the speech resource key and region values?")

import pandas as pd
from pathlib import Path

dataset_name = "common-voice-11-zh-hk"
dataset_path = Path("data")/dataset_name

metadata = pd.read_csv(dataset_path/"test.tsv", sep="\t")

results = []

for _, row in tqdm(list(metadata.iterrows())):
    result = recognize((dataset_path/"test"/row["path"]).as_posix())
    if result is not None:
        results.append({ "path": row["path"], "sentence": row["sentence"], "result": result })

with open(dataset_name + "-transcriptions.json", "w+") as output_file:
    json.dump(results, output_file, ensure_ascii=False)
