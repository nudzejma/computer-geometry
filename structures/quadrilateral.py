from structures.point import Point
from structures.polygon import Polygon


class Quadrilateral(Polygon):
    def __init__(self, first: Point, second: Point, third: Point, fourth: Point):
        super().__init__([first, second, third, fourth])
        self.first = first
        self.second = second
        self.third = third
        self.fourth = fourth