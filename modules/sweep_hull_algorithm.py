'''
Finds Delaunay trianguations of set of points using sweep hull algorithm
'''
import turtle
from bisect import bisect_left, bisect
from typing import List, Tuple

# import numpy
import math

import numpy

from modules.primitives import get_x_coordinate, euclidean_distance, is_polygon_convex
from modules.sweep_line import any_intersection, do_segments_intersects
from structures.line_segment import Segment
from structures.point import Point
from structures.polygon import Polygon
from structures.triangle import Triangle

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

def is_point_outside_of_circum_circle(a: Point, b: Point, c: Point, d: Point):
    '''
    Args:
        a: point of circum circle
        b: point of circum circle
        c: point of circum circle
        d: examined point

    Returns: false if point d is outside of circum circle which is determined by points a, b and c, true otherwise

    '''

    det = numpy.linalg.det([[a.x, a.y, (a.x ** 2 + a.y ** 2), 1],
                            [b.x, b.y, (b.x ** 2 + b.y ** 2), 1],
                            [c.x, c.y, (c.x ** 2 + c.y ** 2), 1],
                            [d.x, d.y, (d.x ** 2 + d.y ** 2), 1]])

    return det < 0


def get_edges(flipp_edge, left_trangle) -> List:
    if flipp_edge.first == left_trangle.first:
        if flipp_edge.second ==  left_trangle.second:
            return [(left_trangle.first, left_trangle.third), (left_trangle.second, left_trangle.third)]
        else:
            return [(left_trangle.first, left_trangle.second), (left_trangle.second, left_trangle.third)]
    elif flipp_edge.first == left_trangle.second :
        if flipp_edge.second == left_trangle.first:
            return [(left_trangle.first, left_trangle.third), (left_trangle.second, left_trangle.third)]
        else:
            return [(left_trangle.first, left_trangle.second), (left_trangle.first, left_trangle.third)]
    else:
        if flipp_edge.second == left_trangle.second:
            return [(left_trangle.first, left_trangle.third), (left_trangle.second, left_trangle.first)]
        else:
            return [(left_trangle.first, left_trangle.second), (left_trangle.second, left_trangle.third)]




def get_sum_of_angles_contrary_to_flipp_edge(flipp_edge: Segment, left_triangle: Triangle, right_triangle: Triangle) -> float:

    base_edge = flipp_edge.first.euclidean_distance(flipp_edge.second)
    left_triangle_edges = get_edges(flipp_edge, left_triangle)
    b1 = left_triangle_edges[0][0].euclidean_distance(left_triangle_edges[0][1])
    c1 = left_triangle_edges[1][0].euclidean_distance(left_triangle_edges[1][1])

    right_triangle_edges = get_edges(flipp_edge, right_triangle)
    b2 = right_triangle_edges[0][0].euclidean_distance(right_triangle_edges[0][1])
    c2 = right_triangle_edges[1][0].euclidean_distance(right_triangle_edges[1][1])

    print(base_edge, b1, c1, b2, c2)
    print(b1 ** 2)
    print(((b1 ** 2) + (c1 ** 2) - (base_edge ** 2)) / (2 * b1 * c1), ((b2 ** 2) + (c2 ** 2) - (base_edge ** 2)) / (2 * b2 * c2))
    left_angle = math.acos(((b1 ** 2) + (c1 ** 2) - (base_edge ** 2)) / (2 * b1 * c1))
    right_angle = math.acos(((b2 ** 2) + (c2 ** 2) - (base_edge ** 2)) / (2 * b2 * c2))

    print('left right angle', math.degrees(left_angle), math.degrees(right_angle))
    return math.degrees(left_angle) + math.degrees(right_angle)


def update_triangles(seg, new_left_triangle, new_right_triangle):
    seg.left_triangle = new_left_triangle
    seg.right_triangle = new_right_triangle


