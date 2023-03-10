import psycopg2
import config
from account import accountSql
from status import statusSql, statusFill
from project import projectSql
from application import applicationSql
from category import categorySql
from faculty import facultySql
from project_categories import projectCategoriesSql
from create_indexes import createIndexes
from user_categories import accountInterestsSql
from database.recommendations import recommendationSql
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
