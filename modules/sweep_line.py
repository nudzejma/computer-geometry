import turtle
from collections import deque
from typing import List, Tuple

from modules.primitives import ccw
from structures.line_segment import Segment
from structures.point import Point


def do_segments_intersects(s1: Segment, s2: Segment) -> bool:
    if s1.first == s2.first or s1.first == s2.second:
        return False

    if s1.second == s2.first or s1.second == s2.second:
        return False

    o1 = ccw(s1.first, s1.second, s2.first)
    o2 = ccw(s1.first, s1.second, s2.second)
    o3 = ccw(s2.first, s2.second, s1.first)
    o4 = ccw(s2.first, s2.second, s1.second)

    return o1 != o2 and o3 != o4


class LabeledSegmentPoint():
    def __init__(self, x: int, y: int, belong_segment: Segment, label: str, is_left: bool):
        self.x = x
        self.y = y
        self.belong_segment = belong_segment
        self.label = label
        self.is_left = is_left


def _get_x_coordinate(point: LabeledSegmentPoint) -> Tuple:

    return point.x, -point.y


def any_intersection(segments: List[Segment]) -> bool:
    '''

    Args:
        segments:

    Returns:

    '''

    list_of_points = []
    dict_of_segments = {}
    for i, segment in enumerate(segments):
        list_of_points.append(
            LabeledSegmentPoint(segment.first.x, segment.first.y, segment, 'A' + str(i), segment.first.x <= segment.second.x))
        list_of_points.append(
            LabeledSegmentPoint(segment.second.x, segment.second.y, segment, 'A' + str(i), segment.first.x > segment.second.x))
        dict_of_segments['A' + str(i)] = segment

    list_of_points = sorted(list_of_points, key=_get_x_coordinate)

    labels_deque = deque()
    current = 0
    for i, point in enumerate(list_of_points):
        # l = list_of_points[i].label
        if point.is_left:
            labels_deque.insert(current, point.label)

            try:
                if do_segments_intersects(dict_of_segments[point.label], dict_of_segments[labels_deque[current+1]]):
                    # dict_of_segments[point.label].draw(turtle, "pink")
                    # turtle.up()
                    # dict_of_segments[labels_deque[current + 1]].draw(turtle, "pink")
                    # turtle.up()
                    print('any_intersection1: true', dict_of_segments[point.label].first, dict_of_segments[point.label].second, dict_of_segments[labels_deque[current+1]].first, dict_of_segments[labels_deque[current+1]].second)
                    return True

                if do_segments_intersects(dict_of_segments[point.label], dict_of_segments[labels_deque[current-1]]):
                    print('any_intersection2: true')
                    return True
            except IndexError:
                continue
            current += 1
        else:
            current = labels_deque.index(point.label)
            try:
                if do_segments_intersects(dict_of_segments[labels_deque[current-1]], dict_of_segments[labels_deque[current+1]]):
                    print('any_intersection3: true')
                    return True
                labels_deque.remove(point.label)

            except IndexError:
                continue
    print('any_intersection4: false')
    return False


# point_x_first = Point(0, 0)
# point_y_first = Point(0, 100)
#
# point_x_second = Point(15, 10)
# point_y_second = Point(15, -20)
# s1 = Segment(Point(x=-40, y=-95), Point(0, 0))
# s1.draw(turtle, "green")
# turtle.up()
# s2 = Segment(Point(x=-100, y=-50), Point(x=-80, y=45))
# s2.draw(turtle, "red")
# turtle.up()
# s3 = Segment(Point(x=-100, y=-50), Point(x=0, y=0))
# s3.draw(turtle, "yellow")
# turtle.up()
# s4 = Segment(Point(x=-40, y=-95), Point(x=-80, y=45))
# s4.draw(turtle, "yellow")
# turtle.up()
# print(any_intersection([s1, s2, s3, s4]))
# turtle.done()

# se = [Segment(Point(x=-100, y=-50), Point(x=-80, y=45)), Segment(Point(x=-100, y=-50), Point(x=-40, y=-95)), Segment(Point(x=-80, y=45), Point(x=-40, y=-95)),
#       Segment(Point(x=0, y=0), Point(x=-80, y=45)), Segment(Point(x=0, y=0), Point(x=-40, y=-95)), Segment(Point(x=0, y=0), Point(x=30, y=100)),
#       Segment(Point(x=-40, y=-95), Point(x=30, y=100))]
# print(any_intersection(se))
# for segments in se:
#     segments.draw(turtle, "red")
# turtle.done()