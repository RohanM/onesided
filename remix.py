import argparse
import csv
from pydub import AudioSegment

parser = argparse.ArgumentParser(
    description="Remix a WAV file based on a diarisation CSV file"
)
parser.add_argument("--ds", help="CSV file with diarisation", required=True)
parser.add_argument("--input", help="Input WAV file", required=True)
parser.add_argument(
    "--include-speakers",
    nargs="+",
    help="Speakers to include, comma-separated",
)
parser.add_argument(
    "--exclude-speakers",
    nargs="+",
    help="Speakers to exclude, comma-separated",
)
args = parser.parse_args()

output_filename = args.input.replace(".wav", ".onesided.wav")


def main():
    full_audio = AudioSegment.from_wav(args.input)

    with open(args.ds) as csvfile:
        reader = csv.reader(csvfile)
        speakers = get_speakers(reader, args.include_speakers, args.exclude_speakers)
        csvfile.seek(0)

        segments = build_audio(reader, speakers, full_audio)
        segments.export(output_filename, format="wav")


def build_audio(csv_reader, speakers, full_audio):
    segments = AudioSegment.empty()

    for start, end, speaker in csv_reader:
        if speaker in speakers:
            start = float(start) * 1000
            end = float(end) * 1000

            # Fix clipping of first sample
            if start < 500:
                start = 0

            print(f"{start / float(len(full_audio))*100:.0f}%")
            segments += full_audio[start:end]

    return segments


def get_speakers(csv_reader, include_speakers, exclude_speakers):
    speakers = set()
    for start, end, speaker in csv_reader:
        speakers.add(speaker)
    if include_speakers:
        speakers = speakers.intersection(parse_speakers(include_speakers))
    if exclude_speakers:
        speakers = speakers.difference(parse_speakers(exclude_speakers))
    return speakers


def parse_speakers(speakers):
    return set([f"SPEAKER_{int(s):02d}" for s in ",".join(speakers).split(",")])


main()
