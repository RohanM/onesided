import sys
from pyannote.audio import Pipeline

print("Loading pipeline...")
pipeline = Pipeline.from_pretrained(
    "pyannote/speaker-diarization",
    use_auth_token="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",
)

print(f"Opening audio file {sys.argv[1]}...")
file = {"uri": "xxx", "audio": sys.argv[1]}
dz = pipeline(file)

print("Reading diarization...")
with open("dz.csv", "w") as f:
    for turn, _, speaker in dz.itertracks(yield_label=True):
        print(f"{turn.start},{turn.end},{speaker}")
        f.write(f"{turn.start},{turn.end},{speaker}\n")

