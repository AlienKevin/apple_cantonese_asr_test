from pathlib import Path
import pandas as pd
import os
import shutil

data_dir = Path("data/guangzhou-daily-use-original/")
target_dir = Path("data/guangzhou-daily-use/")
target_data_dir = target_dir/"test"

os.makedirs(target_data_dir, exist_ok=True)

metadata = pd.read_csv(data_dir/"UTTRANSINFO.txt", sep="\t")

with open(target_dir/"test.tsv", "w+") as target_metadata:
    target_metadata.write("path\tsentence\n")
    for _, row in metadata.iterrows():
        path = row["UTTRANS_ID"]
        speaker = row["SPEAKER_ID"]
        sentence = row["TRANSCRIPTION"]
        target_metadata.write(path + "\t" + sentence + "\n")
        shutil.copy(data_dir/"WAV"/speaker/path, target_data_dir)
