import sys, os
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')

from modules.primitives import get_simple_polygon, polygon_orientation, graham_scan
from structures.point import Point
from structures.polygon import Polygon


def test_polygon_orientation() -> None:
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
    assert polygon_orientation(Polygon(get_simple_polygon(input_list))) == -1
    assert polygon_orientation((graham_scan(input_list))) == 1
