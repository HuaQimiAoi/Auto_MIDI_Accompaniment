from note_alignment import note_alignment_16
from tempo_adjustment import tempo_adjustment
import pretty_midi
import os
from tqdm import tqdm


def program_change(midiFile):
    midi_data = pretty_midi.PrettyMIDI(midiFile)
    instruments_count = len(midi_data.instruments)
    for i in range(instruments_count):
        # 鼓
        if midi_data.instruments[i].is_drum:
            midi_data.instruments[i].program = 0
            midi_data.instruments[i].name = "Drum_Track"
        # 原声钢琴
        elif midi_data.instruments[i].program >= 0 and midi_data.instruments[i].program <= 7:
            midi_data.instruments[i].program = 0
        # 尼龙吉他
        elif midi_data.instruments[i].program >= 24 and midi_data.instruments[i].program <= 25:
            midi_data.instruments[i].program = 24
        # 清音电吉他
        elif midi_data.instruments[i].program >= 26 and midi_data.instruments[i].program <= 28:
            midi_data.instruments[i].program = 27
        # 失真电吉他
        elif midi_data.instruments[i].program >= 29 and midi_data.instruments[i].program <= 31:
            midi_data.instruments[i].program = 30
        # 指弹电贝斯
        elif (midi_data.instruments[i].program >= 32 and midi_data.instruments[i].program <= 35) or (midi_data.instruments[i].program >= 38 and midi_data.instruments[i].program <= 39):
            midi_data.instruments[i].program = 33
        # slap电贝斯
        elif midi_data.instruments[i].program >= 36 and midi_data.instruments[i].program <= 37:
            midi_data.instruments[i].program = 36
    return midi_data


src_folder = "./ultimate_dataset_16_one_drum/"
tgt_folder = "./ultimate_dataset_16_one_drum_v2/"
for _, _, filenames in os.walk(src_folder):
    for filename in tqdm(filenames, desc="processing", unit="midi"):
        midi_data = program_change(f"{src_folder}{filename}")
        midi_data.write(f"{tgt_folder}{filename}")


src_folder = "./ultimate_dataset_16_one_drum_v2/"
tgt_folder = "./HMuseData/"
program_dict = {0: 'Piano',
                24: 'Nylon Guitar',
                27: 'Voiceless Electric Guitar',
                30: 'Distorted Electric Guitar',
                33: 'Finger Bass',
                36: 'Slap Bass'}
count = 0
for _, _, filenames in os.walk(src_folder):
    for filename in tqdm(filenames, desc="processing", unit="midi"):
        midi_data = pretty_midi.PrettyMIDI(f"{src_folder}{filename}")
        tgt_midi_data = pretty_midi.PrettyMIDI()
        bpm = round(midi_data.get_tempo_changes()[1][0])
        for track in midi_data.instruments:
            if track.is_drum:
                track.name = "Drum"
                tgt_midi_data.instruments.append(track)
            elif track.program in program_dict.keys():
                track.name = program_dict[track.program]
                tgt_midi_data.instruments.append(track)
        if len(tgt_midi_data.instruments) >= 2:
            count = count + 1
            tgt_midi_data.write(f"{tgt_folder}{filename}")
            tempo_adjustment(
                f"{tgt_folder}{filename}",
                f"{tgt_folder}{filename}",
                bpm)
            midi_data = note_alignment_16(f"{tgt_folder}{filename}")
            midi_data.write(f"{tgt_folder}{filename}")
count
