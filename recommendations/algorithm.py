import pandas as pd
import numpy as np
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from sklearn.metrics.pairwise import cosine_similarity

from database.config import DB_NAME, DB_USER, DB_HOST, DB_PASS, DB_PORT
from recommendations.SqlRequest import SqlRequest
from recommendations.AlgorithmOperator import AlgorithmOperator

conn = psycopg2.connect(database=DB_NAME, user=DB_USER, port=DB_PORT, password=DB_PASS,
                        host=DB_HOST)

try:
    cursor = conn.cursor()
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    getTagsQuery = 'Select category from categories'
    getProjectTagsQuery = 'Select * from project_categories'
    getProjectQuery = 'Select ID from projects where is_closed = false'
    tags = SqlRequest.make_query(cursor, getTagsQuery)
    projects = SqlRequest.make_query(cursor, getProjectQuery)
    projectsTags = SqlRequest.make_query(cursor, getProjectTagsQuery)
    tagsUnited = list(set().union(*tags))
    df_tf = pd.DataFrame(np.zeros((len(projects), len(tags))), columns=tagsUnited)
    for i in range(len(projects)+1):
        getTagsOfCurrentProject = 'Select * from project_categories where project_id = %s'
        tagsOfProject = SqlRequest.make_query(cursor, getTagsOfCurrentProject, i)
        if len(tagsOfProject) != 0:
            df_tf[tags[tagsOfProject[0][1] - 1][0]][tagsOfProject[0][0]-1] = df_tf[tags[tagsOfProject[0][1] - 1][0]][tagsOfProject[0][0]-1] +\
                                                                   (1 / len(tagsOfProject))

    idf = {}
    for tag in range(1, len(tags)+1):
        getProjectsWithTag = 'Select * from project_categories where category_id = %s'
        projectsWithTag = SqlRequest.make_query(cursor, getProjectsWithTag, tag)
        idf[tags[tag-1][0]] = np.log10(len(projects)/len(projectsWithTag))

    df_tf_idf = df_tf.copy()

    for tag in tags:
        for i in range(len(projects)):
            df_tf_idf[tag[0]][i] = df_tf[tag[0]][i] * idf[tag[0]]

    res = pd.DataFrame(cosine_similarity(df_tf_idf))
    indexes = res.apply(AlgorithmOperator.get_top_indexes, axis=1) # Проекты со схожими тегами, без прибавки единицы

    getUsersApplicationsQuery = 'SELECT applications.applicant_id, applications.project_id ' \
                                'FROM applications ' \
                                'INNER JOIN projects ' \
                                'ON applications.project_id = projects.id ' \
                                'WHERE projects.is_closed = false;'
    usersApplications = SqlRequest.make_query(cursor, getUsersApplicationsQuery)
    dictApplications = {}

    # group the tuples by their first element
    for tup in usersApplications:
        if tup[0] not in dictApplications:
            dictApplications[tup[0]] = [tup[1]]
        else:
            dictApplications[tup[0]].append(tup[1])

    # join the tuples with the same first element
    applicationsByUsers = [(key, tuple(val)) for key, val in dictApplications.items()]

    getAllUsersQuery = 'SELECT users.id, users.faculty_id ' \
                       'FROM users'

    getUserFromSameFacultyQuery = 'SELECT u.id ' \
                                  'FROM users u ' \
                                  'INNER JOIN applications a ' \
                                  'ON u.id = a.applicant_id ' \
                                  'INNER JOIN project_categories pc ' \
                                  'ON a.project_id = pc.project_id ' \
                                  'WHERE u.faculty_id = %s ' \
                                  'ORDER BY RANDOM() ' \
                                  'LIMIT 1;'


    allUsers = SqlRequest.make_query(cursor, getAllUsersQuery)
    recommend = {}
    for i in range(len(allUsers)):
        if allUsers[i][0] in dictApplications:
            apps = dictApplications.get(allUsers[i][0])
            temp = []
            for el in apps:
                temp.extend(indexes[el - 1])
            recommend.update({allUsers[i][0]: temp})
        else:
            simularStudent = SqlRequest.make_query(cursor, getUserFromSameFacultyQuery, allUsers[i][1])
            apps = dictApplications.get(simularStudent[0][0])
            temp = []
            for el in apps:
                temp.append(el-1)
            recommend.update({allUsers[i][0]: temp})

    for i in range(len(allUsers)):
        if len(recommend[allUsers[i][0]]) == 0:
            simularStudent = SqlRequest.make_query(cursor, getUserFromSameFacultyQuery, allUsers[i][1])
            apps = dictApplications.get(simularStudent[0][0])
            temp = []
            for el in apps:
                temp.append(el-1)
            recommend.update({allUsers[i][0]: temp})

    for key in recommend.keys():
        recommended_projects = list(set(recommend[key]))
        for i in range(len(recommended_projects)):
            query = 'Insert into user_recommendations (user_id, project_id) values (%s, %s);'
            cursor.execute(query, (key, recommended_projects[i]+1))
    print('e')


except Exception as err:
    print("Error: " + str(err))

finally:
    conn.close()
