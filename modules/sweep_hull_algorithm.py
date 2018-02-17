'''
Finds Delaunay trianguations of set of points using sweep hull algorithm
'''
import turtle
from random import randint
from typing import List, Tuple

import math
import numpy

from modules.primitives import get_x_coordinate, is_polygon_convex
from modules.sweep_line import any_intersection
from structures.line_segment import Segment
from structures.point import Point
from structures.polygon import Polygon
from structures.triangle import Triangle

turtle.speed(0)

class DelaunayTriangulationSegment(Segment):

    def __init__(self,first_point: Point, second_point: Point, first_triangle=None, second_triangle=None):
        super(DelaunayTriangulationSegment, self).__init__(first_point, second_point)
        self.first_triangle = first_triangle
        self.second_triangle = second_triangle

    def add_first_triangle(self, triangle: Triangle):
        self.first_triangle = triangle

    def __eq__(self, other):
        return ((self.first == other.first) and (self.second == other.second)) \
               or ((self.first == other.second) and (self.second == other.first))

    def add_second_triangle(self, triangle: Triangle):
        self.second_triangle = triangle

def is_point_outside_of_circum_circle(a: Point, b: Point, c: Point, d: Point) -> bool:
    '''
    Args:
        a: point of circum circle
        b: point of circum circle
        c: point of circum circle
        d: examined point

    Returns: False if point d is outside of circum circle which is determined by points a, b and c, True otherwise

    '''

    det = numpy.linalg.det([[a.x, a.y, (a.x ** 2 + a.y ** 2), 1],
                            [b.x, b.y, (b.x ** 2 + b.y ** 2), 1],
                            [c.x, c.y, (c.x ** 2 + c.y ** 2), 1],
                            [d.x, d.y, (d.x ** 2 + d.y ** 2), 1]])

    return det < 0


def get_triangle_vertices(edge, triangle) -> List:
    '''

    Args:
        edge: known one edge from triangle
        triangle: triangle

    Returns: List of two Tuple in which are coordinates of two vertices

    '''

    points = [edge.first, edge.second]

    if triangle.first not in points:

        return [(edge.first, triangle.first), (edge.second, triangle.first)]

    if triangle.second not in points:

        return [(edge.first, triangle.second), (edge.second, triangle.second)]

    if triangle.third not in points:

            return [(edge.first, triangle.third), (edge.second, triangle.third)]


def get_sum_of_angles_contrary_to_flipp_edge(flipp_edge: Segment, left_triangle: Triangle, right_triangle: Triangle) -> float:
    '''

    Args:
        flipp_edge: potentionaly edge to be flipped
        left_triangle: edge's left side triangle edge belongs
        right_triangle: edge's right side triangle edge belongs

    Returns: sum of contrary to flipp edge angles

    '''

    base_edge = flipp_edge.first.euclidean_distance(flipp_edge.second)
    left_triangle_edges = get_triangle_vertices(flipp_edge, left_triangle)
    b1 = left_triangle_edges[0][0].euclidean_distance(left_triangle_edges[0][1])
    c1 = left_triangle_edges[1][0].euclidean_distance(left_triangle_edges[1][1])

    right_triangle_edges = get_triangle_vertices(flipp_edge, right_triangle)
    b2 = right_triangle_edges[0][0].euclidean_distance(right_triangle_edges[0][1])
    c2 = right_triangle_edges[1][0].euclidean_distance(right_triangle_edges[1][1])

    left_angle = math.acos(((b1 ** 2) + (c1 ** 2) - (base_edge ** 2)) / (2 * b1 * c1))
    right_angle = math.acos(((b2 ** 2) + (c2 ** 2) - (base_edge ** 2)) / (2 * b2 * c2))

    return math.degrees(left_angle) + math.degrees(right_angle)


def get_point(edge: Segment, triangle: Triangle) -> Point:
    '''

    Args:
        edge: edge which belongs to traingle
        triangle: triangle

    Returns: point which is contrary do edge

    '''

    edge_points = [edge.first, edge.second]

    if triangle.first not in edge_points:

        return triangle.first

    if triangle.second not in edge_points:

        return triangle.second

    if triangle.third not in edge_points:

        return triangle.third



