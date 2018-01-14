import turtle
from random import randint
from typing import List, Tuple
from anytree.dotexport import RenderTreeGraph

from anytree import Node, RenderTree, PreOrderIter

from structures.line_segment import Segment
from structures.point import Point
from structures.polygon import Polygon

class Triangulation:
    def __init__(self, diagonals: List[Tuple[int, int]]):
        self.diagonals = diagonals

    def add_diagonal(self, diagonal: Tuple[int, int]) -> None:
        self.diagonals.append(diagonal)

    def transform_diagonal(self, old_diagonal: Tuple[int, int], new_diagonal: Tuple[int, int]) -> None:
        for i, diag in enumerate(self.diagonals):
            if (diag[0] == old_diagonal[0] and diag[1] == old_diagonal[1]):
                self.diagonals[i] = new_diagonal
                break


def sort(element: Tuple[int, int]) -> Tuple[int,int]:
    '''
    :param element: point element coordinates we use
    :return: order of sorting
    '''
    return (element[0], element[1])

def triangulate_recursive(root_triangulation, triangulation: Triangulation, current_n: int, end_n: int) -> Node:

    diagonals_list = triangulation.diagonals
    if (diagonals_list[len(diagonals_list)-1] == [end_n-1,end_n]):
        node = Node('triangulation'+str(current_n), parent=root_triangulation, triangulation=triangulation.diagonals)
        return node

    for i, diagonal in enumerate(diagonals_list):

        if diagonal[1] == current_n:

            new_diagonal_list = list(triangulation.diagonals)
            new_triangulation = Triangulation(new_diagonal_list)

            for previous_diag in diagonals_list[(i-1)::-1]:

                if previous_diag[1] == current_n:

                    new_triangulation.transform_diagonal(previous_diag, [previous_diag[0], current_n + 1])

            new_triangulation.transform_diagonal(diagonal, [diagonal[0], diagonal[1]])
            new_triangulation.add_diagonal([diagonal[0],current_n + 1])
            new_triangulation.add_diagonal([current_n, current_n + 1])
            new_triangulation.diagonals = sorted(new_triangulation.diagonals, key=sort)

            triangulation.transform_diagonal(diagonal, [diagonal[0], diagonal[1]])
            triangulation.diagonals = sorted(triangulation.diagonals, key=sort)

            root_string = 'root' + str(diagonal[0]) + '_' + str(current_n)
            new_root_triangulation = Node(root_string,parent=root_triangulation, triangulation=triangulation.diagonals)
            triangulate_recursive(new_root_triangulation, new_triangulation,(current_n+1), end_n)

    if len(diagonals_list) == 3:
         return root_triangulation



def triangulate(convex_polygon: Polygon):
    diagonal_list = []
    diagonal_list.append([1, 2])
    diagonal_list.append([1, 3])
    diagonal_list.append([2, 3])
    t = Triangulation(diagonal_list)
    current_n = 3
    root_triangulation = Node('root', triangulation=t.diagonals)
    node = triangulate_recursive(root_triangulation, t, current_n, len(convex_polygon.points))
    # print(RenderTree(node))


    polygons_segments = []
    for node1 in PreOrderIter(node):
        if node1.is_leaf:
            node_triangulation = node1.triangulation
            print(node_triangulation)
            input_list = []
            list_of_segments = []
            for pair in node_triangulation:

                s = Segment(convex_polygon.points[pair[0]-1], convex_polygon.points[pair[1]-1])
                list_of_segments.append(s)

            polygons_segments.append(list_of_segments)

    for segments in polygons_segments[18]:
        segments.draw(turtle, "red")
    turtle.done()


# n = 6
# input_x_list = [randint(-200,200) for _ in range(0,n)]
# input_y_list = [randint(-200, 200) for _ in range(0, n)]
# for i in range(n):
#     input_list.append(Point(input_x_list[i], input_y_list[i]))
input_list = [Point(0, 0), Point(100, 0), Point(200, 100), Point(250, 150),  Point(100, 200), Point(0, 200), Point(-70, 150), Point(-100, 100)]
q = Polygon(input_list)
# q.draw(turtle, "red")
triangulate(q)