import argparse
import csv
from pydub import AudioSegment

parser = argparse.ArgumentParser(
    description="Remix a WAV file based on a diarisation CSV file"
)
parser.add_argument("--ds", help="CSV file with diarisation", required=True)
parser.add_argument("--input", help="Input WAV file", required=True)
parser.add_argument(
    "--speakers",
    action="store_true",
    help="Generate audio with samples of all speakers",
)
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


def main():
    full_audio = AudioSegment.from_wav(args.input)

    with open(args.ds) as csvfile:
        reader = csv.reader(csvfile)
        speakers = get_speakers(reader, args.include_speakers, args.exclude_speakers)
        csvfile.seek(0)

        if not args.speakers:
            segments = build_audio(reader, speakers, full_audio)
            output_filename_suffix = ".onesided.wav"
        else:
            segments = build_speakers_sample(reader, speakers, full_audio)
            output_filename_suffix = ".speakers.wav"

        output_filename = args.input.replace(".wav", output_filename_suffix)
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


def build_speakers_sample(csv_reader, speakers, full_audio):
    segments = AudioSegment.empty()

    chime = AudioSegment.from_wav("audio/chime.wav")

    for tgt_speaker in sorted(speakers):
        for start, end, speaker in csv_reader:
            start = float(start) * 1000
            end = float(end) * 1000

            # Fix clipping of first sample
            if start < 500:
                start = 0

            if speaker == tgt_speaker and end - start > 1000:
                segments += chime
                segments += AudioSegment.from_wav(f"audio/num-{tgt_speaker[-2:]}.wav")

                segments += full_audio[start:end]
                break

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
