from typing import Tuple, List

from src.shape import shape_translation, shape_scaling, shape_rotation, shape_reflection, point_farther_north, \
    point_farther_east, point_farther_south, point_farther_west, vector_reverse, Vector2D, Shape2D

Multishape2D = List[Tuple[str, Shape2D]]


def multishape_middle(m: Multishape2D):
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
    return (right - left) / 2 + left, (top - down) / 2 + down


def multishape_translation(m: Multishape2D, v: Vector2D):
    for item in m:
        shape_translation(item[1], v)


def multishape_scaling(m: Multishape2D, scale_factor_x: float, scale_factor_y: float):
    mid = multishape_middle(m)
    for item in m:
        shape_scaling(item[1], scale_factor_x, scale_factor_y, mid)


# counterclockwise rotation of a vector through angle θ
def multishape_rotation(m: Multishape2D, θ: float):
    mid = multishape_middle(m)
    for item in m:
        shape_rotation(item[1], mid, θ)


def multishape_reflection(m: Multishape2D, vec_in_line: Vector2D):
    mid = multishape_middle(m)
    rev_mid = vector_reverse(mid)
    multishape_translation(m, rev_mid)
    for item in m:
        shape_reflection(item[1], vec_in_line)
    multishape_translation(m, mid)


# return tuple from shape
def point_farthest_north(m: Multishape2D):
    farthest_point = None
    north = float("-inf")
    for item in m:
        point = point_farther_north(item[1])
        if point[1] > north:
            north = point[1]
            farthest_point = point
    return farthest_point


# return tuple from shape
def point_farthest_east(m: Multishape2D):
    farthest_point = None
    east = float("-inf")
    for item in m:
        point = point_farther_east(item[1])
        if point[0] > east:
            east = point[0]
            farthest_point = point
    return farthest_point


# return tuple from shape
def point_farthest_south(m: Multishape2D):
    farthest_point = None
    south = float("inf")
    for item in m:
        point = point_farther_south(item[1])
        if point[1] < south:
            south = point[1]
            farthest_point = point
    return farthest_point


# return tuple from shape
def point_farthest_west(m: Multishape2D):
    farthest_point = None
    west = float("inf")
    for item in m:
        point = point_farther_west(item[1])
        if point[0] < west:
            west = point[0]
            farthest_point = point
    return farthest_point
