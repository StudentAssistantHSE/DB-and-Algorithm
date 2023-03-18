import psycopg2
from database.models.projects import Project


class ProjectController:
    def __init__(self, cursor):
        self.cursor = cursor

    def initiate_creation(self):
        return Project.initiate(self.cursor)

    def get_all_projects(self):
        return Project.get_all(self.cursor)

    def get_id_non_closed(self):
        return Project.get_id_of_not_closed(self.cursor)


