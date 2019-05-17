import os
import essentia.standard as ess
import numpy as np
import json
import IPython

DATA_PATH = 'data'
SAMPLING_RATE = 44100


def get_track_list_from_directory(tradition):
    """Helper function to get the list of all tracks from data folders"""
    files_all = os.listdir(os.path.join(DATA_PATH, tradition))
    [print(filename.replace('.mp3', '')) for filename in sorted(files_all) if filename.endswith('.mp3')]


def load_track(tradition, name, fs=SAMPLING_RATE):
    """Loads audio, metadata and melodic phrases"""
    path = os.path.join(DATA_PATH, tradition, name)
    audio = ess.MonoLoader(filename=path + '.mp3', sampleRate=fs)()
    phrases = np.loadtxt(path + '.mphrases-manual.txt',
                         dtype={'names': ('start', 'dummy', 'duration', 'phrase'),
                                'formats': ('f4', 'i4', 'f4', np.str)})
    with open(path + '.json') as fp:
        metadata = json.load(fp)
    return audio, metadata, phrases


def get_track_list(tradition):
    path = os.path.join(DATA_PATH, tradition + '.txt')
    return np.genfromtxt(path, dtype=np.str, delimiter=256)


def collate_phrases(phrases, fs=SAMPLING_RATE):
    """Collect all occurrences of each phrase and transform secs to samples"""
    phrases_dict = {}
    for (start_sec, dummy, duration_sec, phrase) in phrases:
        start_ind = int(fs * start_sec)
        stop_ind = start_ind + int(fs * duration_sec)

        if phrase not in phrases_dict.keys():
            phrases_dict[phrase] = []
        phrases_dict[phrase].append([start_ind, stop_ind])
    return phrases_dict


def display_audio(audio):
    IPython.display.display(IPython.display.Audio(audio, rate=SAMPLING_RATE))


def extract_pitch(audio):
    audio_eqd = ess.EqualLoudness()(audio)
    pitch, confidence = ess.PitchMelodia()(audio_eqd)
    pitch[pitch == 0] = np.nan
    return pitch, confidence
