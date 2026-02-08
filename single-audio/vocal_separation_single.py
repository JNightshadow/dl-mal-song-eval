import torch
import numpy as np
import librosa
import soundfile as sf
from demucs import pretrained
from demucs.apply import apply_model

audio_path = r"D:\Codes\Final Year\YTDataset\Good\00007.wav"

# Load audio with librosa
y, sr = librosa.load(audio_path, sr=44100, mono=False)

# Ensure correct shape (2, samples)
if y.ndim == 1:
    y = np.vstack([y, y])    # duplicate mono to stereo
else:
    if y.shape[0] == 1:
        y = np.vstack([y, y])

waveform = torch.tensor(y, dtype=torch.float32)

# Load Demucs model
model = pretrained.get_model('htdemucs')

# Apply model (no sr argument)
with torch.no_grad():
    sources = apply_model(model, waveform.unsqueeze(0))[0]

# Extract vocals
vocal_idx = model.sources.index('vocals')
vocals = sources[vocal_idx]

# Save output
sf.write("vocals.wav", vocals.cpu().numpy().T, sr)
