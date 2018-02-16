'''
This module contains some primitve methods in computer geometry
'''
import turtle
from cmath import inf
from random import random, randint
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
    '''
    Helper function.
    :param p1: point
    :param p2: point
    :return: euclidean distance of two points
    '''
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

    if len(input_list) == 0:
        return input_list

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
    Determinates orientation of 3 points
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
    Determinates whether segments intersect
    :param s1: segment
    :param s2: segment
    :return: True if segments intersect, False otherwise
    '''

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
    Helper function
    :param s: stack
    :return: point next to top point
    '''
    first = s.peek()
    s.pop()
    second = s.peek()
    s.push(first)
    return second


def stack_to_list(s) -> list:
    '''
    Helper function
    :param s: stack
    :return: list with elements from stack
    '''
    final_list = list()
    while not s.isEmpty():
        final_list.append(s.peek())
        s.pop()
    return final_list

def sort_list(input_list: List[Point]) -> List[Point]:
    '''
    Args:
        input_list: list of points

    Returns: sorted list of points

    '''
    def _get_tan(point: Point) -> float:
        '''
        :param point: upon which calcutes tangens
        :return: order of sorting
        '''
        left_point = input_list[0]
        if point.x == left_point.x:
            return -inf
        return (left_point.y - point.y) / (left_point.x - point.x)

    input_list.sort()
    input_list = input_list[:1] + sorted(input_list[1:], key=_get_tan)
    return input_list

def graham_scan(input_list: List[Point]) -> Polygon:
    '''
    Method for generation convex polygon
    :param input_list: input_list
    :return: convex polygon
    '''

    # input_list = get_simple_polygon(input_list)
    convex_hull = []
    input_list = sort_list(input_list)
    for p in input_list:
        while len(convex_hull) > 1 and ccw(convex_hull[-2], convex_hull[-1], p) <= 0:
            convex_hull.pop()
        convex_hull.append(p)
    return Polygon(convex_hull)


def point_in_triangle(triangle: Triangle, inspect_point: Point) -> bool:
    '''
    :param triangle: triangle
    :param inspect_point: point
    :return: True if inspect_point is in triangle, False otherwise
    '''
    ccw_ABD = ccw(triangle.first, triangle.second, inspect_point)
    ccw_BCD = ccw(triangle.second, triangle.third, inspect_point)
    ccw_CAD = ccw(triangle.third, triangle.first, inspect_point)

    return (ccw_ABD >= 0 and ccw_BCD >= 0 and ccw_CAD >= 0) or (ccw_ABD <= 0 and ccw_BCD <= 0 and ccw_CAD <= 0)


def point_in_polygon(polygon: Polygon, inspect_point: Point) -> bool:
    '''
    :param polygon: polygon
    :param inspect_point: point
    :return: True if inspect_point is in polygon, False otherwise
    '''

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
    '''
    Determinates polygon's orientation
    :param polygon: polygon
    :return: 1 if polygon's orientation is cw, -1 otherwise
    '''
    sum = 0
    for i in range(len(polygon.points)-1):
        sum += (polygon.points[i+1].x-polygon.points[i].x)*(polygon.points[i+1].y+polygon.points[i].y)
    print(sum)
    if sum > 0: return 1
    return -1


def segment_polygon_intersection(polygon: Polygon, segment: Segment) -> bool:
    '''
    Determinates whether segment and polygon intersect
    :param polygon: polygon
    :param segment: segment
    :return: True if segment and polygon intersect, False otherwise
    '''
    for i in range(len(polygon.points)):
        if segments_intersect(Segment(polygon.points[i%len(polygon.points)], polygon.points[(i+1)%len(polygon.points)]), segment):
            return True

    return False


