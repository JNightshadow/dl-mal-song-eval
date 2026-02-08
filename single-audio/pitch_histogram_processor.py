import scipy.io.wavfile as wav
import numpy as np
from matplotlib import pylab as plt
import pickle
import os
import csv
from scipy.spatial.distance import euclidean
import scipy.stats


def PitchMedianSubtraction(time_pitch):
    time = time_pitch[:, 0]
    pitch = time_pitch[:, 1]
    median = np.median(pitch)
    pitch_new = pitch - median
    time_pitch_mediansubtracted = np.hstack(
        [time[np.newaxis].T, pitch_new[np.newaxis].T])
    return time_pitch_mediansubtracted


def InitialFinalSilenceRemoved(sig):
    energy_thresh = 0.01
    window = 512
    hop = window / 2
    energy = []
    i = 0
    energy_index = []
    while i < (len(sig) - window):
        chunk = sig[int(i):int(i + window)][np.newaxis]
        energy.append(chunk.dot(chunk.T)[0][0])
        energy_index.append(i)
        i = i + hop

    energy = np.array(energy)
    significant_indices = np.where(energy > energy_thresh)[0]
    if significant_indices[0] == 0:
        start_point_sample = 0
    else:
        start_point_sample = (significant_indices[0] - 1) * hop
    if significant_indices[-1] == len(energy) - 1:
        end_point_sample = len(energy) * hop
    else:
        end_point_sample = (significant_indices[-1] + 1) * hop
    new_sig = sig[int(start_point_sample):int(end_point_sample + 1)]
    return new_sig


def extract_time_pitch(file):
    f = open(file, 'r')
    obj = csv.reader(f, delimiter=' ')
    cols = []
    for row in obj:
        if len(row) < 2:
            break
        if np.size(cols) == 0:
            cols = [
                -100.0 if 'undefined' in elem else float(elem) for elem in row
            ]
        else:
            cols = np.vstack((cols, [
                -100.0 if 'undefined' in elem else float(elem) for elem in row
            ]))
    cols_modified = []
    for row in cols:
        if row[1] == -100.0:
            continue
        if np.size(cols_modified) == 0:
            cols_modified = row[:]
        else:
            cols_modified = np.vstack((cols_modified, row))
    return cols_modified


def GridMap(time_pitch):
    pitch = time_pitch[:, 1]
    pitch_new = []
    for elem in pitch:
        if elem > 6:
            elem = np.mod(elem, 6) - 6
        elif elem < -6:
            elem = np.mod(elem, 6) + 6
        pitch_new.append(elem)
    return pitch_new


def GetFinerNoteHistogram(griddedpitch):
    notes = [0] * 120
    for elem in griddedpitch:
        count = 0
        for ind in np.arange(-6, 5.5, 0.1):
            left = ind
            right = ind + 0.1

            if elem >= left and elem < right:
                notes[count] = notes[count] + 1
            count = count + 1
        count = 0
        for ind in np.arange(6, 5.5, -0.1):
            right = ind
            left = ind - 0.1

            if elem >= left and elem < right:
                notes[count] = notes[count] + 1
            count = count + 1
    return notes


def plotHistogram(notes):
    plt.figure()
    plt.bar(range(len(notes)), notes / np.trapz(notes))
    plt.ylim(ymin=0.000)
    plt.ylim(ymax=0.025)
    plt.xlabel('Pitch x 10 cents', fontsize=15)
    plt.ylabel('Normalized number of frames', fontsize=15)
    plt.show()


def CreateNoteHistogram(original_pitch_file):
    original_time_pitch = extract_time_pitch(original_pitch_file)
    lpf_time_pitch = original_time_pitch
    original_time_pitchmediansubtracted = PitchMedianSubtraction(
        lpf_time_pitch)
    griddedpitch = GridMap(original_time_pitchmediansubtracted)
    notes = GetFinerNoteHistogram(griddedpitch)
    return notes


if __name__ == "__main__":
    pitch_file = "path_to_pitch_file.txt"
    histogram = CreateNoteHistogram(pitch_file)
    plotHistogram(histogram)