def flipp(flipp_edge: Segment, left_triangle: Triangle, right_triangle: Triangle, hull: List):
    print()
    hull.remove(flipp_edge)
    # new_left_triangle = Triangle(right_triangle.second, right_triangle.third, left_triangle.first)
    # new_right_triangle = Triangle(left_triangle.first, left_triangle.second, right_triangle.second)

    new_right_triangle = Triangle(right_triangle.second, right_triangle.third, left_triangle.first)
    new_left_triangle = Triangle(left_triangle.first, left_triangle.second, right_triangle.second)

    hull.append(DelaunayTriangulationSegment(left_triangle.first, right_triangle.second,
                                        new_left_triangle, new_right_triangle))
    print(left_triangle.first, left_triangle.second, right_triangle.first, right_triangle.second)
    print(new_left_triangle.first, new_left_triangle.second, new_right_triangle.first, new_right_triangle.second)
    seg_1 = hull[hull.index(
        DelaunayTriangulationSegment(left_triangle.first, left_triangle.second))]
    seg_1.second_triangle = new_right_triangle

    seg_2 = hull[hull.index(
        DelaunayTriangulationSegment(left_triangle.first, left_triangle.third))]
    seg_2.second_triangle = new_left_triangle

    seg_3 = hull[hull.index(
        DelaunayTriangulationSegment(right_triangle.first, right_triangle.second))]
    seg_3.first_triangle = new_right_triangle

    seg_4 = hull[hull.index(
        DelaunayTriangulationSegment(right_triangle.second, right_triangle.third))]
    seg_4.first_triangle = new_left_triangle

    if get_sum_of_angles_contrary_to_flipp_edge(seg_1, seg_1.first_triangle,
                                                seg_1.second_triangle) > 180:
        flipp(seg_1, seg_1.first_triangle, seg_1.second_triangle, hull)
    if get_sum_of_angles_contrary_to_flipp_edge(seg_2, seg_2.first_triangle,
                                                seg_2.second_triangle) > 180:
        flipp(seg_2, seg_2.first_triangle, seg_2.second_triangle, hull)

    if seg_3.first_triangle != None and seg_3.second_triangle != None and get_sum_of_angles_contrary_to_flipp_edge(seg_3, seg_3.first_triangle,
                                                seg_3.second_triangle) > 180:
        flipp(seg_3, seg_3.first_triangle, seg_3.second_triangle, hull)
    if seg_4.first_triangle != None and seg_4.second_triangle != None and get_sum_of_angles_contrary_to_flipp_edge(seg_4, seg_4.first_triangle,
                                                seg_4.second_triangle) > 180:
        flipp(seg_2, seg_4.first_triangle, seg_4.second_triangle, hull)


