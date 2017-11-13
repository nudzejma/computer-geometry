'''
This module contains some primitve methods in computer geometry
'''
from cmath import inf
from inspect import stack
from typing import List, Tuple
import math

from structures.line_segment import Segment
from structures.point import Point

# helping methods
from structures.polygon import Polygon
from structures.stack import Stack


def euclidean_distance(p1: Point, p2: Point) -> float:
    return math.sqrt((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2)

def get_x_coordinate(point: Point):
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
    # print(left_point)

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

def ccw(p1: Point, p2: Point, p3: Point) -> float:
    '''
    Computes orientation of 3 points
    :param p1: point
    :param p2: point
    :param p3: point
    :return: positive number if points are counter-clockwise oriented, zero if they're collinear
            and negative number if they're clockwise oriented
    '''
    return (p2.x-p1.x)*(p3.y-p1.y) - (p3.x-p1.x)*(p2.y-p1.y)

def segments_intersect(s1: Segment, s2: Segment) -> bool:
    if(s1 == s2): return True

    ccw1 = ccw(s1.first, s2.second, s2.first)
    ccw2 = ccw(s2.second, s2.first, s1.second)
    # print(ccw1,' ', ccw2)
    if(ccw1*ccw2 < 0):
        return True

    # if((ccw(s1.first, s1.second, s2.first)*ccw(s1.first, s1.second, s2.second) < 0) &
    #        (ccw(s2.first, s2.second, s1.first)*ccw(s2.first, s2.second, s1.second) < 0)):
    #     return True
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
    final_list = list()
    while not s.isEmpty():
        final_list.append(s.peek())
        s.pop()
    return final_list

def graham_scan(input_list: List[Point]) -> Polygon:
    '''
    method for generation convex polygon
    :param input_list:
    :return:
    '''
#     phase one
    m = 0
    right_point = sorted(input_list, key=get_y_coordinate)[0]
    # print(right_point)
    def _get_tan(point: Point) -> Tuple[float, float]:
        '''
        :param point: upon which calcutes tangens and Euclidean distance
        :return: order of sorting
        '''
        distance = euclidean_distance(right_point, point)
        if point.y == right_point.y:
            tan = -inf
        else:
            tan =  (point.x - right_point.x) / (point.y - right_point.y)
        return (tan, distance)

    input_list = sorted(input_list, key=_get_tan)
    # print(input_list)
    # phase two
    s = Stack()
    s.push(input_list[0])
    s.push(input_list[1])
    s.push(input_list[2])
    # i = 2
    # print(s.size())
    print(input_list)
    for i in range(3, len(input_list)):
        to_top = next_to_top(s)
        print('i: ',i)
        print('peek: ', s.peek(),'  to top',to_top, ' [i]', input_list[i],' ccw', ccw(s.peek(),to_top, input_list[i]), '\n')
        while ccw(to_top,s.peek(), input_list[i]) > 0:
            print('pop')
            s.pop()
        s.push(input_list[i])
    # s.push(input_list[0])
    input_list = stack_to_list(s)
    return Polygon(input_list)

s1 = Segment(Point(0,0), Point(100, 0))
s2 = Segment(Point(50, 0), Point(50, 10))
# print(segments_intersect(s1, s2))
pol = Polygon([Point(0,0), Point(100, 0), Point(50,-30), Point(100, 0)])
# pol.draw()
print(ccw(Point(0, 0), Point(50, 0), Point(100, 0)), ' ' , ccw(Point(0, 0), Point(-50, 0), Point(100, 0)))

input_points = [Point(0,0),
                    Point(200, 100),
                    Point(0, 100),
                    Point(200, 0),
                    Point(50, 30),
                    Point(100, 100),
                    Point(100, 0),
                    Point(30, 50),
                Point(-50, 50),
                Point(10,210)]
p = Polygon(get_simple_polygon(input_points))
# p.draw()
# q = graham_scan(input_points)
# q.draw()

p1 = Point(0, 0)
p2 = Point(100, 0)
p3 = Point(50, -30)
p = Polygon([p1, p2, p3])
# print(ccw(p1, p2, p3))
# p.draw()
