'''

This module represents implementaion of Hurtado Noy algorithm for
calculating all triangulations of convex polygon - optimized

'''

import turtle
from collections import deque
from random import randint
from time import time
from typing import List, Tuple, Deque
# from anytree.dotexport import RenderTreeGraph
import copy

import itertools
from anytree import Node, RenderTree, PreOrderIter
from anytree.exporter import DotExporter

from modules.primitives import graham_scan
from sorting_algorithms.benchmark import benchmark
from structures.line_segment import Segment
from structures.point import Point
from structures.polygon import Polygon

# def convert_to_list(s: str):
#     return_list = []
#     s = s[1:len(s) - 1]
#     items_list = s.split('],');
#
#     for item in items_list:
#         if item[0] == ' ':
#             item = item[2:]
#         else:
#             item = item[1:]
#
#         if item[len(item) - 1] == ']':
#             item = item[:-1]
#
#         new_tuple =item.split(', ')
#
#         return_list.append([int(new_tuple[0]), int(new_tuple[1])])
#
#     return return_list


def triangulate_recursive(root_triangulation, current_n: int, end_n: int) -> None:
    '''

    This function represents recursively called function for calculating and creating
    a tree of triangulations
    Args:
        root_triangulation: root node of coming child triangulations
        current_n: current number of points
        end_n: length of convex polygon triangulations are finding for

    Returns: None

    '''

    pairs_list = root_triangulation.triangulation

    for i, pair in enumerate(pairs_list):

        if pair[1] == current_n:

            list_of_child = list(pairs_list)

            for j, previous_pair in enumerate(list_of_child[(i-1)::-1]):
                if previous_pair[1] == current_n:

                    pp = previous_pair
                    list_of_child.remove(previous_pair)
                    list_of_child.insert(i-j-1,[pp[0], pp[1]+1])

            list_of_child.insert(i+1, [pair[0], current_n + 1])
            list_of_child.append([current_n, current_n + 1])

            new_child = Node('Child_' + str(pair[0]) + '_' + str(pair[1]), parent=root_triangulation, triangulation=list_of_child)
            if ([current_n, current_n+1] == [end_n - 1, end_n]):

               continue

            triangulate_recursive(new_child, current_n+1, end_n)

def triangulate(convex_polygon: Polygon):
    '''

    This function finds triangulations of convex polygon
    Args:
        convex_polygon: input polygon

    Returns: number od triangulations

    '''
    diagonal_list = []
    diagonal_list.append([1, 2])
    diagonal_list.append([1, 3])
    diagonal_list.append([2, 3])
    current_n = 3
    root_triangulation = Node('root', triangulation=diagonal_list)
    fm = time()
    triangulate_recursive(root_triangulation, current_n, len(convex_polygon.points))
    sm = time()
    print('{}s'.format(sm - fm))
    print(RenderTree(root_triangulation))

    polygons_segments = []
    for node1 in PreOrderIter(root_triangulation):
        if node1.is_leaf:
            node_triangulation = node1.triangulation
            list_of_segments = []
            for pair in node_triangulation:

                s = Segment(convex_polygon.points[pair[0]-1], convex_polygon.points[pair[1]-1])
                list_of_segments.append(s)

            polygons_segments.append(list_of_segments)
    # for segments in polygons_segments[23]:
    #     segments.draw(turtle, "red")
    # turtle.done()
    return len(polygons_segments)

def hurtado_noy_benchmark(input_list: List) -> None:
    '''

    This function is used for benchmarking triangulate(polygon) function, writing times in file
    Args:
        input_list: input list of points of polygon

    Returns: None

        '''
    text_file = "hurtado_noy_benchmark_optimized.txt"
    f = open(text_file, 'a+')
    n = 4
    while n < 17:
        q = Polygon(input_list[:n])
        bench = benchmark(triangulate, q)
        f.write(str(len(q.points)) + ' ' + str(bench) + 's \n')
        n += 1

    f.close()

input_list = [
    Point(x=-170, y=70),
    Point(x=-160, y=40),
    Point(x=-130, y=-20),
    Point(x=-110, y=-50),
    Point(x=0, y=-100),
    Point(x=80, y=-100),
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
]
# hurtado_noy_benchmark(input_list)
q = Polygon(input_list)
# q.draw(turtle, "red")
# turtle.done()
print(triangulate(q))