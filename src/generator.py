def compare_coord(item1, item2):
    if item1[0] < item2[0]:
        return -1
    elif item1[0] > item2[0]:
        return 1
    else:
        return 0


def add_tracks_from_country(midi_file, tracks, channel, tempo=60 * 5, volume=100):
    for track_nr, track in enumerate(tracks):
        track.sort(key=lambda coord: coord[0])
        notes = list()

        # after this note(pitch, time_seg, time_collision)
        for j, coord in enumerate(track):
            pitch = round(coord[1])  # pitch wysokość tonu

            time = round(coord[0]*5)
            if j > 0 and time == notes[j - 1][1]:
                k = 1
            else:
                k = 0

            notes.append((pitch, time, k))

        # after this note(pitch, time_seg, time_shift)
        for j, note in enumerate(notes):
            if j > 0:
                notes[j] = (note[0], note[1], notes[j - 1][2] + note[2])

        # after this note(pitch, time after shift)
        for j, note in enumerate(notes):
            notes[j] = (note[0], note[1] + note[2])

        # after this note(pitch, time, duration)
        for j, note in enumerate(notes):
            if j < len(notes) - 1:
                duration = notes[j + 1][1] - note[1]
            else:
                duration = 10
            notes[j] = (note[0], note[1], duration)

        midi_file.addTempo(track_nr, channel, tempo)
        for note in notes:
            pitch = note[0]
            time = note[1]
            duration = note[2]
            midi_file.addNote(track_nr, channel, pitch, time, duration, volume)


def save_file(midi_file, output_path_name):
    with open(output_path_name + ".mid", "wb") as output_file:
        midi_file.writeFile(output_file)
