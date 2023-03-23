import psycopg2
from models.applications import Application

class ApplicationController:
    def __init__(self, cursor):
        self.cursor = cursor

    def initiate_creation(self):
        applications = Application.initiate(self.cursor)
        return applications

    def get_all_applications(self):
        applications = Application.get_all(self.cursor)
        return applications

    def get_application_by_id(self, application_id):
        application = Application.get_by_id(self.cursor, application_id)
        return application

    def create_application(self, project_id, applicant_id, message, status):
        application = Application(project_id=project_id, applicant_id=applicant_id, message=message, status=status)
        application.create(self.cursor)
        return application

    def update_application(self, application_id, **kwargs):
        application = Application.get_by_id(self.cursor, application_id)
        if application:
            application.update(self.cursor, **kwargs)
            return application
        else:
            return None

    def get_users_applications(self):
        return Application.get_users_applications(self.cursor)
