import random

import pandas as pd
import numpy as np
import psycopg2
from controllers import CategoriesController, ProjectCategoriesController, ProjectsController, ApplicationController, \
    UsersController, UserRecommendationsController
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from sklearn.metrics.pairwise import cosine_similarity

from config import DB_NAME, DB_PORT, DB_PASS, DB_HOST, DB_USER
from recommendationHelpers import SqlRequest
from recommendationHelpers import AlgorithmOperator

conn = psycopg2.connect(database=DB_NAME, user=DB_USER, port=DB_PORT, password=DB_PASS,
                        host=DB_HOST)

try:
    cursor = conn.cursor()
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

    categoryController = CategoriesController.CategoryController(cursor)
    projectCategoriesController = ProjectCategoriesController.ProjectCategoriesController(cursor)
    projectController = ProjectsController.ProjectController(cursor)
    applicationsController = ApplicationController.ApplicationController(cursor)
    usersController = UsersController.UsersController(cursor)
    userRecommendationController = UserRecommendationsController.UserRecommendationsController(cursor)

    tags = categoryController.get_all_categories()
    projects = projectController.get_id_non_closed()
    projectsTags = projectCategoriesController.get_all()
    tagsUnited = list(set().union(*tags))

    max_value = max(projects, key=lambda x: x[0])[0]
    df_tf = pd.DataFrame(np.zeros(((max_value), len(tags))), columns=tagsUnited)
    for el in projects:
        tagsOfProject = projectCategoriesController.get_by_project(el[0])
        if el == 1004:
            print()
        if len(tagsOfProject) != 0:
            df_tf[tags[tagsOfProject[0][1] - 1][0]][tagsOfProject[0][0]-1] = df_tf[tags[tagsOfProject[0][1] - 1][0]][tagsOfProject[0][0]-1] +\
                                                                   (1 / len(tagsOfProject))

    idf = {}
    for tag in range(1, len(tags)+1):
        projectsWithTag = projectCategoriesController.get_by_category(tag)
        if len(projectsWithTag) != 0:
            idf[tags[tag-1][0]] = np.log10(len(projects)/len(projectsWithTag))
        else:
            idf[tags[tag - 1][0]] = 0

    df_tf_idf = df_tf.copy()

    for tag in tags:
        for i in range(projects[-1][0]):
            df_tf_idf[tag[0]][i] = df_tf[tag[0]][i] * idf[tag[0]]

    res = pd.DataFrame(cosine_similarity(df_tf_idf))
    indexes = res.apply(AlgorithmOperator.get_top_indexes, axis=1) # Проекты со схожими тегами, без прибавки единицы

    usersApplications = applicationsController.get_users_applications()
    dictApplications = {}

    # group the tuples by their first element
    for tup in usersApplications:
        if tup[0] not in dictApplications:
            dictApplications[tup[0]] = [tup[1]]
        else:
            dictApplications[tup[0]].append(tup[1])

    # join the tuples with the same first element
    applicationsByUsers = [(key, tuple(val)) for key, val in dictApplications.items()]

    allUsers = usersController.get_all_id_and_faculty()
    recommend = {}
    for i in range(len(allUsers)):
        if allUsers[i][0] in dictApplications:
            apps = dictApplications.get(allUsers[i][0])
            temp = []
            for el in apps:
                temp.extend(indexes[el - 1])
            recommend.update({allUsers[i][0]: temp})
        else:
            faculty = usersController.get_user_faculty(allUsers[i][1])
            if len(faculty) != 0:
                simularStudent = usersController.get_user_from_same_faculty(allUsers[i][1])
                if len(simularStudent) != 0:
                    apps = dictApplications.get(simularStudent[0][0])
                    temp = []
                    for el in apps:
                        temp.append(el-1)
                    recommend.update({allUsers[i][0]: temp})
                else:
                    recommend.update({allUsers[i][0]: [random.randint(0, len(projects) - 1)]})
            else:
                recommend.update({allUsers[i][0]: [random.randint(0, len(projects) - 1)]})

    for i in range(len(allUsers)):
        if len(recommend[allUsers[i][0]]) == 0:
            faculty = usersController.get_user_faculty(allUsers[i][1])
            if len(faculty) != 0:
                simularStudent = usersController.get_user_from_same_faculty(allUsers[i][1])
                if len(simularStudent) != 0:
                    apps = dictApplications.get(simularStudent[0][0])
                    temp = []
                    for el in apps:
                        temp.append(el-1)
                    recommend.update({allUsers[i][0]: temp})
                else:
                    recommend.update({allUsers[i][0]: [random.randint(0, len(projects) - 1)]})
            else:
                recommend.update({allUsers[i][0]: [random.randint(0, len(projects) - 1)]})


    for key in recommend.keys():
        recommended_projects = list(set(recommend[key]))
        for i in range(len(recommended_projects)):
            userRecommendationController.insert_recommendations(key, recommended_projects[i] + 1)
    print('Success')


except Exception as err:
    raise err

finally:
    conn.close()
