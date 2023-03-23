import psycopg2
from models.statuses import Status


class StatusesController:
    def __init__(self, cursor):
        self.cursor = cursor

    def initiate_creation(self):
        return Status.initiate(self.cursor)

    def get_all_statuses(self):
        return Status.get_all(self.cursor)


