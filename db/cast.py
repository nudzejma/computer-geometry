"""
Contains helper cast functions that convert objects from structures module to
their respective database counterparts.
"""

from typing import List

from structures.line_segment import Segment
from structures.point import Point
from structures.triangle import Triangle
from structures.polygon import Polygon

from db.models import Point as DBPoint
from db.models import Segment as DBSegment
from db.models import Triangle as DBTriangle
from db.models import Triangulation as DBTriangulation
from db.models import Polygon as DBPolygon


def cast_point(point: Point) -> DBPoint:
    """
    Makes models.Point from structures.Point

    Args:
        point: structures.Point object

    Returns: models.Point object
    """
    db_point = DBPoint()

    db_point.x = point.x
    db_point.y = point.y

    return db_point

def cast_segment(segment: Segment) -> DBSegment:
    """
    Makes models.Point from structures.Point

    Args:
        point: structures.Point object

    Returns: models.Point object
    """
    db_segment = DBSegment()

    db_segment.points.append(cast_point(segment.first))
    db_segment.points.append(cast_point(segment.second))

    return db_segment


def cast_triangle(triangle: Triangle) -> DBTriangle:
    """
    Makes models.Triangle from structures.Triangle. Uses cast_point for
    triangle point casting.

    Args:
        triangle: structures.Triangle object

    Returns: models.Triangle object
    """
    db_triangle = DBTriangle()

    db_triangle.points.append(cast_point(triangle.first))
    db_triangle.points.append(cast_point(triangle.second))
    db_triangle.points.append(cast_point(triangle.third))

    return db_triangle

def cast_triangulation(triangulation: List) -> DBTriangulation:
    """
    Makes models.Triangulation from list of structures.Triangle. Uses
    cast_triangle for triangle casting. For loop wrapper function.

    Args:
        triangulation: List of structures.Triangle objects

    Returns: models.Triangulation object
    """
    db_triangulation = DBTriangulation()

    for segment in triangulation:

        db_triangulation.segments.append(cast_segment(segment))

    return db_triangulation

# def cast_triangulation(triangulation: List[Triangle]) -> DBTriangulation:
#     """
#     Makes models.Triangulation from list of structures.Triangle. Uses
#     cast_triangle for triangle casting. For loop wrapper function.
#
#     Args:
#         triangulation: List of structures.Triangle objects
#
#     Returns: models.Triangulation object
#     """
#     db_triangulation = DBTriangulation()
#
#     for triangle in triangulation:
#         db_triangulation.triangles.append(cast_triangle(triangle))
#
#     return db_triangulation


def cast_polygon(polygon: Polygon) -> DBPolygon:
    """
    Makes models.Polygon from  structures.Polygon. Uses
    cast_point for point casting.

    Args:
        polygon: structures.Polygon object

    Returns: models.Polygon object.

    """
    db_polygon = DBPolygon()

    for point in polygon.points:
        db_polygon.points.append(cast_point(point))
    return db_polygon
