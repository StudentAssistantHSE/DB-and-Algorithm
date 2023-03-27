class Project:
    def __init__(self, id, name, description, contacts, created_date, updated_date, start_date, end_date, creator_user_id, is_closed):
        self.id = id
        self.name = name
        self.description = description
        self.contacts = contacts
        self.created_date = created_date
        self.updated_date = updated_date
        self.start_date = start_date
        self.end_date = end_date
        self.creator_user_id = creator_user_id
        self.is_closed = is_closed

    @classmethod
    def from_row(cls, row):
        return cls(*row)

    @staticmethod
    def initiate(cursor):
        cursor.execute(''' DROP TABLE IF EXISTS projects CASCADE;
            CREATE TABLE projects (
            ID SERIAL PRIMARY KEY NOT NULL,
            NAME text NOT NULL,
            DESCRIPTION text NOT NULL,
            CONTACTS text,
            CREATED_DATE DATE NOT NULL DEFAULT CURRENT_DATE,
            APPLICATION_DEADLINE DATE,
            UPDATED_DATE DATE,
            START_DATE DATE,
            END_DATE DATE,
            CREATOR_USER_ID BIGINT REFERENCES users,
            IS_CLOSED BOOLEAN,
            EMPLOYMENT_TYPE BIGINT,
            TERRITORY text,
            SKILLS text,
            CREDIT_NUMBER BIGINT,
            CAMPUS BIGINT,
            PARTICIPANTS_NUMBER BIGINT,
            PROJECT_TYPE BIGINT,
            WEEKLY_HOURS BIGINT)''')

    @staticmethod
    def create(cursor, name, description, contacts, start_date=None, end_date=None, creator_user_id=None):
        cursor.execute(
            "INSERT INTO projects (name, description, contacts, start_date, end_date, creator_user_id) "
            "VALUES (%s, %s, %s, %s, %s, %s) RETURNING id",
            (name, description, contacts, start_date, end_date, creator_user_id)
        )
        return cursor.fetchone()[0]

    @staticmethod
    def get_all(cursor):
        cursor.execute(
            "SELECT id, name, description, contacts, created_date, updated_date, start_date, end_date, creator_user_id, is_closed "
            "FROM projects"
        )
        return [Project.from_row(row) for row in cursor.fetchall()]

    @staticmethod
    def get_by_id(cursor, project_id):
        cursor.execute(
            "SELECT id, name, description, contacts, created_date, updated_date, start_date, end_date, creator_user_id, is_closed "
            "FROM projects "
            "WHERE id = %s",
            (project_id,)
        )
        return Project.from_row(cursor.fetchone())

    @staticmethod
    def update(cursor, project_id, name=None, description=None, contacts=None, start_date=None, end_date=None, creator_user_id=None, is_closed=None):
        set_clause = []
        if name is not None:
            set_clause.append("name = %s")
        if description is not None:
            set_clause.append("description = %s")
        if contacts is not None:
            set_clause.append("contacts = %s")
        if start_date is not None:
            set_clause.append("start_date = %s")
        if end_date is not None:
            set_clause.append("end_date = %s")
        if creator_user_id is not None:
            set_clause.append("creator_user_id = %s")
        if is_closed is not None:
            set_clause.append("is_closed = %s")

        if not set_clause:
            return

        set_clause = ", ".join(set_clause)

        cursor.execute(
            f"UPDATE projects SET {set_clause} WHERE id = %s",
            (name, description, contacts, start_date, end_date, creator_user_id, is_closed, project_id)
        )

    @staticmethod
    def delete(cursor, project_id):
        cursor.execute(
            "DELETE FROM projects "
            "WHERE id = %s",
            (project_id,)
        )

    @staticmethod
    def get_id_of_not_closed(cursor):
        cursor.execute('Select ID from projects where is_closed = false')
        return cursor.fetchall()
