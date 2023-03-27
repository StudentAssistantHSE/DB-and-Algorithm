import psycopg2


class User:
    def __init__(self, email, fullname, password, faculty_id=None, description=None, last_login=None, created_date=None,
                 updated_date=None):
        self.email = email
        self.fullname = fullname
        self.password = password
        self.faculty_id = faculty_id
        self.description = description
        self.last_login = last_login
        self.created_date = created_date
        self.updated_date = updated_date

    @classmethod
    def from_row(cls, row):
        return cls(*row)

    @staticmethod
    def initiate(cursor):
        cursor.execute(''' DROP TABLE IF EXISTS users CASCADE;
            CREATE TABLE users (
            ID SERIAL PRIMARY KEY NOT NULL,
            EMAIL text NOT NULL UNIQUE,
            FULLNAME text NOT NULL,
            LAST_LOGIN DATE,
            DESCRIPTION TEXT,
            BIO TEXT,
            FACULTY_ID BIGINT REFERENCES FACULTIES,
            PASSWORD text NOT NULL,
            CREATED_DATE DATE NOT NULL DEFAULT CURRENT_DATE,
            UPDATED_DATE DATE)''')

    @staticmethod
    def create_table(cur):
        cur.execute('DROP TABLE IF EXISTS users CASCADE')
        cur.execute('''CREATE TABLE users (
            ID SERIAL PRIMARY KEY NOT NULL,
            EMAIL text NOT NULL UNIQUE,
            FULLNAME text NOT NULL,
            LAST_LOGIN DATE,
            DESCRIPTION TEXT,
            FACULTY_ID BIGINT REFERENCES FACULTIES,
            PASSWORD text NOT NULL,
            CREATED_DATE DATE NOT NULL DEFAULT CURRENT_DATE,
            UPDATED_DATE DATE
        )''')

    def save(self, cur):
        cur.execute('''INSERT INTO users (EMAIL, FULLNAME, PASSWORD, FACULTY_ID, DESCRIPTION, LAST_LOGIN, CREATED_DATE, UPDATED_DATE)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)''',
                    (self.email, self.fullname, self.password, self.faculty_id, self.description, self.last_login,
                     self.created_date, self.updated_date))

    @staticmethod
    def get_by_email(cur, email):
        cur.execute('SELECT * FROM users WHERE EMAIL = %s', (email,))
        user = cur.fetchone()
        if user:
            return User(*user[1:])
        return None

    @staticmethod
    def get_all_id_and_faculty(cursor):
        cursor.execute('SELECT users.id, users.faculty_id ' \
                       'FROM users')
        return cursor.fetchall()

    @staticmethod
    def get_user_from_same_faculty(cursor, faculty_id):
        cursor.execute('SELECT u.id ' \
                       'FROM users u ' \
                       'INNER JOIN applications a ' \
                       'ON u.id = a.applicant_id ' \
                       'INNER JOIN project_categories pc ' \
                       'ON a.project_id = pc.project_id ' \
                       'INNER JOIN projects p ON pc.project_id = p.id AND p.is_closed = false ' \
                       'WHERE u.faculty_id = %s ' \
                       'ORDER BY RANDOM() ' \
                       'LIMIT 1;', (faculty_id,))
        return cursor.fetchall()

    @staticmethod
    def get_user_faculty(cursor, id):
        cursor.execute('Select Faculty_id from users where id = %s', (id,))
        return cursor.fetchall()
