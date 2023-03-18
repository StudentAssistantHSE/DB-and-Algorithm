import psycopg2.extras

class ProjectTimetable:
    def __init__(self, connection):
        self.connection = connection

    @classmethod
    def from_row(cls, row):
        return cls(*row)

    @staticmethod
    def initiate(cursor):
        cursor.execute(''' DROP TABLE IF EXISTS projects_timetable CASCADE;
            CREATE TABLE projects_timetable (
            ID SERIAL PRIMARY KEY NOT NULL,
            PROJECT_ID BIGINT REFERENCES PROJECTS,
            DEADLINE DATE NOT NULL,
            NAME text NOT NULL,
            DESCRIPTION text)''')

    @staticmethod
    def create(self, project_id, deadline, name, description=None):
        cursor = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute(
            """
            INSERT INTO projects_timetable (project_id, deadline, name, description)
            VALUES (%s, %s, %s, %s)
            RETURNING id
            """,
            (project_id, deadline, name, description)
        )
        row = cursor.fetchone()
        cursor.close()
        return row['id']

    @staticmethod
    def get_by_project_id(self, project_id):
        cursor = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute(
            """
            SELECT * FROM projects_timetable WHERE project_id = %s
            """,
            (project_id,)
        )
        rows = cursor.fetchall()
        cursor.close()
        return [dict(row) for row in rows]

    @staticmethod
    def update(self, id, project_id, deadline, name, description=None):
        cursor = self.connection.cursor()
        cursor.execute(
            """
            UPDATE projects_timetable
            SET project_id = %s, deadline = %s, name = %s, description = %s
            WHERE id = %s
            """,
            (project_id, deadline, name, description, id)
        )
        cursor.close()

    @staticmethod
    def delete(self, id):
        cursor = self.connection.cursor()
        cursor.execute(
            """
            DELETE FROM projects_timetable WHERE id = %s
            """,
            (id,)
        )
        cursor.close()
