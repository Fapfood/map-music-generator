from src.multishape import multishape_middle, multishape_scaling, multishape_translation, point_farthest_north, \
    point_farthest_east, point_farthest_south, point_farthest_west

from src.shape import vector_between, point_farther_west, point_farther_east, move_until_reach_point, \
    split_and_reverse_in_point, point_farther_north, point_farther_south


# longitude - długość geograficzna WE
# latitude - szerokość geograficzna SN


def fraction_of_fill_multishape_in_area(multishape, max_n, max_e, max_s, max_w):
    point_north = point_farthest_north(multishape)
    point_east = point_farthest_east(multishape)
    point_south = point_farthest_south(multishape)
    point_west = point_farthest_west(multishape)
    return (vector_between(point_west, point_east)[0] / (max_e - max_w),
            vector_between(point_south, point_north)[1] / (max_n - max_s))


def fraction_of_fill_shape_in_multishape(shape, multishape):
    farthest_north = point_farthest_north(multishape)
    farthest_east = point_farthest_east(multishape)
    farthest_south = point_farthest_south(multishape)
    farthest_west = point_farthest_west(multishape)
    farther_north = point_farther_north(shape)
    farther_east = point_farther_east(shape)
    farther_south = point_farther_south(shape)
    farther_west = point_farther_west(shape)
    return (vector_between(farther_west, farther_east)[0] / vector_between(farthest_west, farthest_east)[0],
            vector_between(farther_south, farther_north)[1] / vector_between(farthest_south, farthest_north)[1])


# TO IMPORT
def normalize(multishape, max_n, max_e, max_s, max_w):
    mid_old = multishape_middle(multishape)
    mid_new = (max_e - max_w) / 2 + max_w, (max_n - max_s) / 2 + max_s
    multishape_translation(multishape, vector_between(mid_old, mid_new))
    fill = fraction_of_fill_multishape_in_area(multishape, max_n, max_e, max_s, max_w)
    multishape_scaling(multishape, 1 / fill[0], 1 / fill[1])


# TO IMPORT
def prepare_tracks(multishape):
    tracks = list()
    for item in multishape:
        l1 = item[1]
        move_until_reach_point(l1, point_farther_west(l1))
        l2 = split_and_reverse_in_point(l1, point_farther_east(l1))
        tracks.append(l1)
        tracks.append(l2)
    return tracks


# from 'countries_coordinates.json': alpha-3 -> geometry
def code3_geometry():
    import json
    with open('jsons_data/countries_coordinates.json', 'r', encoding="utf8") as f:
        c = json.loads(f.read())
        return {country_data['id']: country_data['geometry']
                for country_data in c['features']}


# przyjmuje polygon ([linearring], gdzie pierwszy jest zewnętrzny, a kolejne to dziury)
def polygon_coords_parse(pol):
    def list_list2list_tup(linearring):
        return [tuple(pair) for pair in linearring]

    polygons = [('sub', list_list2list_tup(item)) for item in pol[1:]]
    polygons.append(('add', list_list2list_tup(pol[0])))
    return polygons


def geometry2coords(geo):
    from itertools import chain
    coordinates = geo['coordinates']
    if geo['type'] == 'MultiPolygon':
        polygons = [polygon_coords_parse(polygon) for polygon in coordinates]
        return list(chain.from_iterable(polygons))
    elif geo['type'] == 'Polygon':
        return polygon_coords_parse(coordinates)
    else:
        print('Nie rozpoznano typu geoJSONa')


# TO IMPORT
# return multishape
def country_coordinates(code3):
    if code3 is not None:
        geo = code3_geometry().get(code3)
        if geo is not None:
            return geometry2coords(geo)
        else:
            print('Error')
