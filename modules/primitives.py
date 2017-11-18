'''
This module contains some primitve methods in computer geometry
'''
from cmath import inf
from random import random
from typing import List, Tuple
import math

from structures.line_segment import Segment
from structures.point import Point

# helping methods
from structures.polygon import Polygon
from structures.quadrilateral import Quadrilateral
from structures.stack import Stack
from structures.triangle import Triangle


def euclidean_distance(p1: Point, p2: Point) -> float:
    return math.sqrt((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2)

def get_x_coordinate(point: Point) -> Tuple[float, float]:
    '''
    :param point: point which coordinates we use
    :return: order of sorting
    '''
    return (point.x, -point.y)

def get_simple_polygon(input_list: List[Point]) -> List[Point]:
    '''
    Method get_simple_polygon implemented by algorithm for finding a simple polygon
    for given input points.
    :param input_list: input list of polygon points
    :return: list of Points for generating a simple polygon
    '''
    left_point = sorted(input_list, key=get_x_coordinate)[0]

    def _get_tan(point: Point) -> Tuple[float, float]:
        '''
        :param point: upon which calcutes tangens and Euclidean distance
        :return: order of sorting
        '''
        distance = euclidean_distance(left_point, point)
        if point.x == left_point.x:
            tan = -inf
        else:
            tan = (point.y - left_point.y) / (point.x - left_point.x)
        if point.y == left_point.y:
            distance *= -1
        return (tan, distance)

    return sorted(input_list, key=_get_tan)

def on_segment(p: Point, q: Point, r: Point) -> bool:
    '''
    Determinates whether point q in on segment pr
    :param p: first point of segment pr
    :param q: inpect point
    :param r: second point of segment pr
    :return: True if point q is on segment pr, False otherwise
    '''
    if (q.x <= max(p.x, r.x) and q.x >= min(p.x, r.x) and
            q.y <= max(p.y, r.y) and q.y >= min(p.y, r.y)):
        return True
    return False

def ccw(p1: Point, p2: Point, p3: Point) -> float:
    '''
    Computes orientation of 3 points
    :param p1: point
    :param p2: point
    :param p3: point
    :return: positive number if points are counter-clockwise oriented, zero if they're collinear
            and negative number if they're clockwise oriented
    '''
    value = (p2.x-p1.x)*(p3.y-p1.y) - (p3.x-p1.x)*(p2.y-p1.y)
    if value == 0: return 0
    elif value > 0: return 1
    return -1

def segments_intersect(s1: Segment, s2: Segment) -> bool:
    '''
    determinates whether segments intersects
    :param s1:
    :param s2:
    :return: true if segment intersects and false if they're not
    '''
    # if(s1 == s2): return True
    o1 = ccw(s1.first, s1.second, s2.first)
    o2 = ccw(s1.first, s1.second, s2.second)
    o3 = ccw(s2.first, s2.second, s1.first)
    o4 = ccw(s2.first, s2.second, s1.second)

    if o1 != o2 and o3 != o4:
        return True

    if o1 == 0 and on_segment(s1.first, s2.first, s1.second): return True
    if o2 == 0 and on_segment(s1.first, s2.second, s1.second): return True
    if o3 == 0 and on_segment(s2.first, s1.first, s2.second): return True
    if o4 == 0 and on_segment(s2.first, s1.second, s2.second): return True

    return False


def get_y_coordinate(point: Point) -> Tuple[float, float]:
    return (point.y, -point.x)

def next_to_top(s):
    '''
    :param s: stack
    :return: point next to top point
    '''
    first = s.peek()
    s.pop()
    second = s.peek()
    # s.push(second)
    s.push(first)
    return second


def stack_to_list(s) -> list:
    '''
    :param s: stack
    :return: list with elements from stack
    '''
    final_list = list()
    while not s.isEmpty():
        final_list.append(s.peek())
        s.pop()
    return final_list

def graham_scan(input_list: List[Point]) -> Polygon:
    '''
    method for generation convex polygon
    :param input_list:
    :return: convex polygon
    '''
    input_list = get_simple_polygon(input_list)
    # print(input_list)
    s = Stack()
    s.push(input_list[0])
    s.push(input_list[1])
    for i in range(2, len(input_list)):
        to_top = next_to_top(s)
        while ccw(to_top, s.peek(), input_list[i]) < 0:
            s.pop()
            to_top = next_to_top(s)
        s.push(input_list[i])
    input_list = stack_to_list(s)
    return Polygon(input_list)

def point_in_triangle(triangle: Triangle, inspect_point: Point) -> bool:
    '''
    :param triangle: triangle
    :param inspect_point:
    :return: true if inspect_point is inside of triangle, false otherwise
    '''
    ccw_ABD = ccw(triangle.first, triangle.second, inspect_point)
    ccw_BCD = ccw(triangle.second, triangle.third, inspect_point)
    ccw_CAD = ccw(triangle.third, triangle.first, inspect_point)

    return (ccw_ABD >= 0 and ccw_BCD >= 0 and ccw_CAD >= 0) or (ccw_ABD <= 0 and ccw_BCD <= 0 and ccw_CAD <= 0)

def point_in_polygon(polygon: Polygon, inspect_point: Point) -> bool:
    '''
    :param polygon:
    :param inspect_point:
    :return: True if inspect_point is inside of polygon, False otherwise
    '''
    # old_ccw = ccw(polygon.points[0], polygon.points[1], inspect_point)
    # for i in range(1,len(polygon.points)-1):
    #     new_ccw = ccw(polygon.points[i], polygon.points[i+1], inspect_point)
    #     print('i:', i, ' ', polygon.points[i])
    #     if(new_ccw*old_ccw < 0):
    #         return False
    # return True
    extreme_point = Point(inf, inspect_point.y)
    count = 0
    i = 0
    while True:
        next = (i+1)%len(polygon.points)
        if segments_intersect(Segment(polygon.points[i], polygon.points[next]), Segment(inspect_point, extreme_point)):
            print('segment intersects')
            if ccw(polygon.points[i], inspect_point,polygon.points[next]) == 0:
                print('collinear')
                return on_segment(polygon.points[i],inspect_point, polygon.points[next])
            count += 1
        i = next
        if i == 0:
            break

    return count % 2 == 1

def polygon_orientation(polygon: Polygon) -> float:
    sum = 0
    for i in range(len(polygon.points)-1):
        sum += (polygon.points[i+1].x-polygon.points[i].x)*(polygon.points[i+1].y+polygon.points[i].y)
    print(sum)
    if sum > 0: return 1
    return -1

def segment_polygon_intersection(polygon: Polygon, segment: Segment) -> bool:
    '''
    Determinates whether segment and polygon intersects
    :param polygon:
    :param segment:
    :return: True if segment and polygon intersects, False otherwise
    '''
    for i in range(len(polygon.points)-1):
        if segments_intersect(Segment(polygon.points[i], polygon.points[i+1]), segment):
            return True

    return False

def is_triangle_empty(input_list: List[Point], triangle: Triangle) -> None:
    '''
    Deeterminate whether some points from input list are in triangle
    :param input_list: list of point
    :param triangle:
    :return: True if triangle is empty, False otherwise
    '''
    sum_of_points_in_triangle = 0
    for i in range(len(input_list)):
        if(point_in_triangle(triangle, input_list[i])):
            sum_of_points_in_triangle += 1

    return sum_of_points_in_triangle == 0

def is_polygon_empty(input_list: List[Point], polygon: Polygon) -> None:
    '''
    :param input_list: list of point
    :param polygon: polygon
    :return: True if polygon is empty, False otherwise
    '''
    sum_of_points_in_polygon = 0
    for i in range(len(input_list)):
        if(point_in_polygon(polygon, input_list[i])):
            sum_of_points_in_polygon += 1

    return sum_of_points_in_polygon == 0

def is_polygon_convex(polygon: Polygon) -> bool:
    '''
    :param polygon: polygon
    :return: True if polygon is convex, False otherwise
    '''
    old_ccw = ccw(polygon.points[0], polygon.points[1], polygon.points[2])
    for i in range(1, len(polygon.points)-1):
        new_ccw = ccw(polygon.points[i%len(polygon.points)], polygon.points[(i+1)%len(polygon.points)], polygon.points[(i+2)%len(polygon.points)])
        if old_ccw != new_ccw:
            return False

    return True

# q = Quadrilateral(Point(0,0), Point(50, 50), Point(100, 0), Point(50, 100))
# q.draw()
# print(is_polygon_convex(q))
# s1 = Segment(Point(0,0), Point(100, 0))
# s2 = Segment(Point(150, 0), Point(170, 0))
# print(segments_intersect(s1, s2))
# triangle_points = [Point(0,0), Point(100, 0), Point(50, 100), Point(30, 0)]
# pol = Polygon(triangle_points)
# pol.draw()
# print(ccw(Point(0, 0), Point(50, 0), Point(100, 0)), ' ' , ccw(Point(0, 0), Point(-50, 0), Point(100, 0)))

input_points = [Point(0,0),
                Point(200, 100),
                Point(0, 100),
                Point(200, 0),
                Point(50, 30),
                # Point(100, 110),
                Point(150, 300),
                Point(100, 0),
                Point(30, 50),
                Point(-50, 50),
                Point(10,210)]

input_list = [Point(0, 0),
                    Point(200, 100),
                    Point(0, 100),
                    Point(200, 0),
                    Point(200, 200),
                    Point(50, 30),
                    Point(100, 110),
                    Point(150, 190),
                    Point(-50, 10),
                    Point(100, 0),
                    Point(30, 50),
                    Point(-50, 210),
                    Point(-50, 50),
                    Point(-40, 50),
                    Point(10, 210)]

# p = Polygon(get_simple_polygon(input_list))
# t = Triangle(Point(-100, 0), Point(-60, 0), Point(-70, 150))
# t.draw()
# print(point_in_polygon(p, Point(100, 150)))
# p.draw()
# print(is_triangle_empty(input_list, t))
# Polygon(get_simple_polygon(input_list)).draw()
# q = graham_scan(input_list)
# print(segment_polygon_intersection(p, s2))
# q.draw()
# p1 = Point(0, 0)
# p2 = Point(100, 0)
# p3 = Point(50, -30)
# p = Polygon([p1, p2, p3])
# print(ccw(p1, p2, p3))
# p.draw()

# print(on_segment(Point(0,0), Point(0,0), Point(0, 100)))