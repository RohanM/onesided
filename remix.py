import csv
from pydub import AudioSegment

full_audio = AudioSegment.from_wav("lex-367-sam-altman-sample.wav")
segments = AudioSegment.empty()

with open("dz.csv") as csvfile:
    reader = csv.reader(csvfile)
    for start, end, speaker in reader:
        if speaker == "SPEAKER_01":
            start = float(start) * 1000 - 500
            if start < 0:
                start = 0
            end = float(end) * 1000
            print(start, end, speaker)
            segments += full_audio[start:end]

segments.export("lex-367-sam-altman-sample-sa-only.wav", format="wav")
