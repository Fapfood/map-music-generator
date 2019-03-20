from math import cos, sin
from typing import Tuple, List

Point2D = Tuple[float, float]
Vector2D = Point2D
Shape2D = List[Point2D]


# return new tuple
def vector_between(beg: Point2D, end: Point2D):
    return end[0] - beg[0], end[1] - beg[1]


# return double
def vector_length(v: Vector2D):
    return (v[0] ** 2 + v[1] ** 2) ** (1 / 2)


# return new tuple
def vector_reverse(v: Vector2D):
    return vector_scaling(v, -1, -1)


# return double
def scalar_product(v1: Vector2D, v2: Vector2D):
    return v1[0] * v2[0] + v1[1] * v2[1]


# return new tuple
def shape_middle(s: Shape2D):
    top = float("-inf")
    right = float("-inf")
    down = float("inf")
    left = float("inf")
    for point in s:
        if point[1] > top:
            top = point[1]
        if point[0] > right:
            right = point[0]
        if point[1] < down:
            down = point[1]
        if point[0] < left:
            left = point[0]
    return (right - left) / 2 + left, (top - down) / 2 + down


# return new tuple
def point_translation(p: Point2D, v: Vector2D):
    return p[0] + v[0], p[1] + v[1]


# update shape
def shape_translation(s: Shape2D, v: Vector2D):
    for i, point in enumerate(s):
        s[i] = point_translation(point, v)


# return new tuple
def vector_scaling(v: Vector2D, scale_factor_x, scale_factor_y):
    return v[0] * scale_factor_x, v[1] * scale_factor_y


# update shape
def shape_scaling(s: Shape2D, scale_factor_x, scale_factor_y, middle_of_scaling: Point2D):
    rev_mid = vector_reverse(middle_of_scaling)
    for i, point in enumerate(s):
        vec = vector_between(middle_of_scaling, point)
        vec = vector_scaling(vec, scale_factor_x, scale_factor_y)
        s[i] = vector_between(rev_mid, vec)


# return new tuple
# counterclockwise rotation of a vector through angle θ
def vector_rotation(v: Vector2D, θ):
    return v[0] * cos(θ) + v[1] * sin(θ), v[0] * sin(θ) + v[1] * cos(θ)


# update shape
# counterclockwise rotation of a vector through angle θ
def shape_rotation(s: Shape2D, rot_center: Point2D, θ):
    for i, point in enumerate(s):
        vec = vector_between(rot_center, point)
        s[i] = vector_rotation(vec, θ)


# return new tuple
def vector_reflection(vec_to_ref: Vector2D, vec_in_line: Vector2D):
    scale_fac = 2 * scalar_product(vec_to_ref, vec_in_line) / scalar_product(vec_in_line, vec_in_line)
    return scale_fac * vec_in_line[0] - vec_to_ref[0], scale_fac * vec_in_line[1] - vec_to_ref[1]


# update shape
def shape_reflection(s: Shape2D, vec_in_line: Vector2D):
    for i, point in enumerate(s):
        s[i] = vector_reflection(point, vec_in_line)


# return tuple from shape
def point_farther_north(s: Shape2D):
    result_point = None
    north = float("-inf")
    for point in s:
        if point[1] > north:
            north = point[1]
            result_point = point
    return result_point


# return tuple from shape
def point_farther_east(s: Shape2D):
    result_point = None
    east = float("-inf")
    for point in s:
        if point[0] > east:
            east = point[0]
            result_point = point
    return result_point


# return tuple from shape
def point_farther_south(s: Shape2D):
    result_point = None
    south = float("inf")
    for point in s:
        if point[1] < south:
            south = point[1]
            result_point = point
    return result_point


# return tuple from shape
def point_farther_west(s: Shape2D):
    result_point = None
    west = float("inf")
    for point in s:
        if point[0] < west:
            west = point[0]
            result_point = point
    return result_point


# update shape
def move_until_reach_point(s: Shape2D, p: Point2D):
    while s[0] != p:
        s.pop(0)
        s.append((s[0][0], s[0][1]))


# update shape and return new shape
def split_and_reverse_in_point(s: Shape2D, p: Point2D):
    second_list = list()
    while s[-1] != p:
        tmp = s.pop()
        second_list.append(tmp)
    second_list.append((s[-1][0], s[-1][1]))
    return second_list
