import os
import pretty_midi
import mido
from mido import MidiFile, MidiTrack
from tqdm import tqdm
from tempo_calculation import find_closest_element, standard_bpm_set

source_dir = "./tgt_dataset/"
tgt_dir = './ultimate_dataset/'


def tempo_adjustment(src_midi, tgt_midi, new_bpm):
    midi_file = MidiFile(src_midi)
    new_midi_file = MidiFile(ticks_per_beat=midi_file.ticks_per_beat)
    for i, track in enumerate(midi_file.tracks):
        new_track = MidiTrack()
        new_midi_file.tracks.append(new_track)
        for msg in track:
            if msg.type == 'set_tempo':
                microseconds_per_beat = mido.bpm2tempo(new_bpm)
                new_msg = msg.copy(tempo=microseconds_per_beat)
                new_track.append(new_msg)
            else:
                new_track.append(msg)
    new_midi_file.save(tgt_midi)


for _, _, filenames in os.walk(source_dir):
    for filename in tqdm(filenames, desc="Processing", unit="midi"):
        midi_data = pretty_midi.PrettyMIDI(f"{source_dir}{filename}")
        tempo = midi_data.get_tempo_changes()[1][0]
        standard_tempo = find_closest_element(tempo, standard_bpm_set)
        tempo_adjustment(
            f"{source_dir}{filename}",
            f"{tgt_dir}{filename}",
            standard_tempo)

