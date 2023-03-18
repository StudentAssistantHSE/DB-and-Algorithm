class Application:
    def __init__(self, id, project_id, applicant_id, created_date, message, status):
        self.id = id
        self.project_id = project_id
        self.applicant_id = applicant_id
        self.created_date = created_date
        self.message = message
        self.status = status

    @classmethod
    def from_row(cls, row):
        return cls(*row)

    @staticmethod
    def initiate(cursor):
        cursor.execute(''' DROP TABLE IF EXISTS applications CASCADE;
            CREATE TABLE applications (
            ID SERIAL NOT NULL,
            PROJECT_ID BIGINT REFERENCES PROJECTS,
            APPLICANT_ID BIGINT REFERENCES users,
            CREATED_DATE DATE NOT NULL DEFAULT CURRENT_DATE,
            MESSAGE text NOT NULL,
            STATUS BIGINT REFERENCES statuses,
            PRIMARY KEY (ID, PROJECT_ID, APPLICANT_ID))''')

    @staticmethod
    def create(cursor, project_id, applicant_id, message, status):
        cursor.execute(
            "INSERT INTO applications (project_id, applicant_id, message, status) "
            "VALUES (%s, %s, %s, %s) RETURNING id, created_date",
            (project_id, applicant_id, message, status)
        )
        result = cursor.fetchone()
        return result[0], result[1]

    @staticmethod
    def get_all(cursor):
        cursor.execute(
            "SELECT id, project_id, applicant_id, created_date, message, status "
            "FROM applications"
        )
        return [Application.from_row(row) for row in cursor.fetchall()]

    @staticmethod
    def get_by_id(cursor, application_id):
        cursor.execute(
            "SELECT id, project_id, applicant_id, created_date, message, status "
            "FROM applications "
            "WHERE id = %s",
            (application_id,)
        )
        return Application.from_row(cursor.fetchone())

    @staticmethod
    def update_status(cursor, application_id, new_status):
        cursor.execute(
            "UPDATE applications "
            "SET status = %s "
            "WHERE id = %s",
            (new_status, application_id)
        )

    @staticmethod
    def get_users_applications(cursor):
        cursor.execute('SELECT applications.applicant_id, applications.project_id ' \
                       'FROM applications ' \
                       'INNER JOIN projects ' \
                       'ON applications.project_id = projects.id ' \
                       'WHERE projects.is_closed = false;')
        return cursor.fetchall()
