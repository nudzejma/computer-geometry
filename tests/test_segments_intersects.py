import sys, os

from modules.primitives import segments_intersect
from structures.line_segment import Segment
from structures.point import Point

myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')

def test_segments_intersects() -> None:
    s1 = Segment(Point(0,0), Point(100, 0))

    s2 = Segment(Point(50, -50), Point(50, 50))
    s3 = Segment(Point(-10, 10), Point(-10, 40))
    s4 = Segment(Point(0, 0), Point(100, 20))
    s5 = Segment(Point(30, 0), Point(50, 0))
    s6 = Segment(Point(0, 0), Point(100, 0))
    s7 = Segment(Point(30, 0), Point(50, 30))

    assert segments_intersect(s1, s2) == True
    assert segments_intersect(s1, s3) == False
    assert segments_intersect(s1, s4) == True
    assert segments_intersect(s1, s5) == True
    assert segments_intersect(s1, s6) == True
    assert segments_intersect(s1, s7) == True
