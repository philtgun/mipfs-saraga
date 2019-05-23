import os

import essentia.standard as ess
import numpy as np
import scipy
from scipy.io import wavfile
import commons
import config

def create_folder(path):
    if not os.path.exists(path):
        os.umask(0)  # To mask the permission restrictions on new files/directories being create
        os.makedirs(path, 0o755)  # setting permissions for the folder

output_dir = os.path.join(config.PREPROCESS_DIR,'samples')
tradition = 'carnatic'
file_list = commons.get_track_list(tradition)
total_phrases = 0
for filename in file_list:
    try:
        audio, metadata, pitch_contour_indices = commons.load_pitch_segments(tradition, filename)
    except (ValueError, OSError):
        continue

    try:
        raga = metadata['raaga'][0]['common_name']
    except IndexError:
        continue

    #len(np.where(pce - pcs > 1.5)[0])
    raga_dir = os.path.join(output_dir, raga)
    create_folder(raga_dir)

    (pitch_contour_start,pitch_contour_end)=(pitch_contour_indices[0],pitch_contour_indices[1])
    #filter indices based on length (only select segments > 1.5s)
    filtered_indices=np.where(pitch_contour_end - pitch_contour_start > config.THRESHOLD_PC_LENGTH)[0]
    filtered_pcs=pitch_contour_start[filtered_indices]
    filtered_pce = pitch_contour_end[filtered_indices]
    fs=config.SAMPLING_RATE

    for idx in range(len(filtered_indices)):
        start_ind = int(fs * filtered_pcs[idx])
        stop_ind = int(fs * filtered_pce[idx])
        melodic_segment_path = os.path.join(raga_dir, '{}-{:03}.wav'.format(filename, idx))
        scipy.io.wavfile.write(melodic_segment_path, config.SAMPLING_RATE, audio[start_ind:stop_ind])
        #ess.MonoWriter(filename=melodic_segment_path, format='mp3')(audio[start_ind:stop_ind])

    print("Finished segmenting "+filename+"!!")
