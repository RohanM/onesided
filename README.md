## Install ffmpeg

```shell
brew install ffmpeg
```

## Download audio from YouTube

```shell
poetry install
poetry shell

yt-dlp -xv --audio-format wav  -o download.wav -- https://www.youtube.com/watch?v=xxxx
```

## Process

```shell
python diarize.py
python remix.py
```
