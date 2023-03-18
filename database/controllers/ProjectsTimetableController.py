import psycopg2
from database.models.projects_timetable import ProjectTimetable


class ProjectTimetableController:
    def __init__(self, cursor):
        self.cursor = cursor

    def initiate_creation(self):
        return ProjectTimetable.initiate(self.cursor)

    def get_all_project_timetables(self):
        return ProjectTimetable.get_all(self.cursor)