def sweep_hull(input_list: List[Point]):
    '''

    Args:
        input_list:

    Returns:

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
        # print('distance from', left_point.x,'to: ', point.x , ': ', distance)
        return distance

    input_list = sorted(input_list, key=_get_euclidean_distance)
    segments_to_flipp = []
    convex_hull_segments = [
                            DelaunayTriangulationSegment(input_list[0], input_list[1],
                                                         Triangle(input_list[2], input_list[1], input_list[0])),
                            DelaunayTriangulationSegment(input_list[0], input_list[2],
                                                        Triangle(input_list[2], input_list[0], input_list[1])),
                            DelaunayTriangulationSegment(input_list[1], input_list[2],
                                                         Triangle(input_list[0], input_list[1], input_list[2]))
                            ]

    # second step: adding
    for i, inspected_point in enumerate(input_list[3:]):

        # print(i)
        new_triangle_segments = []
        flipp_edges = []
        # convex_hull_segments_ = convex_hull_segments[:]
        for point in input_list[(i + 3 - 1)::-1]:

            new_segment = DelaunayTriangulationSegment(inspected_point, point)

            convex_hull_segments.append(new_segment)
            print(i, inspected_point, point)

            if not any_intersection(convex_hull_segments):
                convex_hull_segments.pop()
                if len(new_triangle_segments) == 0:
                    new_triangle_segments.append(new_segment)
                    # convex_hull_segments.append(new_segment)
                    # print(" i apendam")
                else:

                    seg = new_triangle_segments.pop()
                    # print('ne apendam, ali imam', seg.first, seg.second)
                    # provjerit da li postoji uopste ovaj segement

                    segment_from_convex_hull = convex_hull_segments[convex_hull_segments.index(DelaunayTriangulationSegment(point, seg.second))]

                    triang = Triangle(point, inspected_point, seg.second)
                    if new_segment.first_triangle == None:
                        new_segment.add_first_triangle(triang)
                    else:
                        new_segment.add_second_triangle(triang)


                    if segment_from_convex_hull.first_triangle == None:
                        segment_from_convex_hull.add_first_triangle(triang)
                    else:
                        segment_from_convex_hull.add_second_triangle(triang)
                        inspect_polygon = Polygon([segment_from_convex_hull.second_triangle.first,
                                                   segment_from_convex_hull.second_triangle.second,
                                                   segment_from_convex_hull.second_triangle.third,
                                                   segment_from_convex_hull.first_triangle.first])
                        # if point == Point(0, 0) and inspected_point == Point(-40, -95):
                        #     inspect_polygon.draw(turtle, 'blue')
                            # turtle.done()
                        if is_polygon_convex(inspect_polygon):
                            print('usaaaappp', inspect_polygon.points[0], inspect_polygon.points[1], inspect_polygon.points[2], inspect_polygon.points[3])
                            flipp_edges.append(segment_from_convex_hull)

                    if seg.first_triangle == None:
                        seg.add_first_triangle(triang)
                    else:
                        seg.add_second_triangle(triang)

                    if seg.second.y > new_segment.second.y:
                        convex_hull_segments.append(seg)
                        new_triangle_segments.append(new_segment)
                    else:
                        convex_hull_segments.append(new_segment)
                        new_triangle_segments.append(seg)

            else:
                # print('else')
                # if inspected_point == Point(0, 0) and point == Point(-40, -95):
                #     for segments in convex_hull_segments:
                #         segments.draw(turtle, "red")
                #     turtle.done()
                convex_hull_segments.pop()

        if len(new_triangle_segments) != 0:

            convex_hull_segments.append(new_triangle_segments.pop())

        print('flipp edges:', end=' ')

        for flipp_edge in flipp_edges:
            print(flipp_edge.first, flipp_edge.second, end='\n')
            # if get_sum_of_angles_contrary_to_flipp_edge(flipp_edge, flipp_edge.first_triangle, flipp_edge.second_triangle) < 180:
            #     print('flippat')

        while len(flipp_edges) > 0:
            # print('len', len(flipp_edges)-1)
            # convex_hull_segments.remove(flipp_edges[len(flipp_edges)-1])
            if get_sum_of_angles_contrary_to_flipp_edge(flipp_edge, flipp_edge.first_triangle, flipp_edge.second_triangle) > 180:
                flipp(flipp_edge, flipp_edge.first_triangle, flipp_edge.second_triangle, convex_hull_segments)

                print('flippat')
            flipp_edges.pop()

    for segment in convex_hull_segments:
        # print(segment.first, segment.second)
        segment.draw(turtle, "red")
    turtle.done()



    # print(input_list)
    # print(len(convex_hull_segments), convex_hull_segments[len(convex_hull_segments)-1].first, convex_hull_segments[len(convex_hull_segments)-1].second)
    return convex_hull_segments

# input_list = [
    # Point(x=-170, y=70),
    # Point(x=-160, y=40),
    # Point(x=-130, y=-20),
    # Point(x=-110, y=-50),
    # Point(x=0, y=-100),
    # Point(x=80, y=-100),
    # Point(x=140, y=-10),
    # Point(x=160, y=40),
    # Point(x=170, y=70),
    # Point(x=160, y=100),
    # Point(x=130, y=160),
    # Point(x=110, y=190),
    # Point(x=80, y=200),
    # Point(x=0, y=200),
    # Point(x=-110, y=190),
    # Point(x=-130, y=160),
    # Point(x=-160, y=100)
# ]

input_list = [
    Point(x=-100, y=-50),
    Point(x=-80, y=45),
    Point(x=-40, y=-95),
    Point(x=30, y=100),
    Point(x=0, y=0),
    Point(x=-50, y=-80),
    Point(x=100, y=0),
    Point(x=90, y=-100),
    Point(x=100, y=50),
    Point(x=140, y=-30),
    Point(x=-140, y=-130)
]


se = sweep_hull(input_list)
# se = [Segment(Point(x=-100, y=-50), Point(x=-80, y=45)), Segment(Point(x=-100, y=-50), Point(x=-40, y=-95)), Segment(Point(x=-80, y=45), Point(x=-40, y=-95)),
#       Segment(Point(x=0, y=0), Point(x=-80, y=45)), Segment(Point(x=0, y=0), Point(x=-40, y=-95)), Segment(Point(x=0, y=0), Point(x=30, y=100)),
#       Segment(Point(x=-40, y=-95), Point(x=30, y=100))]
# print(any_intersection(se))
# for segments in se:
#     segments.draw(turtle, "red")
# turtle.done()
# p = Polygon(input_list)
# p.draw(turtle, "red")
# turtle.done()
# print(is_point_outside_of_circum_circle(Point(-100, 0), Point(100, 0), Point(0, 100), Point(-100, 0)))

# t = Triangle(Point(-100, 0), Point(100, 0), Point(0, 100))
# t.draw(turtle, "green")
# turtle.penup()
# turtle.setposition(0, -100)
# turtle.pendown()
# turtle.circle(100)
# turtle.up()
# Point(-50, 0).draw(turtle, "yellow")
# turtle.up()
# turtle.done()
# s = DelaunayTriangulationSegment(Point(0,0),Point(0, 100), Triangle(Point(0,0), Point(0,10), Point(0,20)), Triangle(Point(0,0), Point(0,10), Point(0,20)))