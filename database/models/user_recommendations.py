import psycopg2

class UserRecommendation:
    def __init__(self, user_id, project_id, generated_date=None):
        self.user_id = user_id
        self.project_id = project_id
        self.generated_date = generated_date

    @classmethod
    def from_row(cls, row):
        return cls(*row)

    @staticmethod
    def initiate(cursor):
        cursor.execute(''' DROP TABLE IF EXISTS user_recommendations CASCADE;
            CREATE TABLE user_recommendations (
            ID SERIAL PRIMARY KEY NOT NULL,
            user_id int NOT NULL,
            project_id int NOT NULL,
            generated_date Date DEFAULT CURRENT_DATE,
            FOREIGN KEY (user_id) REFERENCES users(id) ON UPDATE CASCADE,
            FOREIGN KEY (project_id) REFERENCES projects(id) ON UPDATE CASCADE);''')

    @staticmethod
    def save(self, cursor):
        sql = '''INSERT INTO user_recommendations (user_id, project_id, generated_date)
                 VALUES (%s, %s, %s) RETURNING id'''
        values = (self.user_id, self.project_id, self.generated_date)
        cursor.execute(sql, values)
        self.id = cursor.fetchone()[0]

    @staticmethod
    def delete(self, cursor):
        sql = 'DELETE FROM user_recommendations WHERE id = %s'
        cursor.execute(sql, (self.id,))

    @staticmethod
    def get_by_id(cursor, recommendation_id):
        sql = 'SELECT * FROM user_recommendations WHERE id = %s'
        cursor.execute(sql, (recommendation_id,))
        row = cursor.fetchone()
        if row is None:
            return None
        else:
            return UserRecommendation(*row[1:], row[0])

    @staticmethod
    def get_by_user(cursor, user_id):
        sql = 'SELECT * FROM user_recommendations WHERE user_id = %s'
        cursor.execute(sql, (user_id,))
        rows = cursor.fetchall()
        return [UserRecommendation(*row[1:], row[0]) for row in rows]

    @staticmethod
    def get_by_project(cursor, project_id):
        sql = 'SELECT * FROM user_recommendations WHERE project_id = %s'
        cursor.execute(sql, (project_id,))
        rows = cursor.fetchall()
        return [UserRecommendation(*row[1:], row[0]) for row in rows]

    @staticmethod
    def insert_recommendations(cursor, user_id, project_id):
        cursor.execute('Insert into user_recommendations (user_id, project_id) values (%s, %s);', (user_id, project_id))
