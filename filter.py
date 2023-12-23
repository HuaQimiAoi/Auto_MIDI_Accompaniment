import mido


def standard_midi_filter(filename):
    mid = mido.MidiFile(filename)
    standard_counter = 0
    note_on_filter_flag = 0
    channel_9_filter_flag = 0
    tempo_sum = 0
    signature_sum = 0
    tempo_signature_filter_flag = 0
    every_track_one_channel_filter_flag = 0
    for i, track in enumerate(mid.tracks):
        if i >= 1:
            every_track_note_on_filter_flag = 0
            channel_set = set()
            for msg in track:
                if hasattr(msg, 'channel'):
                    channel_set.add(msg.channel)
                if msg.type == 'note_on':
                    every_track_note_on_filter_flag = 1
            if every_track_note_on_filter_flag == 0:
                return 0
            if len(channel_set) == 1:
                every_track_one_channel_filter_flag = 1

        for msg in track:
            if msg.type == 'note_off':
                note_on_filter_flag = 1
            if msg.type == 'note_on' and msg.channel == 9:
                channel_9_filter_flag = 1
            if msg.type == 'time_signature':
                signature_sum = signature_sum + 1
                if msg.numerator == 4 and msg.denominator == 4:
                    tempo_signature_filter_flag = 1
            if msg.type == 'set_tempo':
                tempo_sum = tempo_sum + 1

    if note_on_filter_flag == 0:
        standard_counter = standard_counter + 1
    if channel_9_filter_flag == 1:
        standard_counter = standard_counter + 1
    if tempo_signature_filter_flag == 1 and signature_sum == 1 and tempo_sum == 1:
        standard_counter = standard_counter + 1
    if every_track_one_channel_filter_flag == 1:
        standard_counter = standard_counter + 1
    return standard_counter
