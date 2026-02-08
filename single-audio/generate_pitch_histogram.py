# generate_pitch_histogram.py
# Python-only pitch histogram (no Praat)

import numpy as np
import librosa
import pickle
from matplotlib import pyplot as plt
import os

# ----------------------------
# Pitch extraction (Python-only)
# ----------------------------
def extract_pitch_python(wavfile, pitchfile, hop=0.01):
    """
    Extract pitch (f0) from WAV file using librosa.pyin
    Saves pitch file with time and pitch values
    """
    y, sr = librosa.load(wavfile, sr=None)
    hop_length = int(hop * sr)

    f0, voiced_flag, voiced_probs = librosa.pyin(
        y,
        fmin=librosa.note_to_hz("C2"),
        fmax=librosa.note_to_hz("C6"),
        sr=sr,
        hop_length=hop_length
    )

    times = librosa.frames_to_time(np.arange(len(f0)), sr=sr, hop_length=hop_length)

    # save pitch to file
    with open(pitchfile, "w") as f:
        for t, p in zip(times, f0):
            if p is None or np.isnan(p):
                f.write(f"{t} undefined\n")
            else:
                f.write(f"{t} {p}\n")


# ----------------------------
# Helper functions
# ----------------------------
def extract_time_pitch(file):
    """
    Read pitch file and return a numpy array of [time, pitch]
    Skips undefined frames
    """
    cols = []
    with open(file, "r") as f:
        for line in f:
            t, p = line.strip().split()
            try:
                pitch_val = float(p)
                cols.append([float(t), pitch_val])
            except ValueError:
                continue  # skip undefined
    return np.array(cols)


def PitchMedianSubtraction(time_pitch):
    """
    Subtract median pitch in cents to center around zero
    """
    median = np.median(time_pitch[:, 1])
    return np.column_stack((time_pitch[:, 0], time_pitch[:, 1] - median))


def GridMap(time_pitch):
    """
    Map pitch to ±6 semitones range
    """
    pitch_new = []
    for elem in time_pitch[:, 1]:
        if elem > 6:
            elem = np.mod(elem, 6) - 6
        elif elem < -6:
            elem = np.mod(elem, 6) + 6
        pitch_new.append(elem)
    return pitch_new


def GetFinerNoteHistogram(griddedpitch):
    """
    Create 120-bin histogram of pitch (10-cent bins)
    """
    notes = [0] * 120
    for elem in griddedpitch:
        count = 0
        for ind in np.arange(-6, 5.5, 0.1):
            if ind <= elem < ind + 0.1:
                notes[count] += 1
            count += 1
    return notes


def plotHistogram(notes):
    """
    Plot normalized 120-bin pitch histogram
    """
    notes = np.array(notes)
    notes = notes / np.trapz(notes)
    plt.figure(figsize=(10, 4))
    plt.bar(range(len(notes)), notes, width=1.0)
    plt.xlabel("Pitch (10-cent bins)")
    plt.ylabel("Normalized frame count")
    plt.title("Pitch Histogram")
    plt.show()


def CreateNoteHistogram(pitchfile):
    """
    Compute 120-bin pitch histogram from pitch file
    """
    time_pitch = extract_time_pitch(pitchfile)

    if time_pitch.size == 0:
        raise ValueError("No valid pitch frames found in file.")

    # Convert Hz -> cents
    pitch_hz = time_pitch[:, 1]
    median_hz = np.median(pitch_hz)
    if median_hz == 0:
        raise ValueError("Median pitch is zero. Check your audio or pitch extraction.")

    pitch_cents = 1200 * np.log2(pitch_hz / median_hz)
    time_pitch[:, 1] = pitch_cents

    # Median subtraction + grid mapping
    time_pitch = PitchMedianSubtraction(time_pitch)
    griddedpitch = GridMap(time_pitch)

    # Generate 120-bin histogram
    notes = GetFinerNoteHistogram(griddedpitch)
    return notes


# ----------------------------
# Main
# ----------------------------
if __name__ == "__main__":

    print("Generating pitch histogram...")
    # Paths
    base_path = r"D:\Codes\DL for singing evaluation\single-audio"
    wavfile = os.path.join(base_path, "vocals.wav")
    pitchfile = r"D:\Codes\DL for singing evaluation\single-audio\vocals_pitch.txt"
    print("pitch file:")
    print(pitchfile)
    histfile = os.path.join(base_path, "vocals_histogram.pkl")

    hop = 0.01  # 10ms hop

    # Check WAV file exists
    if not os.path.exists(wavfile):
        raise FileNotFoundError(f"{wavfile} not found")

    # 1️⃣ Extract pitch (Python-only)
    extract_pitch_python(wavfile, pitchfile, hop)

    # 2️⃣ Create histogram
    notes = CreateNoteHistogram(pitchfile)

    # 3️⃣ Save histogram
    with open(histfile, "wb") as f:
        pickle.dump(notes, f)

    print(f"Pitch histogram saved to {histfile}")

    # 4️⃣ Optional: plot histogram
    plotHistogram(notes)