def is_triangle_empty(input_list: List[Point], triangle: Triangle) -> None:
    '''
    Determinates whether some points from input list are in triangle
    :param input_list: list of points
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
    :param input_list: list of points
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
    for i in range(1, len(polygon.points)):
        new_ccw = ccw(polygon.points[i%len(polygon.points)], polygon.points[(i+1)%len(polygon.points)], polygon.points[(i+2)%len(polygon.points)])
        if old_ccw != new_ccw:
            return False

    return True





#Test for algorithm "get_simple_polygon"
# input_list = []
# n = 50
# input_x_list = [randint(-200,200) for _ in range(0,n)]
# input_y_list = [randint(-200, 200) for _ in range(0,n)]
# for i in range(n):
#     input_list.append(Point(input_x_list[i], input_y_list[i]))
# p = Polygon(get_simple_polygon(input_list))
# p.draw(turtle, "blue")


#Test for alghoritm "convex_polygon"
# input_list = []
# n = 100000
# input_x_list = [randint(-200,200) for _ in range(0,n)]
# input_y_list = [randint(-200, 200) for _ in range(0,n)]
# for i in range(n):
#     input_list.append(Point(input_x_list[i], input_y_list[i]))
# q = graham_scan(input_list)
# q.draw(turtle, "red")


#Test for algorithm "point_in_triangle"
# point_first = Point(randint(-200, 200),randint(-200,200))
# point_second = Point(randint(-200, 200),randint(-200,200))
# point_third = Point(randint(-200, 200),randint(-200,200))
# inspect_point = Point(randint(-200, 200),randint(-200,200))
#
# t = Triangle(point_first, point_second, point_third)
# t.draw(turtle, "green")
# turtle.up()
# inspect_point.draw(turtle, "yellow")
# turtle.up()
# turtle.setpos(-100,-250)
# turtle.color("red")
# if(point_in_triangle(t, inspect_point)):
#     turtle.write("Point is in triangle", font=("Arial", 16, "bold"))
# else:
#          turtle.write("Point is not in triangle", font=("Arial", 16, "italic"))


#Test for algorithm "point_in_polygon"
# point = Point(randint(-200, 200),randint(-200,200))
# input_list = []
# n = 20
# input_x_list = [randint(-200,200) for _ in range(0,n)]
# input_y_list = [randint(-200, 200) for _ in range(0,n)]
# for i in range(n):
#     input_list.append(Point(input_x_list[i], input_y_list[i]))
#
# p = Polygon(get_simple_polygon(input_list))
# p.draw(turtle, "blue")
# point.draw(turtle, "green")
# turtle.up()
# turtle.setpos(-100,-250)
# turtle.color("red")
# if point_in_polygon(p, point):
#      turtle.write("Point is in polygon", font=("Arial", 16, "bold"))
# else:
#      turtle.write("Point is not in polygon", font=("Arial", 16, "italic"))


#Test for algorithm "segments_intersects"
# point_x_first = Point(randint(-200, 200),randint(-200,200))
# point_y_first = Point(randint(-200, 200),randint(-200,200))
# point_x_second = Point(randint(-200, 200),randint(-200,200))
# point_y_second = Point(randint(-200, 200),randint(-200,200))
#
# point_x_first = Point(0, 0)
# point_y_first = Point(0, 100)
# point_x_second = Point(0, 100)
# point_y_second = Point(100, 200)
# s1 = Segment(point_x_first, point_y_first)
# s1.draw(turtle, "green")
# turtle.up()
# s2 = Segment(point_x_second, point_y_second)
# s2.draw(turtle, "yellow")
# turtle.up()
# turtle.setpos(-100,-250)
# turtle.color("red")
# if( segments_intersect(s1, s2)):
#     turtle.write("Segments do intersect", font=("Arial", 16, "bold"))
# else:
#    turtle.write("Segments do not intersect", font=("Arial", 16, "italic"))
# turtle.done()

#Test for algorithm "ccw"
# point_first = Point(randint(-200, 200),randint(-200,200))
# point_second = Point(randint(-200, 200),randint(-200,200))
# point_third = Point(randint(-200, 200),randint(-200,200))
# turtle.up()
# point_first.draw(turtle, "green")
# turtle.up()
# point_second.draw(turtle, "yellow")
# turtle.up()
# point_third.draw(turtle, "blue")
# turtle.up()
# turtle.setpos(-100,-250)
# turtle.color("red")
#
# if(ccw(point_first, point_second, point_third)) > 0:
#     turtle.write("CCW", font=("Arial", 16, "bold"))
# elif(ccw(point_first, point_second, point_third)) <0:
#     turtle.write("NOT CCW", font=("Arial", 16, "bold"))
# else:
#     turtle.write("Points are colinear", font=("Arial", 16, "bold"))


#Test for algorithm "polygon_orientation"
# input_list = []
# n = 10
# input_x_list = [randint(-200,200) for _ in range(0,n)]
# input_y_list = [randint(-200, 200) for _ in range(0,n)]
# for i in range(n):
#     input_list.append(Point(input_x_list[i], input_y_list[i]))
# p = graham_scan(input_list)
# p.draw(turtle, "blue")
#
# turtle.up()
# turtle.setpos(-100,-250)
# turtle.color("red")
#
# if(polygon_orientation(p)) < 0:
#     turtle.write("Orientation: CCW", font=("Arial", 16, "bold"))
# else:
#     turtle.write("Orientation: CW", font=("Arial", 16, "bold"))


#Test for algorithm "segment_polygon_intersection"
# input_list = []
# n = 10
# input_x_list = [randint(-200,200) for _ in range(0,n)]
# input_y_list = [randint(-200, 200) for _ in range(0,n)]
# for i in range(n):
#     input_list.append(Point(input_x_list[i], input_y_list[i]))
# p = Polygon(get_simple_polygon(input_list))
# p.draw(turtle, "blue")
#
# point_x_first = Point(randint(-200, 200),randint(-200,200))
# point_y_first = Point(randint(-200, 200),randint(-200,200))
#
# turtle.up()
# s1 = Segment(point_x_first, point_y_first)
# s1.draw(turtle, "green")
#
# turtle.up()
# turtle.setpos(-100,-250)
# turtle.color("red")
#
# if(segment_polygon_intersection(p,s1)):
#     turtle.write("Polygon and segment do intersect", font=("Arial", 16, "bold"))
# else:
#     turtle.write("Polygon and segment do not intersect", font=("Arial", 16, "bold"))


#Test for algorithm "is_empty_triangle"
# input_list = []
# n = 18
# input_x_list = [randint(-200,200) for _ in range(0,n)]
# input_y_list = [randint(-200, 200) for _ in range(0,n)]
# for i in range(n):
#     input_list.append(Point(input_x_list[i], input_y_list[i]))
#
# point_first = Point(randint(-200, 200),randint(-200,200))
# point_second = Point(randint(-200, 200),randint(-200,200))
# point_third = Point(randint(-200, 200),randint(-200,200))
#
#
# t = Triangle(point_first, point_second, point_third)
# t.draw(turtle, "green")
# turtle.up()
# for i in range(n):
#     input_list[i].draw(turtle, "blue")
#     turtle.up()
#
# turtle.up()
# turtle.setpos(-100,-250)
# turtle.color("red")

# if(is_triangle_empty(input_list,t)):
#     turtle.write("Triangle is empty", font=("Arial", 16, "bold"))
# else:
#     turtle.write("Triangle is not empty", font=("Arial", 16, "bold"))for i in range(n):
#     input_list[i].draw(turtle, "blue")
#     turtle.up()


#Test for algorithm "is_polygon_empty"
# input_list = []
# n = 18
# input_x_list = [randint(-200,200) for _ in range(0,n)]
# input_y_list = [randint(-200, 200) for _ in range(0,n)]
# for i in range(n):
#     input_list.append(Point(input_x_list[i], input_y_list[i]))
# p = Polygon(get_simple_polygon(input_list))
# p.draw(turtle, "blue")
# turtle.up()
#
# input_list_points = []
# n = 18
# input_x_list_points = [randint(-200,200) for _ in range(0,n)]
# input_y_list_points = [randint(-200, 200) for _ in range(0,n)]
# for i in range(n):
#     input_list_points.append(Point(input_x_list_points[i], input_y_list_points[i]))
#
# for i in range(n):
#     input_list_points[i].draw(turtle, "green")
#     turtle.up()
#
# turtle.setpos(-100,-250)
# turtle.color("red")
#
# if(is_polygon_empty(input_list_points, p)):
#     turtle.write("Polygon is empty", font=("Arial", 16, "bold"))
# else:
#     turtle.write("Polygon is not empty", font=("Arial", 16, "bold"))


#Test for algorithm "convex_polygon"
# point_first = Point(randint(-200, 200),randint(-200,200))
# point_second = Point(randint(-200, 200),randint(-200,200))
# point_third = Point(randint(-200, 200),randint(-200,200))
# point_fourth = Point(randint(-200, 200),randint(-200,200))
#
# q = Quadrilateral(Point(x=-100, y=-50), Point(x=-40, y=-95), Point(x=-80, y=45), Point(x=-140, y=-130))
# q.draw(turtle, "green")
#
# turtle.up()
# turtle.setpos(-100,-250)
# turtle.color("red")
# if(is_polygon_convex(q)):
#     turtle.write("Polygon is convex", font=("Arial", 16, "bold"))
# else:
#     turtle.write("Polygon is not convex", font=("Arial", 16, "bold"))
#
# turtle.done()




















