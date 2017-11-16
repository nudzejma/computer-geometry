import sys, os

from modules.primitives import point_in_triangle
from structures.point import Point

myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')

def test_point_in_triangle() -> None:
    inspect_point1 = Point(0, 0)
    inspect_point2 = Point(30, 30)
    inspect_point3 = Point(30, 0)
    inspect_point4 = Point(200, 0)
    inspect_point5 = Point(200, 150)
    assert point_in_triangle(Point(0,0), Point(100, 0), Point(50, 100), inspect_point1) == True
    assert point_in_triangle(Point(0, 0), Point(100, 0), Point(50, 100), inspect_point2) == True
    assert point_in_triangle(Point(0, 0), Point(100, 0), Point(50, 100), inspect_point3) == True
    assert point_in_triangle(Point(0, 0), Point(100, 0), Point(50, 100), inspect_point4) == False
    assert point_in_triangle(Point(0, 0), Point(100, 0), Point(50, 100), inspect_point5) == False