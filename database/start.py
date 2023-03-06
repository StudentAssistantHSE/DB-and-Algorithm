import psycopg2
import config
import config_local
from account import accountSql, accountFill
from status import statusSql, statusFill
from project import projectSql, projectFill
from project_timetable import projectTimetableSql, projectTimetableFill
from application import applicationSql, applicationFill
from category import categoryFill, categorySql
from faculty import facultyFill, facultySql
import DummyData.facultyFill, DummyData.accountFill, DummyData.projectFill, DummyData.applicationsFill, DummyData.categoryFill,\
    DummyData.accountInterestsFill, DummyData.projectCategoriesFill
from project_categories import projectCategoriesFill, projectCategoriesSql
from create_indexes import createIndexes
from user_categories import accountInterestsFill, accountInterestsSql
from recommendations import recommendationSql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

conn = psycopg2.connect(database=config.DB_NAME, user=config.DB_USER, port=config.DB_PORT, password=config.DB_PASS,
                       host=config.DB_HOST)

# conn = psycopg2.connect(database=config_local.DB_NAME, user=config_local.DB_USER, port=config_local.DB_PORT, password=config_local.DB_PASS,
#                         host=config_local.DB_HOST)

try:
    cursor = conn.cursor()
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    requests = [facultySql, accountSql, statusSql, projectSql, applicationSql, categorySql, accountInterestsSql,
                 projectCategoriesSql, recommendationSql]
    fill = [statusFill]

    # executing query
    for request in requests:
        cursor.execute(request)
    for filling in fill:
        cursor.execute(filling)
    cursor.execute(createIndexes)
    print("Success")

except Exception as err:
    print("Error: " + err)

finally:
    conn.close()
