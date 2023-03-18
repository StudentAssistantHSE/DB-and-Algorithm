import psycopg2.extras

class Status:
    def __init__(self, id, status):
        self.id = id
        self.status = status

    @classmethod
    def from_row(cls, row):
        return cls(*row)

    @staticmethod
    def initiate(cursor):
        cursor.execute(''' DROP TABLE IF EXISTS statuses CASCADE;
            CREATE TABLE statuses (
            ID SERIAL PRIMARY KEY NOT NULL,
            STATUS text NOT NULL UNIQUE)''')
        cursor.execute(''' INSERT INTO statuses (STATUS)
            VALUES('SENT'), ('REJECTED'), ('ACCEPTED');''')

    @staticmethod
    def create(self, cursor,  status):
        cursor.execute(
            """
            INSERT INTO statuses (status)
            VALUES (%s)
            RETURNING id
            """,
            (status,)
        )
        row = cursor.fetchone()
        self.id = row[0]
        self.status = status

    @staticmethod
    def get_all(self, cursor):
        cursor.execute(
            """
            SELECT * FROM statuses
            """
        )
        rows = cursor.fetchall()
        return [dict(row) for row in rows]

    def update(self, status):
        cursor = self.connection.cursor()
        cursor.execute(
            """
            UPDATE statuses
            SET status = %s
            WHERE id = %s
            """,
            (status, self.id)
        )
        self.status = status

    @staticmethod
    def delete(self):
        cursor = self.connection.cursor()
        cursor.execute(
            """
            DELETE FROM statuses WHERE id = %s
            """,
            (self.id,)
        )
        self.id = None
        self.status = None
