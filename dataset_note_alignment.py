from note_alignment import note_alignment_16
import os
from tqdm import tqdm
src_folder='./ultimate_dataset/'
tgt_folder='./ultimate_aligned_dataset_16/'

for _, _, filenames in os.walk(src_folder):
    for filename in tqdm(filenames, desc="Processing", unit="midi"):
        file_path = f"{src_folder}{filename}"
        midi_data=note_alignment_16(file_path)
        midi_data.write(f"{tgt_folder}{filename}")