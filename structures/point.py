'''
    Class Point in 2D
'''
import turtle
from collections import namedtuple

import math

# turtle.ht()

class Point(namedtuple('Point', ['x', 'y'])):
    def __eq__(self, other):
        return (self.x == other.x) and (self.y == other.y)
    def draw(self, forbbid_drop = False):
        if not forbbid_drop:
            turtle.up()
        turtle.setpos(self.x, self.y)
        turtle.down()
        turtle.dot()
    def euclidean_distance(self, other_point:'Point'):
        return math.sqrt((other_point.x - self.x) ** 2 + (other_point.y - self.y) ** 2)
# point = Point(x=100, y=100)
# p2 = Point(x=101, y=100)
# print(point == p2)
# point.draw(True)
# turtle.done()