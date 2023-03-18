import psycopg2.extras


class UserCategory:
    def __init__(self):
        self.user_id = None
        self.category_id = None

    @classmethod
    def from_row(cls, row):
        return cls(*row)

    @staticmethod
    def initiate(cursor):
        cursor.execute(''' DROP TABLE IF EXISTS user_categories CASCADE;
            CREATE TABLE user_categories (
            user_id int NOT NULL,
            category_id int NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id) ON UPDATE CASCADE,
            FOREIGN KEY (category_id) REFERENCES categories(id) ON UPDATE CASCADE,
            PRIMARY KEY (user_id, category_id)); ''')

    @staticmethod
    def create(self, cursor, user_id, category_id):
        cursor.execute(
            """
            INSERT INTO user_categories (user_id, category_id)
            VALUES (%s, %s)
            RETURNING user_id, category_id
            """,
            (user_id, category_id)
        )
        row = cursor.fetchone()
        self.user_id = row[0]
        self.category_id = row[1]

    @staticmethod
    def get_all(self, cursor):
        cursor.execute(
            """
            SELECT * FROM user_categories
            """
        )
        rows = cursor.fetchall()
        return [dict(row) for row in rows]

    @staticmethod
    def update(self, cursor, user_id, category_id):
        cursor.execute(
            """
            UPDATE user_categories
            SET category_id = %s
            WHERE user_id = %s
            """,
            (category_id, user_id)
        )
        self.user_id = user_id
        self.category_id = category_id

    @staticmethod
    def delete(self, cursor):
        cursor.execute(
            """
            DELETE FROM user_categories WHERE user_id = %s
            """,
            (self.user_id,)
        )
        self.user_id = None
        self.category_id = None
