class Faculty:
    def __init__(self, id, name, shortname):
        self.id = id
        self.name = name
        self.shortname = shortname

    @classmethod
    def from_row(cls, row):
        return cls(*row)

    @staticmethod
    def initiate(cursor):
        cursor.execute('''DROP TABLE IF EXISTS faculties CASCADE;
            CREATE TABLE faculties (
            ID SERIAL PRIMARY KEY NOT NULL,
            NAME text NOT NULL,
            SHORTNAME text NOT NULL)''')
        
    @staticmethod
    def create(cursor, name, shortname):
        cursor.execute(
            "INSERT INTO faculties (name, shortname) "
            "VALUES (%s, %s) RETURNING id",
            (name, shortname)
        )
        return cursor.fetchone()[0]

    @staticmethod
    def get_all(cursor):
        cursor.execute(
            "SELECT id, name, shortname "
            "FROM faculties"
        )
        return [Faculty.from_row(row) for row in cursor.fetchall()]

    @staticmethod
    def get_by_id(cursor, faculty_id):
        cursor.execute(
            "SELECT id, name, shortname "
            "FROM faculties "
            "WHERE id = %s",
            (faculty_id,)
        )
        return Faculty.from_row(cursor.fetchone())

    @staticmethod
    def get_by_name(cursor, name):
        cursor.execute(
            "SELECT id, name, shortname "
            "FROM faculties "
            "WHERE name = %s",
            (name,)
        )
        return Faculty.from_row(cursor.fetchone())

    @staticmethod
    def update_name(cursor, faculty_id, new_name):
        cursor.execute(
            "UPDATE faculties "
            "SET name = %s "
            "WHERE id = %s",
            (new_name, faculty_id)
        )

    @staticmethod
    def update_shortname(cursor, faculty_id, new_shortname):
        cursor.execute(
            "UPDATE faculties "
            "SET shortname = %s "
            "WHERE id = %s",
            (new_shortname, faculty_id)
        )

    @staticmethod
    def delete(cursor, faculty_id):
        cursor.execute(
            "DELETE FROM faculties "
            "WHERE id = %s",
            (faculty_id,)
        )
