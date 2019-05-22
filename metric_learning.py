import os

import essentia.standard as ess
import numpy as np

import commons
import config


output_dir = os.path.join(config.DATA_PATH, config.PREPROCESS_DIR)
tradition = 'carnatic'
file_list = commons.get_track_list(tradition)
total_phrases = 0
for filename in file_list:
    try:
        audio, metadata, phrases = commons.load_track(tradition, filename)
    except (ValueError, OSError):
        continue

    try:
        raga = metadata['raaga'][0]['common_name']
    except IndexError:
        continue

    raga_dir = os.path.join(output_dir, raga)
    os.makedirs(raga_dir, exist_ok=True)

    try:
        length = len(phrases)
    except TypeError:
        length = 1
        phrases = np.array([phrases])

    print(phrases)

    if len(phrases) > 0:
        collated_phrases = commons.collate_phrases(phrases)
        for phrase_annotation, phrases in collated_phrases.items():
            for i, indices in enumerate(phrases):
                melodic_segment_dir = os.path.join(raga_dir, phrase_annotation.decode())
                os.makedirs(melodic_segment_dir, exist_ok=True)
                melodic_segment_path = os.path.join(melodic_segment_dir, '{}-{:02}.mp3'.format(filename, i))
                ess.MonoWriter(filename=melodic_segment_path, format='mp3')(audio[indices[0]:indices[1]])
        total_phrases += len(phrases)
        print(filename, len(phrases))

print(total_phrases)
