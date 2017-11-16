import sys, os
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')
from random import random

from modules.primitives import graham_scan
from structures.point import Point
from structures.polygon import Polygon


def test_convex_polygon() -> None:
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
    assert graham_scan(input_list).points == [Point(10, 210),
                                                Point(200, 200),
                                                Point(200, 100),
                                                Point(200, 0),
                                                Point(100, 0),
                                                Point(0, 0),
                                                Point(-50, 10),
                                                Point(-50, 50),
                                                Point(-50, 210)]