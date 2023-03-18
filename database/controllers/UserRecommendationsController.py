import psycopg2
from database.models.user_recommendations import UserRecommendation


class UserRecommendationsController:
    def __init__(self, cursor):
        self.cursor = cursor

    def initiate_creation(self):
        return UserRecommendation.initiate(self.cursor)

    def get_all_projects(self):
        return UserRecommendation.get_all(self.cursor)

    def insert_recommendations(self, user_id, project_id):
        UserRecommendation.insert_recommendations(self.cursor, user_id, project_id)


