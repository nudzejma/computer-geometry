'''
This module represents sweep line algorithm implementation for specific use of sweep hull algorithm
'''
import turtle
from collections import deque
from typing import List, Tuple

from modules.primitives import ccw
from structures.line_segment import Segment
from structures.point import Point


def do_segments_intersects(s1: Segment, s2: Segment) -> bool:
    '''

    Args:
        s1: first segment
        s2: second segment

    Returns: True if segments intersects, otherwise False

    '''
    if s1.first == s2.first or s1.first == s2.second:

        return False

    if s1.second == s2.first or s1.second == s2.second:

        return False

    o1 = ccw(s1.first, s1.second, s2.first)
    o2 = ccw(s1.first, s1.second, s2.second)
    o3 = ccw(s2.first, s2.second, s1.first)
    o4 = ccw(s2.first, s2.second, s1.second)

    return o1 != o2 and o3 != o4


class LabeledSegmentPoint:
    def __init__(self, x: int, y: int, belong_segment: Segment, label: str, is_left: bool):
        self.x = x
        self.y = y
        self.belong_segment = belong_segment
        self.label = label
        self.is_left = is_left


def _get_x_coordinate(point: LabeledSegmentPoint) -> Tuple:
    '''

    Args:
        point: current inspect point

    Returns: order of sorting

    '''

    if point.belong_segment.first.x == point.x:

        return point.x, -point.y, point.belong_segment.second.x

    elif point.belong_segment.second.x == point.x:

        return point.x, -point.y, point.belong_segment.first.x

def any_intersection(segments: List[Segment]) -> bool:
        '''

        Args:
            segments: list of segments upon which determines whether there is intersection between them

        Returns: True if there is intersection, otherwise False

        '''

        list_of_points = []
        dict_of_segments = {}

        for i, segment in enumerate(segments):

            list_of_points.append(
                LabeledSegmentPoint(segment.first.x, segment.first.y, segment, 'A' + str(i), segment.first.x <= segment.second.x))
            list_of_points.append(
                LabeledSegmentPoint(segment.second.x, segment.second.y, segment, 'A' + str(i), segment.first.x > segment.second.x))
            dict_of_segments['A' + str(i)] = segment

        def _get_coordinates(label: str) -> Tuple:
            '''

            Args:
                label: label of segment

            Returns: order of sorting

            '''
            seg_points = [point for point in list_of_points if point.label == label]

            if seg_points[0].is_left:

                return seg_points[0].y, seg_points[1].y
            else:

                return seg_points[1].y, seg_points[0].y

        list_of_points = sorted(list_of_points, key=_get_x_coordinate)
        labels_deque = deque()

        for i, point in enumerate(list_of_points):

            if point.is_left:

                labels_deque.append(point.label)
                labels_deque = sorted(labels_deque, key=_get_coordinates)
                current = labels_deque.index(point.label)

                try:
                    successor = labels_deque[current+1]

                    if do_segments_intersects(dict_of_segments[point.label], dict_of_segments[successor]):

                        return True
                    else:
                        try:
                            predecessor = labels_deque[current - 1]

                            if do_segments_intersects(dict_of_segments[point.label], dict_of_segments[predecessor]):

                                return True
                        except IndexError:
                            continue

                except IndexError:
                    try:

                        predecessor = labels_deque[current-1]

                        if do_segments_intersects(dict_of_segments[point.label], dict_of_segments[predecessor]):

                            return True
                    except IndexError:
                        continue
                    continue

            else:
                current = labels_deque.index(point.label)
                try:

                    successor = labels_deque[current + 1]
                    predecessor = labels_deque[current - 1]
                    labels_deque.remove(point.label)

                    if do_segments_intersects(dict_of_segments[successor], dict_of_segments[predecessor]):

                        return True


                except IndexError:
                    labels_deque.remove(point.label)
                    continue

        return False

