import IPython
import essentia.standard as ess
import numpy as np
import os
import json
from copy import deepcopy

import config


def display_audio(audio):
    IPython.display.display(IPython.display.Audio(audio, rate=config.SAMPLING_RATE))


def extract_pitch(audio):
    audio_eqd = ess.EqualLoudness()(audio)
    pitch, confidence = ess.PitchMelodia(hopSize=config.HOP_SIZE)(audio_eqd)
    return pitch, confidence


def get_plot_pitch(pitch):
    pitch_plot = deepcopy(pitch)
    pitch_plot[pitch == 0] = np.nan
    return pitch_plot


def get_track_list_from_directory(tradition):
    """Helper function to get the list of all tracks from data folders"""
    files_all = os.listdir(os.path.join(config.DATA_PATH, tradition))
    [print(filename.replace('.mp3', '')) for filename in sorted(files_all) if filename.endswith('.mp3')]


def load_track(tradition, name, fs=config.SAMPLING_RATE):
    """Loads audio, metadata and melodic phrases"""
    path = os.path.join(config.DATA_PATH, tradition, name)
    audio = ess.MonoLoader(filename=path + '.mp3', sampleRate=fs)()
    phrases = np.loadtxt(path + '.mphrases-manual.txt',
                         dtype={'names': ('start', 'dummy', 'duration', 'phrase'),
                                'formats': ('f4', 'i4', 'f4', 'S32')})
    with open(path + '.json') as fp:
        metadata = json.load(fp)
    return audio, metadata, phrases

def get_pitch_contour_indices(path):
    """Gets the timestamps of detected pitch contours"""
    pitch_data = np.loadtxt(path + '.pitch.txt')
    pitch_data_marker=pitch_data[:,1]
    pitch_data_marker[np.where(pitch_data_marker!=0)]=1
    pitch_contour_trans=np.diff(pitch_data_marker)
    pitch_contour_start=np.where(pitch_contour_trans==1)[0]+1
    pitch_contour_end=np.where(pitch_contour_trans==-1)[0]
    return [pitch_data[pitch_contour_start,0],pitch_data[pitch_contour_end,0]]

def load_pitch_segments(tradition, name, fs=config.SAMPLING_RATE):
    """Loads audio, metadata and pitch contours"""
    path = os.path.join(config.DATA_PATH, tradition, name)
    audio = ess.MonoLoader(filename=path + '.mp3', sampleRate=fs)()
    pitch_contour_indices = get_pitch_contour_indices(path)
    with open(path + '.json') as fp:
        metadata = json.load(fp)
    return audio, metadata, pitch_contour_indices

def get_track_list(tradition):
    path = os.path.join(config.DATA_PATH, tradition + '.txt')
    return np.genfromtxt(path, dtype=np.str, delimiter=256)


def collate_phrases(phrases, fs=config.SAMPLING_RATE):
    """Collect all occurrences of each phrase and transform secs to samples"""
    phrases_dict = {}
    for (start_sec, dummy, duration_sec, phrase) in phrases:
        start_ind = int(fs * start_sec)
        stop_ind = start_ind + int(fs * duration_sec)

        if phrase not in phrases_dict.keys():
            phrases_dict[phrase] = []
        phrases_dict[phrase].append([start_ind, stop_ind])
    return phrases_dict
