from filter import standard_midi_filter
from tqdm import tqdm
import os
import shutil
source_dir = './tgt_dataset_v2/'
tgt_dir = './tgt_dataset_v8/'

i = 0
print("dataset_clean.py started!")
for _, _, filenames in os.walk(source_dir):
    for filename in tqdm(filenames, desc="Processing", unit="midi"):
        file_path = f"{source_dir}{filename}"
        if standard_midi_filter(file_path) == 4:
            shutil.copy(file_path, f"{tgt_dir}{i}.mid")
            i = i + 1
print(i)