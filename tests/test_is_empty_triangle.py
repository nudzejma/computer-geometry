import sys, os

from modules.primitives import is_triangle_empty
from structures.point import Point
from structures.triangle import Triangle

myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')

def test_is_empty_triangle() -> None:
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
    t1 = Triangle(Point(-100, 0), Point(-60, 0), Point(-70, 150))
    t2 = Triangle(Point(0, 0), Point(100, 0), Point(50, 150))

    assert is_triangle_empty(input_list, t1) == True
    assert is_triangle_empty(input_list, t2) == False
