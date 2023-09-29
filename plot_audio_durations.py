import os
import wave
from pydub import AudioSegment
import matplotlib.pyplot as plt
from tqdm.contrib.concurrent import thread_map
import threading

# Path to the directory containing the audio files
directory_path = './data/guangzhou-daily-use/test'

# List all files in the directory
all_files = os.listdir(directory_path)

# Initialize an empty list to store the lengths
audio_lengths = []

lengths_lock = threading.Lock()

def get_length(audio_file):
    file_path = os.path.join(directory_path, audio_file)
    length_in_seconds = 0

    if audio_file.lower().endswith('.wav'):
        with wave.open(file_path, 'rb') as f:
            frame_rate = f.getframerate()
            n_frames = f.getnframes()
            length_in_seconds = n_frames / frame_rate

    elif audio_file.lower().endswith('.mp3'):
        audio = AudioSegment.from_mp3(file_path)
        length_in_seconds = len(audio) / 1000  # pydub works in milliseconds

    if length_in_seconds > 0:
        lengths_lock.acquire()
        audio_lengths.append(length_in_seconds)
        lengths_lock.release()

# Loop through each file to find its length
thread_map(get_length, all_files)

# Plotting the distribution
plt.hist(audio_lengths, bins=20, edgecolor='black')
plt.title('Distribution of Audio Durations in Guangzhou Daily Use')
plt.xlabel('Durations (seconds)')
plt.ylabel('Counts')
plt.show()
