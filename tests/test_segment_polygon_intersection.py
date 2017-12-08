import sys, os

myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')

from modules.primitives import get_simple_polygon, segment_polygon_intersection
from structures.line_segment import Segment
from structures.point import Point
from structures.polygon import Polygon

def test_segment_polygon_intersect() -> None:
    s1 = Segment(Point(50, 0), Point(50, 10))
    s2 = Segment(Point(50, 0), Point(50, 100))
    s3 = Segment(Point(50, 0), Point(50, 30))
    s4 = Segment(Point(150, 0), Point(170, 0))

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
    p = Polygon(get_simple_polygon(input_list))
    assert segment_polygon_intersection(p, s1) == False
    assert segment_polygon_intersection(p, s2) == True
    assert segment_polygon_intersection(p, s3) == True
    assert segment_polygon_intersection(p, s4) == True