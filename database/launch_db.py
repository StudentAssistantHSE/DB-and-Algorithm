import psycopg2
import config
from controllers import ApplicationController, CategoriesController, FacultyController, ProjectCategoriesController, \
    ProjectsController, ProjectsTimetableController, StatusesController, UserCategoriesController, UserRecommendationsController, \
    UsersController
import DummyData.facultyFill, DummyData.accountFill, DummyData.projectFill, DummyData.applicationsFill, DummyData.categoryFill,\
    DummyData.accountInterestsFill, DummyData.projectCategoriesFill
from database.create_indexes import createIndexes
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

conn = psycopg2.connect(database=config.DB_NAME, user=config.DB_USER, port=config.DB_PORT, password=config.DB_PASS,
                       host=config.DB_HOST)

# conn = psycopg2.connect(database=config_local.DB_NAME, user=config_local.DB_USER, port=config_local.DB_PORT, password=config_local.DB_PASS,
#                         host=config_local.DB_HOST)

try:
    cursor = conn.cursor()
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

    application = ApplicationController.ApplicationController(cursor)
    categories = CategoriesController.CategoryController(cursor)
    faculty = FacultyController.FacultyController(cursor)
    projectCategories = ProjectCategoriesController.ProjectCategoriesController(cursor)
    projects = ProjectsController.ProjectController(cursor)
    projectTimetable = ProjectsTimetableController.ProjectTimetableController(cursor)
    statuses = StatusesController.StatusesController(cursor)
    userCategories = UserCategoriesController.UserCategoriesController(cursor)
    userRecommendations = UserRecommendationsController.UserRecommendationsController(cursor)
    users = UsersController.UsersController(cursor)

    controllers = [faculty, users, statuses, projects, application, categories, userCategories, projectCategories,
                   userRecommendations, projectTimetable]

    fill = [DummyData.facultyFill.facultyFill, DummyData.accountFill.accountFill,
            DummyData.projectFill.projectFill,
            DummyData.applicationsFill.applicationFill, DummyData.categoryFill.categoryFill,
            DummyData.accountInterestsFill.accountInterestsFill,
            DummyData.projectCategoriesFill.projectCategoriesFill]

    # executing query
    for request in controllers:
        request.initiate_creation()
    for filling in fill:
        cursor.execute(filling)
    cursor.execute(createIndexes)
    print("Success")

except Exception as err:
    print("Error: " + err)

finally:
    conn.close()
