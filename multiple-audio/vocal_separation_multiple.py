import os
import torch
import librosa
import numpy as np
import soundfile as sf
from demucs import pretrained
from demucs.apply import apply_model

BASE_IN = r"D:\Codes\DL for singing evaluation\covers_dataset"
BASE_OUT = r"D:\Codes\DL for singing evaluation\processed\vocals"

os.makedirs(BASE_OUT, exist_ok=True)

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
MAX_DURATION = 300.0  # seconds (3 minutes)

# Load Demucs ONCE
model = pretrained.get_model("htdemucs")
model.to(DEVICE)
model.eval()

for song in os.listdir(BASE_IN):
    song_in = os.path.join(BASE_IN, song)
    song_out = os.path.join(BASE_OUT, song)

    if not os.path.isdir(song_in):
        continue

    os.makedirs(song_out, exist_ok=True)
    print(f"\nProcessing song: {song}")

    for fname in os.listdir(song_in):
        if not fname.lower().endswith(".wav"):
            continue

        in_path = os.path.join(song_in, fname)
        out_path = os.path.join(song_out, fname)

        try:
            # ---- duration check (FAST) ----
            duration = librosa.get_duration(path=in_path)
            if duration > MAX_DURATION:
                print(f"  ⏭ Skipped (>5 min): {fname}")
                continue

            # ---- load audio ----
            y, sr = librosa.load(in_path, sr=44100, mono=False)

            if y.ndim == 1 or y.shape[0] == 1:
                y = np.vstack([y, y])

            waveform = torch.tensor(y, dtype=torch.float32).to(DEVICE)

            # ---- separate ----
            with torch.no_grad():
                sources = apply_model(model, waveform.unsqueeze(0))[0]

            vocal_idx = model.sources.index("vocals")
            vocals = sources[vocal_idx].cpu().numpy().T

            # ---- save ----
            sf.write(out_path, vocals, sr)
            print(f"  ✓ {fname}")

        except Exception as e:
            print(f"  ✗ Failed: {fname} | {e}")
