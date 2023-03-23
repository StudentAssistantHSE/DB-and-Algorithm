import psycopg2
from models.users import User


class UsersController:
    def __init__(self, cursor):
        self.cursor = cursor

    def initiate_creation(self):
        return User.initiate(self.cursor)

    def get_all_projects(self):
        return User.get_all(self.cursor)

    def get_all_id_and_faculty(self):
        return User.get_all_id_and_faculty(self.cursor)

    def get_user_from_same_faculty(self, faculty_id):
        return User.get_user_from_same_faculty(self.cursor, faculty_id)

    def get_user_faculty(self, id):
        return User.get_user_faculty(self.cursor, id)


