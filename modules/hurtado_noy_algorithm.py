import turtle
from random import randint
from time import time
from typing import List, Tuple
# from anytree.dotexport import RenderTreeGraph

from anytree import Node, RenderTree, PreOrderIter
from anytree.exporter import DotExporter
from modules.primitives import graham_scan, is_polygon_convex
from sorting_algorithms.benchmark import benchmark
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

            # new_triangulation.transform_diagonal(diagonal, [diagonal[0], diagonal[1]])
            new_triangulation.add_diagonal([diagonal[0],current_n + 1])
            new_triangulation.add_diagonal([current_n, current_n + 1])
            new_triangulation.diagonals = sorted(new_triangulation.diagonals, key=sort)

            # triangulation.transform_diagonal(diagonal, [diagonal[0], diagonal[1]])
            triangulation.diagonals = sorted(triangulation.diagonals, key=sort)

            root_string = 'root' + str(diagonal[0]) + '_' + str(current_n)
            new_root_triangulation = Node(root_string,parent=root_triangulation, triangulation=triangulation.diagonals)
            triangulate_recursive(new_root_triangulation, new_triangulation,(current_n+1), end_n)

    if len(diagonals_list) == 3:
         return root_triangulation



def triangulate(convex_polygon: Polygon):
    fm = time()
    diagonal_list = []
    diagonal_list.append([1, 2])
    diagonal_list.append([1, 3])
    diagonal_list.append([2, 3])
    t = Triangulation(diagonal_list)
    current_n = 3
    root_triangulation = Node('root', triangulation=t.diagonals)
    node = triangulate_recursive(root_triangulation, t, current_n, len(convex_polygon.points))
    # print(RenderTree(root_triangulation))
    # RenderTreeGraph(root_triangulation).to_picture("tree.png")
    # DotExporter(root_triangulation).to_dotfile("tree_pet.dot")
    # dot = Digraph(comment='The Round Table')

    polygons_segments = []
    for node1 in PreOrderIter(node):
        if node1.is_leaf:
            node_triangulation = node1.triangulation
            # print(node_triangulation)
            input_list = []
            list_of_segments = []
            for pair in node_triangulation:

                s = Segment(convex_polygon.points[pair[0]-1], convex_polygon.points[pair[1]-1])
                list_of_segments.append(s)

            polygons_segments.append(list_of_segments)
    sm = time()
    print('{}s'.format(sm - fm))
    return len(polygons_segments)
    # for segments in polygons_segments[41]:
    #     segments.draw(turtle, "red")
    # turtle.done()

def hurtado_noy_benchmark():
    text_file = "hurtado_noy_benchmark.txt"
    f = open(text_file, 'a+')
    n = 1000
    while n < 1001:
        input_x_list = [randint(-200,200) for _ in range(0,n)]
        input_y_list = [randint(-200, 200) for _ in range(0, n)]

        input_list = []

        for i in range(n):
            input_list.append(Point(input_x_list[i], input_y_list[i]))

        q = graham_scan(input_list)
        bench = benchmark(triangulate, q)
        f.write(str(len(q.points)) + ' ' + str(bench) + '\n')
        n += 1

    # f.write('writing')
    f.close()

# hurtado_noy_benchmark()
n = 6
# print(input_list)
# print(q.points)
# q.draw(turtle, "red")
# input_list = [Point(0, 0), Point(100, 0), Point(250, 150),  Point(100, 200), Point(0, 200), Point(-70, 150), Point(-100, 100)]
# input_list = [Point(0, 0), Point(100, 0), Point(100, 200), Point(50, 250), Point(0, 200)]
# input_list = [Point(0, 0), Point(100, 0), Point(150, 150), Point(100, 200), Point(0, 200), Point(-50, 150)]
# q = Polygon(input_list)
# triangulate(q)

