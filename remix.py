import sys
import csv
from pydub import AudioSegment

csv_filename = sys.argv[1]
input_filename = sys.argv[2]
output_filename = sys.argv[2].replace(".wav", ".onesided.wav")

full_audio = AudioSegment.from_wav(input_filename)
segments = AudioSegment.empty()

with open(csv_filename) as csvfile:
    reader = csv.reader(csvfile)
    for start, end, speaker in reader:
        if speaker in ["SPEAKER_00", "SPEAKER_00"]:
            start = float(start) * 1000
            end = float(end) * 1000

            # Fix clipping of first sample
            if start < 500:
                start = 0
            print(f"{start / float(len(full_audio))*100:.0f}%")
            segments += full_audio[start:end]

segments.export(f"{output_filename}", format="wav")
