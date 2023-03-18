import psycopg2
from database.models.categories import Category

class CategoryController:
    def __init__(self, cursor):
        self.cursor = cursor

    def initiate_creation(self):
        return Category.initiate(self.cursor)

    def get_all_categories(self):
        categories = Category.get_all_categories(self.cursor)
        return categories

    def create_category(self, category, is_custom):
        Category.create(self.cursor, category, is_custom)
        self.cursor.connection.commit()