# n = 6
# input_x_list = [randint(-200,200) for _ in range(0,n)]
# input_y_list = [randint(-200, 200) for _ in range(0, n)]
# while len(input_x_list) < n or len(input_y_list) < n:
#
#     input_x_list = [randint(-200, 200) for _ in range(0, n)]
#     input_y_list = [randint(-200, 200) for _ in range(0, n)]
# input_list = []
#
# for i in range(n):
#     input_list.append(Point(input_x_list[i], input_y_list[i]))
#
# q = graham_scan(input_list)
# print(q.points, 'triangulate', triangulate(q))
#
# p = 1
# for i in range(15, 29):
#     p *= i
#
# k = 1
# for j in range(2, 13):
#     k *= j
#
# print('')
# input_list = [Point(0, -100),
#               Point(80, -100),
#               Point(110, -50),
#               Point(130, -25),
#               Point(140, -10),
#               Point(160,40),
#               Point(170, 70),
#               Point(160, 100),
#               Point(140, 130),
#               Point(130, 160),
#               Point(110, 190),
#               Point(80, 200),
#               Point(0, 200),
#               Point(-110, 190),
#               Point(-130, 160),
#               Point(-140, 130),
#               Point(-160, 100),
#               Point(-170, 70),
#               Point(-160, 40),
#               Point(-140, 10),
#               Point(-130, -20),
#               Point(-110, -50)
#              ]
# input_list = [
#     Point(x=-170, y=70),
#     Point(x=-160, y=40),
#     Point(x=-130, y=-20),
#     Point(x=-110, y=-50),
#     Point(x=0, y=-100),
#     Point(x=80, y=-100),
#     Point(x=140, y=-10),
#     Point(x=160, y=40),
#     Point(x=170, y=70),
#     Point(x=160, y=100),
#     Point(x=130, y=160),
#     Point(x=110, y=190),
#     Point(x=80, y=200),
#     Point(x=0, y=200),
#     Point(x=-110, y=190),
#     Point(x=-130, y=160),
#     Point(x=-160, y=100)
# ]
# desetougao: time = 0.22129249572753906s, 1430 triangulations
input_list = [
    Point(x=-170, y=70),
    Point(x=-160, y=40),
    Point(x=-130, y=-20),
    Point(x=140, y=-10),
    Point(x=160, y=40),
    Point(x=170, y=70),
    Point(x=160, y=100),
    Point(x=130, y=160),
    Point(x=110, y=190),
    Point(x=-160, y=100)
]
#jedanaestougao: time=0.6800506114959717s; 4862 triangulations
input_list = [
    Point(x=-170, y=70),
    Point(x=-160, y=40),
    Point(x=-130, y=-20),
    Point(x=140, y=-10),
    Point(x=160, y=40),
    Point(x=170, y=70),
    Point(x=160, y=100),
    Point(x=130, y=160),
    Point(x=110, y=190),
    Point(x=-130, y=160),
    Point(x=-160, y=100)
]

#dvanaestougao: time=3.932284116744995s; 16796 triangulations
input_list = [
    Point(x=-170, y=70),
    Point(x=-160, y=40),
    Point(x=-130, y=-20),
    Point(x=140, y=-10),
    Point(x=160, y=40),
    Point(x=170, y=70),
    Point(x=160, y=100),
    Point(x=130, y=160),
    Point(x=110, y=190),
    Point(x=-110, y=190),
    Point(x=-130, y=160),
    Point(x=-160, y=100)
]
#13-go: time=15.5772545337677s; 58786 triangulations
input_list = [
    Point(x=-170, y=70),
    Point(x=-160, y=40),
    Point(x=-130, y=-20),
    Point(x=140, y=-10),
    Point(x=160, y=40),
    Point(x=170, y=70),
    Point(x=160, y=100),
    Point(x=130, y=160),
    Point(x=110, y=190),
    Point(x=0, y=200),
    Point(x=-110, y=190),
    Point(x=-130, y=160),
    Point(x=-160, y=100)
]
#14-go: time=62.755178689956665s; 208012 triangulations
input_list = [
    Point(x=-170, y=70),
    Point(x=-160, y=40),
    Point(x=-130, y=-20),
    # Point(x=-110, y=-50),
    # Point(x=0, y=-100),
    # Point(x=80, y=-100),
    Point(x=140, y=-10),
    Point(x=160, y=40),
    Point(x=170, y=70),
    Point(x=160, y=100),
    Point(x=130, y=160),
    Point(x=110, y=190),
    Point(x=80, y=200),
    Point(x=0, y=200),
    Point(x=-110, y=190),
    Point(x=-130, y=160),
    Point(x=-160, y=100)
]
#15-go: time=220.458731174469s; 742900 triangulations
input_list = [
    Point(x=-170, y=70),
    Point(x=-160, y=40),
    Point(x=-130, y=-20),
    # Point(x=-110, y=-50),
    Point(x=80, y=-100),
    Point(x=140, y=-10),
    Point(x=160, y=40),
    Point(x=170, y=70),
    Point(x=160, y=100),
    Point(x=130, y=160),
    Point(x=110, y=190),
    Point(x=80, y=200),
    Point(x=0, y=200),
    Point(x=-110, y=190),
    Point(x=-130, y=160),
    Point(x=-160, y=100)
]
# 16-go: time=?s; ?triangulations
input_list = [
    Point(x=-170, y=70),
    Point(x=-160, y=40),
    Point(x=-130, y=-20),
    # Point(x=-110, y=-50),
    Point(x=0, y=-100),
    Point(x=80, y=-100),
    Point(x=140, y=-10),
    Point(x=160, y=40),
    Point(x=170, y=70),
    Point(x=160, y=100),
    Point(x=130, y=160),
    Point(x=110, y=190),
    Point(x=80, y=200),
    Point(x=0, y=200),
    Point(x=-110, y=190),
    Point(x=-130, y=160),
    Point(x=-160, y=100)
]
q = Polygon(input_list)
# q = graham_scan(q.points)
# print(is_polygon_convex(q))
# q.draw(turtle, "red")
# turtle.done()
print(triangulate(q))