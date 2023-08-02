# One-sided

One-sided is a tool to process spoken audio (eg. podcasts) and selectively remove specific speakers. It's ideal for when you want to eliminate extraneous chatter, enabling
you to focus on the crux of an interview.

## Install

```shell
# Install ffmpeg
apt-get install ffmpeg # Ubuntu
brew install ffmpeg # MacOS

# Install python packages and open shell
poetry install
poetry shell
```

## Getting started

Download your podcast audio from YouTube:

```shell
yt-dlp -xv --audio-format wav --restrict-filenames -o "%(title)s.%(ext)s" -- https://www.youtube.com/watch?v=xxxx
```

Segment the audio by speaker, producing a CSV. This process is compute-intensive,
and performs best with a GPU:

```shell
python diarise.py my-podcast.wav

# outputs my-podcast.ds.csv
```

Produce sample audio to determine the identity of each speaker:

```shell
python remix.py --speakers --ds my-podcast.ds.csv --in my-podcast.wav
# outputs my-podcast.speakers.wav
```

Listen to the sample audio. This will consist of a segment for each speaker, separated by a chime.
Make note of which speakers you'd like to retain and/or remove.

Output the processed audio:

```shell
# Include only specified speakers
python remix.py --ds my-podcast.ds.csv --in my-podcast.wav --include-speakers=1,3

# Exclude some speakers, retain the others:
python remix.py --ds my-podcast.ds.csv --in my-podcast.wav --exclude-speakers=2,4

# Either will output my-podcast.onesided.wav
```

## Credits

- Spoken numbers by Amy Gedgaudas - https://freesound.org/people/tim.kahn/packs/4372/
