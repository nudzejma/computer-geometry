import sys, os

from modules.primitives import is_polygon_empty, is_polygon_convex
from structures.point import Point
from structures.polygon import Polygon
from structures.quadrilateral import Quadrilateral

myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')

def test_is_polygon_convex() -> None:
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

    q1 = Quadrilateral(Point(0, 0), Point(50, 50), Point(100, 0), Point(50, 100))
    q2 = Quadrilateral(Point(0, 0), Point(100, 0), Point(100, 100), Point(0, 100))
    q3 = Quadrilateral(Point(0, 0), Point(100, 100), Point(100, 0), Point(0, 100))
    pol = Polygon(input_list)
    assert is_polygon_convex(q1) == False
    assert is_polygon_convex(q2) == True
    assert is_polygon_convex(q3) == False
    assert is_polygon_convex(pol) == False
