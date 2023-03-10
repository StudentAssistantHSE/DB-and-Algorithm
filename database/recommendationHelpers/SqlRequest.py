def make_query(cursor, query, param=None):
    cursor.execute(query, (param,))
    return cursor.fetchall()
