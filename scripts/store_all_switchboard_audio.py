#python store_all_switchboard_train_audio.py --output_pickle_file=/data0/project/microtuning/misc/swb_train_audios.pkl --switchboard_audio_path=/data/corpora/switchboard-1/97S62/ --switchboard_transcriptions_path=/data/corpora/switchboard-1/swb_ms98_transcriptions
import sys, time, librosa, os, argparse, pickle
sys.path.append('/mnt/data0/jrgillick/projects/audio-feature-learning/')
from tqdm import tqdm
import dataset_utils, audio_utils, data_loaders
import pandas as pd
from tqdm import tqdm
from joblib import Parallel, delayed

parser = argparse.ArgumentParser()

##################################################################
######################  Get input arguments ######################
##################################################################

# Path to store the parsed label times and inputs for Switchboard
#parser.add_argument('--output_pickle_file', type=str, required=True)
# Path to the root folder containing the switchboard audio
#parser.add_argument('--switchboard_audio_path', type=str, required=True)
# Path to the root folder containing the switchboard transcriptions
#parser.add_argument('--switchboard_transcriptions_path', type=str, required=True)

#args = parser.parse_args()

#output_pickle_file = '/data0/project/microtuning/misc/swb_train_audios.pkl'#args.output_pickle_file

a_root = '/mnt/data0/jrgillick/projects/laughter-detection/data/switchboard/switchboard-1/97S62/' #args.switchboard_audio_path
t_root = '/mnt/data0/jrgillick/projects/laughter-detection/data/switchboard/switchboard-1/swb_ms98_transcriptions/'#args.switchboard_transcriptions_path


all_audio_files = librosa.util.find_files(a_root,ext='sph')
train_folders, val_folders, test_folders = dataset_utils.get_train_val_test_folders(t_root)

train_transcription_files_A, train_audio_files = dataset_utils.get_audio_files_from_transcription_files(
    dataset_utils.get_all_transcriptions_files(train_folders, 'A'), all_audio_files)
train_transcription_files_B, _ = dataset_utils.get_audio_files_from_transcription_files(
    dataset_utils.get_all_transcriptions_files(train_folders, 'B'), all_audio_files)

val_transcription_files_A, val_audio_files = dataset_utils.get_audio_files_from_transcription_files(
    dataset_utils.get_all_transcriptions_files(val_folders, 'A'), all_audio_files)
val_transcription_files_B, _ = dataset_utils.get_audio_files_from_transcription_files(
    dataset_utils.get_all_transcriptions_files(val_folders, 'B'), all_audio_files)

test_transcription_files_A, test_audio_files = dataset_utils.get_audio_files_from_transcription_files(
    dataset_utils.get_all_transcriptions_files(test_folders, 'A'), all_audio_files)
test_transcription_files_B, _ = dataset_utils.get_audio_files_from_transcription_files(
    dataset_utils.get_all_transcriptions_files(test_folders, 'B'), all_audio_files)

h = {}
train_y = audio_utils.parallel_load_audio_batch(train_audio_files, n_processes=8, sr=8000)
assert(len(train_y) == len(train_audio_files))
for i in range(len(train_audio_files)):
    f = train_audio_files[i]
    y = train_y[i]
    h[f] = y

with open("/mnt/data0/jrgillick/projects/laughter-detection/data/switchboard/train/swb_train_audios.pkl", "wb") as f:
    pickle.dump(h, f)
    
    
h = {}
val_y = audio_utils.parallel_load_audio_batch(val_audio_files, n_processes=8, sr=8000)
assert(len(val_y) == len(val_audio_files))
for i in range(len(val_audio_files)):
    f = val_audio_files[i]
    y = val_y[i]
    h[f] = y

with open("/mnt/data0/jrgillick/projects/laughter-detection/data/switchboard/val/swb_val_audios.pkl", "wb") as f:
    pickle.dump(h, f)

    
h = {}
test_y = audio_utils.parallel_load_audio_batch(test_audio_files, n_processes=8, sr=8000)
assert(len(test_y) == len(test_audio_files))
for i in range(len(test_audio_files)):
    f = test_audio_files[i]
    y = test_y[i]
    h[f] = y

with open("/mnt/data0/jrgillick/projects/laughter-detection/data/switchboard/test/swb_test_audios.pkl", "wb") as f:
    pickle.dump(h, f)