import sys, os
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')

from modules.primitives import get_simple_polygon
from structures.point import Point
def test_simple_polygon() -> None:
    '''
    :return:
    '''
    input_points = [Point(0,0),
                    Point(200, 100),
                    Point(0, 100),
                    Point(200, 0),
                    Point(100, 100),
                    Point(100, 0)]
    assert get_simple_polygon(input_points) == [Point(0,100),
                                                Point(0, 0),
                                                Point(100, 0),
                                                Point(200, 0),
                                                Point(200, 100),
                                                Point(100, 100)]
