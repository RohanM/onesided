from pyannote.audio import Pipeline

pipeline = Pipeline.from_pretrained(
    "pyannote/speaker-diarization",
    use_auth_token="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",
)

DEMO_FILE = {"uri": "xxx", "audio": "lex-367-sam-altman-sample.wav"}
dz = pipeline(DEMO_FILE)

with open("dz.csv", "w") as f:
    for turn, _, speaker in dz.itertracks(yield_label=True):
        f.write(f"{turn.start},{turn.end},{speaker}\n")
