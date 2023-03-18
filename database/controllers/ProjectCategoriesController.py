import psycopg2
from database.models.project_categories import ProjectCategory


class ProjectCategoriesController:
    def __init__(self, cursor):
        self.cursor = cursor

    def initiate_creation(self):
        return ProjectCategory.initiate(self.cursor)

    def get_all(self):
        project_categories = ProjectCategory.get_all(self.cursor)
        return project_categories

    def get_by_project(self, project_id):
        return ProjectCategory.get_by_project(self.cursor, project_id)

    def get_by_category(self, category_id):
        return ProjectCategory.get_by_category(self.cursor, category_id)


