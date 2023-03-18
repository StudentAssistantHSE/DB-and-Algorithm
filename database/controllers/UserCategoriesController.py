import psycopg2
from database.models.user_categories import UserCategory


class UserCategoriesController:
    def __init__(self, cursor):
        self.cursor = cursor

    def initiate_creation(self):
        return UserCategory.initiate(self.cursor)

    def get_all_user_categories(self):
        return UserCategory.get_all(self.cursor)


