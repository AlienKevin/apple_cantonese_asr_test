from google.cloud import speech_v1p1beta1 as speech
from tqdm import tqdm
import json

def recognize(filename):
    client = speech.SpeechClient()
    with open(filename, "rb") as audio_file:
        content = (audio_file.read())

    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.MP3,
        sample_rate_hertz=32000,
        language_code="yue-Hant-HK",
        max_alternatives=30,
        profanity_filter=False,
        # enable_automatic_punctuation=True, # not available for Cantonese
        use_enhanced=True,
    )
    response = client.recognize(config=config, audio=audio)
    candidates = []
    for result in response.results:
        for alternative in result.alternatives:
            candidates.append({"transcript": alternative.transcript, "confidence": alternative.confidence})
    return candidates

import pandas as pd
from pathlib import Path

dataset_name = "common-voice-15"
dataset_path = Path("data")/dataset_name

metadata = pd.read_csv(dataset_path/"test.tsv", sep="\t")

results = []

for _, row in tqdm(list(metadata.iterrows())):
    result = recognize((dataset_path/"test"/row["path"]).as_posix())
    if result is not None:
        results.append({ "path": row["path"], "sentence": row["sentence"], "result": result })

with open(dataset_name + "-transcriptions.json", "w+") as output_file:
    json.dump(results, output_file, ensure_ascii=False)