def flipp(flipp_edge: Segment, left_triangle: Triangle, right_triangle: Triangle, hull: List) -> None:
    '''

    Args:
        flipp_edge: potentinaly edge to be flipped
        left_triangle: edge's left side triangle edge belongs
        right_triangle: edge's right side triangle edge belongs
        hull: convex hull whose diagional is edge

    Returns:

    '''
    hull.remove(flipp_edge)

    new_edge_first_point = get_point(flipp_edge, left_triangle)
    new_edge_second_point = get_point(flipp_edge, right_triangle)
    new_edge = DelaunayTriangulationSegment(new_edge_first_point, new_edge_second_point)

    new_left_triangle = Triangle(new_edge.first, new_edge.second, flipp_edge.second)

    new_right_triangle = Triangle(new_edge.first, new_edge.second, flipp_edge.first)

    new_edge.first_triangle = new_left_triangle
    new_edge.second_triangle = new_right_triangle
    hull.append(new_edge)

    seg_1 = hull[hull.index(
        DelaunayTriangulationSegment(new_edge.first, flipp_edge.second))]
    seg_1.second_triangle = new_right_triangle

    seg_2 = hull[hull.index(
        DelaunayTriangulationSegment(new_edge.first, flipp_edge.first))]
    seg_2.second_triangle = new_left_triangle

    seg_3 = hull[hull.index(
        DelaunayTriangulationSegment(flipp_edge.second, new_edge.second))]
    seg_3.first_triangle = new_right_triangle

    seg_4 = hull[hull.index(
        DelaunayTriangulationSegment(flipp_edge.first, new_edge.second))]
    seg_4.first_triangle = new_left_triangle

    if seg_1.first_triangle != None and seg_1.second_triangle != None and  get_sum_of_angles_contrary_to_flipp_edge(seg_1, seg_1.first_triangle,
                                                seg_1.second_triangle) > 180:

        flipp(seg_1, seg_1.first_triangle, seg_1.second_triangle, hull)

    if seg_2.first_triangle != None and seg_2.second_triangle != None and get_sum_of_angles_contrary_to_flipp_edge(seg_2, seg_2.first_triangle,
                                                seg_2.second_triangle) > 180:

        flipp(seg_2, seg_2.first_triangle, seg_2.second_triangle, hull)

    if seg_3.first_triangle != None and seg_3.second_triangle != None and get_sum_of_angles_contrary_to_flipp_edge(seg_3, seg_3.first_triangle,
                                                seg_3.second_triangle) > 180:
        flipp(seg_3, seg_3.first_triangle, seg_3.second_triangle, hull)

    if seg_4.first_triangle != None and seg_4.second_triangle != None and get_sum_of_angles_contrary_to_flipp_edge(seg_4, seg_4.first_triangle,
                                                seg_4.second_triangle) > 180:
        flipp(seg_2, seg_4.first_triangle, seg_4.second_triangle, hull)


def get_four_diff_points_from_triangles(first_triangle: Triangle, second_triangle: Triangle) -> List:
    '''

    Args:
        first_triangle: one triangle
        second_triangle: second triangle

    Returns: four verticces the two triangles forms

    '''

    return_list = [first_triangle.first, first_triangle.second, first_triangle.third]

    if second_triangle.first not in return_list:
        return_list.insert(2, second_triangle.first)

        return return_list

    if second_triangle.second not in return_list:
        return_list.insert(2, second_triangle.second)

        return return_list


    if second_triangle.third not in return_list:
        return_list.insert(2, second_triangle.third)

        return return_list



