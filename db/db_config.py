"""
Contains configuration for database access.
"""

DRIVER = "postgresql+psycopg2"
USER = "postgres"
PASS = "admin"
HOST = "localhost:5432"
DB_NAME = "db_triangulations"

DB_URI = "{}://{}:{}@{}/{}".format(DRIVER, USER, PASS, HOST, DB_NAME)