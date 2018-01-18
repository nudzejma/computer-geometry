'''
Class Polygon
'''
from cmath import inf
from random import randint
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
    def draw(self, t, color):
        i = 0
        length = self.points.__len__()
        # t.color(color)
        while(i < length):
            s = Segment(self.points[i], self.points[(i+1)%length])
            s.draw(t,color)
            i += 1
        # other way:
        # for i, _ in enumerate(self.points):
        #     s = Segment(self.points[i-1], self.points[i])
        #     s.draw()
        # t.done()

# n = 18
# input_x_list = [randint(-200,200) for _ in range(0,n)]
# p = Polygon(input_x_list)
# p.degrees[3] = 3
# print(p.degrees)