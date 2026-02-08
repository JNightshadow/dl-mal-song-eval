import librosa
import soundfile as sf
import numpy as np
import os

# Input file
audio_path = r"D:\Codes\Final Year\Malayalam Dataset\clip0002.wav"
y, sr = librosa.load(audio_path, sr=16000)

# Output folder
output_folder = r"D:\Codes\Final Year\Malayalam Dataset\augmented_bad_strong"
os.makedirs(output_folder, exist_ok=True)

# 1️⃣ Strong random detune (±3 to 5 semitones, sudden jumps)
def strong_detune(y, sr):
    y_out = y.copy()
    num_segments = np.random.randint(5, 12)
    seg_len = len(y) // num_segments
    detuned = []
    for i in range(num_segments):
        start = i * seg_len
        end = (i+1) * seg_len if i < num_segments-1 else len(y)
        chunk = y_out[start:end]
        n_steps = np.random.uniform(-5, 5)  # semitones
        detuned.append(librosa.effects.pitch_shift(y=chunk, sr=sr, n_steps=n_steps))
    return np.concatenate(detuned)

# 2️⃣ Extreme timing jitter
def extreme_timing_jitter(y):
    num_chunks = np.random.randint(5, 12)
    chunk_len = len(y) // num_chunks
    augmented = []
    for i in range(num_chunks):
        start = i * chunk_len
        end = (i+1) * chunk_len if i < num_chunks-1 else len(y)
        chunk = y[start:end]
        rate = np.random.uniform(0.8, 1.2)  # 20% faster/slower
        chunk_stretched = librosa.effects.time_stretch(y=chunk, rate=rate)
        augmented.append(chunk_stretched)
    return np.concatenate(augmented)

# 3️⃣ Exaggerated vibrato + micro pitch wobbles
def strong_vibrato(y, sr):
    t = np.arange(len(y)) / sr
    mod_freq = np.random.uniform(2, 6)   # faster vibrato
    mod_amp = np.random.uniform(0.02, 0.05)  # larger amplitude
    modulation = 1 + mod_amp * np.sin(2 * np.pi * mod_freq * t + np.random.rand()*2*np.pi)
    return y * modulation

# 4️⃣ Random micro-pauses
def micro_pauses(y, sr):
    y_out = y.copy()
    num_pauses = np.random.randint(5, 10)
    for _ in range(num_pauses):
        start = np.random.randint(0, len(y_out)-2000)
        end = start + np.random.randint(500, 2000)
        y_out[start:end] = 0
    return y_out

# Generate 3 strong bad singing samples
for i in range(3):
    y_bad = y.copy()
    y_bad = strong_detune(y_bad, sr)
    y_bad = extreme_timing_jitter(y_bad)
    y_bad = strong_vibrato(y_bad, sr)
    y_bad = micro_pauses(y_bad, sr)

    out_path = os.path.join(output_folder, f"clip0002_bad_strong_{i+1}.wav")
    sf.write(out_path, y_bad, sr)
    print(f"Saved: {out_path}")

print("✅ Done generating strong poor singing samples!")
