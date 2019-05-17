# -*- coding: utf-8 -*-

from compmusic import dunya as dn
from compmusic.dunya import hindustani as hin
from compmusic.dunya import carnatic as car
from compmusic.dunya import docserver as ds
import collections
import os, json

myDunyaToken = ''
dn.set_token(myDunyaToken)

# Path to the folder where all files will be downloaded to
rootFolder = ''

# MBID of the Dunya Hindustani CC collection (= Hindustani Saraga)
hinCC = '6adc54c6-6605-4e57-8230-b85f1de5be2b'

# MBID of the Dunya Carnatic CC collection (= Carnatic Saraga)
carCC = 'a163c8f2-b75f-4655-86be-1504ea2944c2'

# Required sourcefiles
sf = []

# Required derivedfiles
ann = [{'type':'mphrases-manual', 'subtype':None},
       {'type':'ctonic', 'subtype':'tonic'},
       {'type':'pitch', 'subtype':'pitch'}]


###############################################################################
# Hindustani collection
print('Retrieving information from the Dunya Hindustani CC collection')

hin.set_collections([hinCC])
recordings = hin.get_recordings(recording_detail=True)

print('{} recordings retrieved from the Dunya Hindustani CC collection'.format(len(recordings)))

usableFiles = 0

# Create a folder for downloading all the hindustani recordings
hindustaniFolder = os.path.join(rootFolder, 'Hindustani')
os.mkdir(hindustaniFolder)

for recording in recordings:
    mbid = recording['mbid']
    artist = recording['album_artists'][0]['name']
    # Make sure that the recording is annotated with the raga
    if len(recording['raags']) == 0:
        continue
    raga = recording['raags'][0]['common_name']
    talas = [tala['common_name'] for tala in recording['taals']]
    # Make sure that the recording is annotated with the talas
    if len(talas) == 0:
        continue
    forms = [form['common_name'] for form in recording['forms']]
    # Make sure that the recording is annotated with the forms
    if len(forms) == 0:
        continue
    
    # Get the related annotation files
    files = ds.document(mbid)
    sourceFiles = files['sourcefiles']
    derivedFiles = files['derivedfiles']
    
    # Check that the recording meet all the required criteria
    if ('Khayal' in forms and
        'mphrases-manual' in sourceFiles and
        'ctonic' in derivedFiles and
        'pitch' in derivedFiles):
        
        # Create a folder for the recording
        name = '{}_{}_'.format(mbid, raga)
        for tala in talas:
            name += tala
        name += '_' + artist
        recordingFolder = os.path.join(hindustaniFolder, name)
        os.mkdir(recordingFolder)
        
        # Download audio file
        fileName = hin.download_mp3(mbid, recordingFolder)
        
        # Download annotation files
        for a in ann:
            content = ds.file_for_document(mbid, a['type'], a['subtype'])
            annName = '{}_{}.txt'.format(fileName[:-4], a['type'])
            with open(os.path.join(recordingFolder, annName), 'w') as f:
                f.write(content.decode())
        print('  Files for "{}" downloaded'.format(fileName[:-4]))
        
        usableFiles += 1

print('{} recordings met the required criteria'.format(usableFiles))
print('All files for the Hindustani dataset downloaded!\n')


###############################################################################
# Carnatic collection
print('Retrieving information from the Dunya Carnatic CC collection')

car.set_collections([carCC])
recordings = car.get_recordings(recording_detail=True)

print('{} recordings retrieved from the Dunya Carnatic CC collection'.format(len(recordings)))

usableFiles = 0

# Create a folder for downloading all the hindustani recordings
carnaticFolder = os.path.join(rootFolder, 'Carnatic')
os.mkdir(carnaticFolder)

for recording in recordings:
    mbid = recording['mbid']
    artist = recording['album_artists'][0]['name']
    # Make sure that the recording is annotated with the raga
    if len(recording['raaga']) == 0:
        continue
    raga = recording['raaga'][0]['common_name']
    talas = [tala['common_name'] for tala in recording['taala']]
    # Make sure that the recording is annotated with the talas
    if len(talas) == 0:
        continue
    forms = [form['name'] for form in recording['form']]
    # Make sure that the recording is annotated with the forms
    if len(forms) == 0:
        continue
    
    # Get the related annotation files
    files = ds.document(mbid)
    sourceFiles = files['sourcefiles']
    derivedFiles = files['derivedfiles']
    
    # Check that the recording meet all the required criteria
    if ('Kriti' in forms and
        'mphrases-manual' in sourceFiles and
        'ctonic' in derivedFiles and
        'pitch' in derivedFiles):
        
        # Create a folder for the recording
        name = '{}_{}_'.format(mbid, raga)
        for tala in talas:
            name += tala
        name += '_' + artist
        recordingFolder = os.path.join(carnaticFolder, name)
        os.mkdir(recordingFolder)
        
        # Download audio file
        fileName = car.download_mp3(mbid, recordingFolder)
        
        # Download annotation files
        for a in ann:
            content = ds.file_for_document(mbid, a['type'], a['subtype'])
            annName = '{}_{}.txt'.format(fileName[:-4], a['type'])
            with open(os.path.join(recordingFolder, annName), 'w') as f:
                f.write(content.decode())
        print('  Files for "{}" downloaded'.format(fileName[:-4]))
        
        usableFiles += 1

print('{} recordings met the required criteria'.format(usableFiles))
print('All files for the Carnatic dataset downloaded!\n')