def sweep_hull(input_list: List[Point]) -> List:
    '''

    Args:
        input_list: list of points

    Returns: list of segments of Delaunay triangulation

    '''

    # first step: sort input list by Euclidean distance
    left_point = sorted(input_list, key=get_x_coordinate)[0]

    def _get_euclidean_distance(point: Point) -> float:
        '''
        :param point: upon which calcutes Euclidean distance
        :return: order of sorting
        '''
        # distance = euclidean_distance(left_point, point)
        distance = (point.x - left_point.x) ** 2
        return distance

    input_list = sorted(input_list, key=_get_euclidean_distance)
    segments_to_flipp = []
    hull_segments = [
                            DelaunayTriangulationSegment(input_list[0], input_list[1],
                                                         Triangle(input_list[2], input_list[1], input_list[0])),
                            DelaunayTriangulationSegment(input_list[0], input_list[2],
                                                        Triangle(input_list[2], input_list[0], input_list[1])),
                            DelaunayTriangulationSegment(input_list[1], input_list[2],
                                                         Triangle(input_list[0], input_list[1], input_list[2]))
                            ]

    # second step: iterating
    for i, inspected_point in enumerate(input_list[3:]):

        new_triangle_segments = []
        flipp_edges = []
        for point in input_list[(i + 3 - 1)::-1]:

            new_segment = DelaunayTriangulationSegment(inspected_point, point)
            hull_segments.append(new_segment)

            if not any_intersection(hull_segments):
                hull_segments.pop()
                if len(new_triangle_segments) == 0:
                    new_triangle_segments.append(new_segment)
                else:

                    seg = new_triangle_segments.pop()

                    segment_from_hull = hull_segments[
                        hull_segments.index(DelaunayTriangulationSegment(point, seg.second))]

                    triang = Triangle(point, inspected_point, seg.second)
                    if new_segment.first_triangle == None:
                        new_segment.add_first_triangle(triang)
                    else:
                        new_segment.add_second_triangle(triang)


                    if segment_from_hull.first_triangle == None:
                        segment_from_hull.add_first_triangle(triang)
                    else:
                        segment_from_hull.add_second_triangle(triang)
                        points_list = get_four_diff_points_from_triangles(segment_from_hull.first_triangle,
                                                                          segment_from_hull.second_triangle)

                        inspect_polygon = Polygon(points_list)
                        if is_polygon_convex(inspect_polygon):
                            flipp_edges.append(segment_from_hull)

                    if seg.first_triangle == None:
                        seg.add_first_triangle(triang)
                    else:
                        seg.add_second_triangle(triang)

                    if seg.second.y > new_segment.second.y:
                        hull_segments.append(seg)
                        new_triangle_segments.append(new_segment)
                    else:
                        hull_segments.append(new_segment)
                        new_triangle_segments.append(seg)

            else:
                hull_segments.pop()

        if len(new_triangle_segments) != 0:

            hull_segments.append(new_triangle_segments.pop())

        while len(flipp_edges) > 0:

            flipp_edge = flipp_edges.pop()

            if get_sum_of_angles_contrary_to_flipp_edge(
                    flipp_edge, flipp_edge.first_triangle, flipp_edge.second_triangle) > 180:

                flipp(flipp_edge, flipp_edge.first_triangle, flipp_edge.second_triangle, hull_segments)


    for segment in hull_segments:

        segment.draw(turtle, "red")
        # if segment.first_triangle != None:
        #     calculate_center_of_circle(segment.first_triangle.first, segment.first_triangle.second,
        #                                segment.first_triangle.third)
        # if segment.second_triangle != None:
        #     calculate_center_of_circle(segment.second_triangle.first, segment.second_triangle.second,
        #                                segment.second_triangle.third)
    turtle.done()



    return hull_segments


def calculate_center_of_circle(p1: Point, p2: Point, p3: Point) -> Tuple:
    '''

    Args:
        p1: one point on circle
        p2: second point on circle
        p3: thrid point on circle

    Returns: center and radius of circle

    '''
    ma = (p2.y - p1.y) / (p2.x - p1.x)

    mb = (p3.y - p2.y) / (p3.x - p2.x)

    x = (ma*mb*(p1.y-p3.y) + mb*(p1.x+p2.x) - ma*(p2.x+p3.x))/(2*(mb-ma))

    y = (-1/mb)*(x - (p2.x+p3.x)/2) + (p2.y+p3.y)/2

    radius = p1.euclidean_distance(Point(x, y))
    draw_circle(turtle, Point(x, y), radius)

    return Point(x, y), radius

def draw_circle(turtle, center: Point, radius: float):
    '''

    Args:
        turtle: turtle
        center: center of circle
        radius: radius of circle

    Returns: draws circle

    '''
    turtle.colormode(255)
    t1 = randint(0, 255)
    t2 = randint(0, 255)
    t3 = randint(0, 255)
    turtle.color(t1, t2, t3)
    turtle.penup()
    turtle.goto(center.x, center.y-radius)
    turtle.pendown()
    turtle.circle(radius)


input_list = [
    Point(x=-100, y=-50),
    Point(x=-80, y=45),
    Point(x=-40, y=-95),
    Point(x=30, y=100),
    Point(x=0, y=0),
    Point(x=-10, y=-80),
    Point(x=100, y=0),
    Point(x=90, y=-95),
    Point(x=-90, y=-75),
    Point(x=100, y=50),
    Point(x=140, y=-30),
    Point(x=-140, y=-130)
]


se = sweep_hull(input_list)
