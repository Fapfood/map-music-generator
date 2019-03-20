from src.arguments_parser import parse
from src.coords_operations import country_coordinates, normalize, prepare_tracks
from midiutil import MIDIFile
from src.multishape import multishape_scaling, multishape_reflection, multishape_rotation, multishape_translation

from src.generator import save_file, add_tracks_from_country


def adapt_to_requrements(requirement):
    multishape = country_coordinates(requirement[0])
    for op in requirement[1]:
        if op[0] == "scl":
            multishape_scaling(multishape, op[1], op[2])
        if op[0] == "rot":
            multishape_rotation(multishape, op[1])
        if op[0] == "ref":
            multishape_reflection(multishape, (op[1], op[2]))
        if op[0] == "tsl":
            multishape_translation(multishape, (op[1], op[2]))
    return multishape


def max_len(tracks_list):
    len_tracks = 0
    for t in tracks_list:
        if len(t) > len_tracks:
            len_tracks = len(t)
    return len_tracks


def determine_boundaries(multishape_list):
    top = float("-inf")
    right = float("-inf")
    down = float("inf")
    left = float("inf")

    for m in multishape_list:
        for item in m:
            for point in item[1]:
                if point[1] > top:
                    top = point[1]
                if point[0] > right:
                    right = point[0]
                if point[1] < down:
                    down = point[1]
                if point[0] < left:
                    left = point[0]
    return {'n': top, 'e': right, 's': down, 'w': left}


def prepare_for_normalization(multishape_list):
    actual_max_nesw = determine_boundaries(multishape_list)

    if requirements.time is None:
        requirements.time = round(actual_max_nesw['e'] - actual_max_nesw['w'])

    if requirements.normalization is None:
        requirements.normalization = [abs(round(actual_max_nesw['s'])), abs(round(actual_max_nesw['n']))]

    expected_max_nesw = {'n': requirements.normalization[1], 'e': requirements.time,
                         's': requirements.normalization[0], 'w': 0}

    vertical_scale_factor = (expected_max_nesw['s'] - expected_max_nesw['n']) / (
        actual_max_nesw['s'] - actual_max_nesw['n'])
    horizontal_scale_factor = (expected_max_nesw['e'] - expected_max_nesw['w']) / (
        actual_max_nesw['e'] - actual_max_nesw['w'])

    for m in multishape_list:
        top = float("-inf")
        right = float("-inf")
        down = float("inf")
        left = float("inf")
        for item in m:
            for point in item[1]:
                if point[1] > top:
                    top = point[1]
                if point[0] > right:
                    right = point[0]
                if point[1] < down:
                    down = point[1]
                if point[0] < left:
                    left = point[0]

        actual_n = expected_max_nesw['n'] + (top - actual_max_nesw['n']) * vertical_scale_factor
        actual_e = expected_max_nesw['w'] + (right - actual_max_nesw['w']) * horizontal_scale_factor
        actual_s = expected_max_nesw['n'] + (down - actual_max_nesw['n']) * vertical_scale_factor
        actual_w = expected_max_nesw['w'] + (left - actual_max_nesw['w']) * horizontal_scale_factor

        normalize(m, actual_n, actual_e, actual_s, actual_w)


requirements = parse()

multishape_list = list()
for req in requirements.inputs:
    m = adapt_to_requrements(req)
    multishape_list.append(m)

prepare_for_normalization(multishape_list)
tracks_list = list()
for m in multishape_list:
    tracks = prepare_tracks(m)
    tracks_list.append(tracks)

MyMIDI = MIDIFile(max_len(tracks_list))  # One track, defaults to format 1 (tempo track is created automatically)

for i, t in enumerate(tracks_list):
    add_tracks_from_country(MyMIDI, t, i)

save_file(MyMIDI, requirements.path_name)
