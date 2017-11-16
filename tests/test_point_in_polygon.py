import sys, os
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')

from modules.primitives import point_in_polygon, get_simple_polygon
from structures.point import Point
from structures.polygon import Polygon


def test_point_in_polygon() -> None:
    inspect_point1 = Point(-30, 50)
    inspect_point2 = Point(100, 110)
    inspect_point3 = Point(-50, 100)
    inspect_point4 = Point(-50, 220)
    inspect_point5 = Point(-100, 150)
    p = Polygon(get_simple_polygon([Point(0, 0),
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
                                    Point(10, 210)]))
    assert point_in_polygon(p, inspect_point1) == True
    assert point_in_polygon(p, inspect_point2) == True
    assert point_in_polygon(p, inspect_point3) == True
    assert point_in_polygon(p, inspect_point4) == False
    assert point_in_polygon(p, inspect_point5) == False
