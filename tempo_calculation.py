import os
import pretty_midi
from tqdm import tqdm


def get_standard_bpm_set():
    bpm_set = set()
    for i in range(0, 10):
        for j in range(0, 4):
            standard_bpm1 = 2**i * 5**j
            standard_bpm2 = 3 * 2**i * 5**j
            if standard_bpm1 <= 400:
                bpm_set.add(standard_bpm1)
            if standard_bpm2 <= 400:
                bpm_set.add(standard_bpm2)
    return bpm_set


def find_closest_element(target, collection):
    closest_element = None
    min_difference = float('inf')  # 初始设为正无穷大

    for element in collection:
        difference = abs(target - element)

        if difference < min_difference:
            min_difference = difference
            closest_element = element

    return closest_element


source_dir = "./tgt_dataset/"
acc = 0
total_num = 0


standard_bpm_set = get_standard_bpm_set()

if __name__ == "main":
    print("tempo_calculation.py started!")
    for _, _, filenames in os.walk(source_dir):
        for filename in tqdm(filenames, desc="Processing", unit="midi"):
            total_num = total_num + 1
            midi_data = pretty_midi.PrettyMIDI(f"{source_dir}{filename}")
            tempo = midi_data.get_tempo_changes()[1][0]
            standard_tempo = find_closest_element(tempo, standard_bpm_set)
            acc = acc + abs(tempo - standard_tempo) / tempo

    print(f"平均速度偏移误差：{round(acc*100/total_num,2)}%")
