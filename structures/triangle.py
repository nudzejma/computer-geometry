from structures.point import Point
from structures.polygon import Polygon


class Triangle(Polygon):
    def __init__(self, first: Point, second: Point, third: Point):
        super().__init__([first, second, third])
        self.first = first
        self.second = second
        self.third = third
