import sys, os
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')

from modules.primitives import ccw
from structures.point import Point


def test_ccw() -> None:
    assert ccw(Point(0,0), Point(100,0), Point(50,100)) == 1
    assert ccw(Point(0, 0), Point(100, 0), Point(50, 0)) == 0
    assert ccw(Point(0, 0), Point(100, 0), Point(50, -100)) == -1