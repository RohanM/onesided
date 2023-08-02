import sys
from pyannote.audio import Pipeline

input_filename = sys.argv[1]
output_filename = input_filename.replace(".wav", ".ds.csv")

print("Loading pipeline...")
pipeline = Pipeline.from_pretrained(
    "pyannote/speaker-diarization",
    use_auth_token="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",
)

print(f"Opening audio file {input_filename}...")
ds = pipeline(input_filename)

print("Writing diarisation...")
with open(output_filename, "w") as f:
    for turn, _, speaker in ds.itertracks(yield_label=True):
        print(f"{turn.start},{turn.end},{speaker}")
        f.write(f"{turn.start},{turn.end},{speaker}\n")
