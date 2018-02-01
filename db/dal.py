from typing import List

from db.cast import cast_polygon, cast_triangulation
from db.db_config import DB_URI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db.models import Polygon
from modules.hurtado_noy_optimized import triangulate
from structures.point import Point

from structures.polygon import Polygon as STPolygon
from structures.triangle import Triangle as STTriangle

engine = create_engine(DB_URI)


DBSession = sessionmaker(bind=engine)
session = DBSession()

def save_triangulations(db_session: DBSession, polygon: STPolygon,
                        triangulations: List[List]) -> Polygon:

    polygon = cast_polygon(polygon)

    for triangulation in triangulations:
        polygon.triangulations.append(cast_triangulation(triangulation))

    db_session.add(polygon)
    db_session.commit()
    return polygon

input_list = [
    Point(x=-170, y=70),
    Point(x=-160, y=40),
    Point(x=-130, y=-20),
    Point(x=-110, y=-50),
    Point(x=0, y=-100),
    Point(x=80, y=-100),
    # Point(x=140, y=-10),
    # Point(x=160, y=40),
    # Point(x=170, y=70),
    # Point(x=160, y=100),
    # Point(x=130, y=160),
    # Point(x=110, y=190),
    # Point(x=80, y=200),
    # Point(x=0, y=200),
    # Point(x=-110, y=190),
    # Point(x=-130, y=160),
    # Point(x=-160, y=100)
]

# q = STPolygon(input_list)
# s = save_triangulations(session, q, triangulate(q))
# print(s.points)