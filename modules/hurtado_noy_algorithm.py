'''

This module represents implementaion of Hurtado Noy algorithm for
calculating all triangulations of convex polygon

'''

import turtle
from random import randint
from time import time
from typing import List, Tuple
# from anytree.dotexport import RenderTreeGraph

from anytree import Node, RenderTree, PreOrderIter
from anytree.exporter import DotExporter

from sorting_algorithms.benchmark import benchmark
from structures.line_segment import Segment
from structures.point import Point
from structures.polygon import Polygon

class Triangulation:
    def __init__(self, diagonals: List[Tuple[int, int]]):
        self.diagonals = diagonals

    def add_diagonal(self, diagonal: Tuple[int, int]) -> None:
        self.diagonals.append(diagonal)

    def insert_diagonal_at(self,position: int, diagonal: Tuple[int, int]) -> None:
        self.diagonals.insert(position, diagonal)

    def transform_diagonal(self, old_diagonal: Tuple[int, int], new_diagonal: Tuple[int, int]) -> None:
        for i, diag in enumerate(self.diagonals):
            if (diag[0] == old_diagonal[0] and diag[1] == old_diagonal[1]):
                self.diagonals[i] = new_diagonal
                break

def triangulate_recursive(root_triangulation: Node, triangulation: Triangulation, current_n: int, end_n: int) -> None:
    '''

    This function recursively calculate and creates a tree of triangulations of convex polygon
    Args:
        root_triangulation: root node of recursively called new child
        triangulation: current calculated triangulation
        current_n: current n in recursion
        end_n: length of convex polygon

    Returns: for now nothing

    '''

    diagonals_list = triangulation.diagonals

    for i, diagonal in enumerate(diagonals_list):

        if diagonal[1] == current_n:

            new_diagonal_list = list(triangulation.diagonals)
            new_triangulation = Triangulation(new_diagonal_list)

            for previous_diag in diagonals_list[(i-1)::-1]:

                if previous_diag[1] == current_n:

                    new_triangulation.transform_diagonal(previous_diag, [previous_diag[0], current_n + 1])

            new_triangulation.insert_diagonal_at(i + 1, [diagonal[0], current_n + 1])
            new_triangulation.add_diagonal([current_n, current_n + 1])
            # new_triangulation.add_diagonal([diagonal[0],current_n + 1])
            # new_triangulation.diagonals = sorted(new_triangulation.diagonals, key=sort)
            # triangulation.diagonals = sorted(triangulation.diagonals, key=sort)

            root_string = 'root' + str(diagonal[0]) + '_' + str(current_n)
            new_root_triangulation = Node(root_string,parent=root_triangulation, triangulation=triangulation.diagonals)

            if ([current_n, current_n+1] == [end_n - 1, end_n]):

               continue

            triangulate_recursive(new_root_triangulation, new_triangulation,(current_n+1), end_n)


def triangulate(convex_polygon: Polygon) -> int:
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
    t = Triangulation(diagonal_list)
    current_n = 3
    root_triangulation = Node('root', triangulation=diagonal_list)
    fm = time()
    node = triangulate_recursive(root_triangulation, t, current_n, len(convex_polygon.points))
    sm = time()
    print('{}s'.format(sm - fm))
    print(RenderTree(root_triangulation))
    # RenderTreeGraph(root_triangulation).to_picture("tree.png")
    # DotExporter(root_triangulation).to_dotfile("tree_pet.dot")
    # dot = Digraph(comment='The Round Table')

    polygons_segments = []
    for node1 in PreOrderIter(root_triangulation):

        if node1.is_leaf:

            node_triangulation = (node1.triangulation)
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
    text_file = "hurtado_noy_benchmark.txt"
    f = open(text_file, 'a+')
    n = 4
    while n < 17:
        print('n: ', n)
        q = Polygon(input_list[:n])
        bench = benchmark(triangulate, q)
        f.write(str(len(q.points)) + ' ' + str(bench) + 's \n')
        n += 1

    # f.write('writing')
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
