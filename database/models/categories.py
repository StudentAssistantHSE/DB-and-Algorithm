class Category:
    def __init__(self, id, category, is_custom):
        self.id = id
        self.category = category
        self.is_custom = is_custom

    @classmethod
    def from_row(cls, row):
        return cls(*row)

    @staticmethod
    def initiate(cursor):
        cursor.execute(''' DROP TABLE IF EXISTS categories CASCADE;
            CREATE TABLE categories (
            ID SERIAL PRIMARY KEY NOT NULL,
            CATEGORY text NOT NULL UNIQUE,
            IS_CUSTOM BOOLEAN)''')

    @staticmethod
    def create(cursor, category, is_custom):
        cursor.execute(
            "INSERT INTO categories (category, is_custom) "
            "VALUES (%s, %s) RETURNING id",
            (category, is_custom)
        )
        return cursor.fetchone()[0]

    @staticmethod
    def get_all(cursor):
        cursor.execute(
            "SELECT id, category, is_custom "
            "FROM categories"
        )
        return [Category.from_row(row) for row in cursor.fetchall()]

    @staticmethod
    def get_by_id(cursor, category_id):
        cursor.execute(
            "SELECT id, category, is_custom "
            "FROM categories "
            "WHERE id = %s",
            (category_id,)
        )
        return Category.from_row(cursor.fetchone())

    @staticmethod
    def get_by_category(cursor, category):
        cursor.execute(
            "SELECT id, category, is_custom "
            "FROM categories "
            "WHERE category = %s",
            (category,)
        )
        return Category.from_row(cursor.fetchone())

    @staticmethod
    def update_category(cursor, category_id, new_category):
        cursor.execute(
            "UPDATE categories "
            "SET category = %s "
            "WHERE id = %s",
            (new_category, category_id)
        )

    @staticmethod
    def delete(cursor, category_id):
        cursor.execute(
            "DELETE FROM categories "
            "WHERE id = %s",
            (category_id,)
        )

    @staticmethod
    def get_all_categories(cursor):
        cursor.execute('Select category from categories')
        return cursor.fetchall()