'''
Class Polygon
'''
from cmath import inf
from typing import List, Tuple
import turtle

from structures.line_segment import Segment
from structures.point import Point
# turtle.ht()

class Polygon:
    def __init__(self, points: List[Point]):
        self.points = points

    def draw(self):
        i = 0
        length = self.points.__len__()
        while(i < length):
            s = Segment(self.points[i], self.points[(i+1)%length])
            s.draw()
            i += 1
        # other way:
        # for i, _ in enumerate(self.points):
        #     s = Segment(self.points[i-1], self.points[i])
        #     s.draw()
        turtle.done()