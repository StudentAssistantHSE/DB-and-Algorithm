import psycopg2
from models.faculties import Faculty


class FacultyController:
    def __init__(self, cursor):
        self.cursor = cursor

    def initiate_creation(self):
        return Faculty.initiate(self.cursor)

    def get_all_faculties(self):
        faculties = Faculty.get_all(self.cursor)
        return faculties

