'''
 Class Segment
'''
import turtle

from structures.point import Point

# turtle.ht()

class Segment:
    def __init__(self, first: Point, second: Point):
        self.first = first
        self.second = second
    def __eq__(self, other):
        return (self.first == other.first) and (self.second == other.second)
    def draw(self,t, color):
        self.first.draw(t, color)
        self.second.draw(t, color, True)

# p1 = Point(0,0)
# p2 = Point(100, -200)
# line_segment = Segment(p1, p2)
# line_segment1 = Segment(p1, p2)
# print(line_segment == line_segment1)
# line_segment.draw()
# turtle.done()