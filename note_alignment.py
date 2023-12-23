import pretty_midi
from tempo_calculation import find_closest_element


def create_timestamp_array(max_time, standard_timestamp):
    timestamp_array = []
    current_time = 0

    while current_time <= max_time:
        timestamp_array.append(round(current_time, 8))
        current_time += standard_timestamp

    return timestamp_array


def note_alignment_32(midi_file):
    midi_data = pretty_midi.PrettyMIDI(midi_file)
    tempo = round(midi_data.get_tempo_changes()[1][0])
    standard_timestamp = 60 / tempo / 8
    max_time = midi_data.get_end_time()
    timestamp_grid = create_timestamp_array(max_time, standard_timestamp)
    for midi_track in midi_data.instruments:
        notes = midi_track.notes
        for note in notes:
            note.start = find_closest_element(note.start, timestamp_grid)
            note.end = find_closest_element(note.end, timestamp_grid)
            if note.end == note.start:
                note.end = note.start + standard_timestamp
    return midi_data


def note_alignment_16(midi_file):
    midi_data = pretty_midi.PrettyMIDI(midi_file)
    tempo = round(midi_data.get_tempo_changes()[1][0])
    standard_timestamp = 60 / tempo / 4
    max_time = midi_data.get_end_time()
    timestamp_grid = create_timestamp_array(max_time, standard_timestamp)
    for midi_track in midi_data.instruments:
        notes = midi_track.notes
        for note in notes:
            note.start = find_closest_element(note.start, timestamp_grid)
            note.end = find_closest_element(note.end, timestamp_grid)
            if note.end == note.start:
                note.end = note.start + standard_timestamp
    return midi_data
