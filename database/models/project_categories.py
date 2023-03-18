class ProjectCategory:
    def __init__(self, id, project_id, category_id):
        self.id = id
        self.project_id = project_id
        self.category_id = category_id

    @classmethod
    def from_row(cls, row):
        return cls(*row)

    @staticmethod
    def initiate(cursor):
        cursor.execute(''' DROP TABLE IF EXISTS project_categories CASCADE;
            CREATE TABLE project_categories (
            ID SERIAL PRIMARY KEY NOT NULL,
            project_id int NOT NULL,
            category_id int NOT NULL,
            UNIQUE(project_id, category_id),
            FOREIGN KEY (project_id) REFERENCES projects(id) ON UPDATE CASCADE,
            FOREIGN KEY (category_id) REFERENCES categories(id) ON UPDATE CASCADE);''')

    @staticmethod
    def create(cursor, project_id, category_id):
        cursor.execute(
            "INSERT INTO project_categories (project_id, category_id) "
            "VALUES (%s, %s) RETURNING id",
            (project_id, category_id)
        )
        return cursor.fetchone()[0]

    @staticmethod
    def get_all(cursor):
        cursor.execute(
            "SELECT * "
            "FROM project_categories"
        )
        return cursor.fetchall()

    @staticmethod
    def get_by_id(cursor, project_category_id):
        cursor.execute(
            "SELECT id, project_id, category_id "
            "FROM project_categories "
            "WHERE id = %s",
            (project_category_id,)
        )
        return ProjectCategory.from_row(cursor.fetchone())

    @staticmethod
    def get_by_project(cursor, project_id):
        cursor.execute(
            "SELECT project_id, category_id "
            "FROM project_categories "
            "WHERE project_id = %s",
            (project_id,)
        )
        return cursor.fetchall()

    @staticmethod
    def get_by_category(cursor, category_id):
        cursor.execute(
            'Select * from project_categories where category_id = %s',
            (category_id,)
        )
        return cursor.fetchall()

    @staticmethod
    def delete(cursor, project_category_id):
        cursor.execute(
            "DELETE FROM project_categories "
            "WHERE id = %s",
            (project_category_id,)
        )
