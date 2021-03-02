from flask import current_app


def query_index(index, query, page, per_page):
    if not current_app.sphinxsearch:
        return [], 0

    con = current_app.sphinxsearch
    cur = con.cursor()
    cur.execute("SELECT id FROM {} WHERE match('{}') LIMIT {},{};".format(index, query, (page - 1) * per_page, per_page))
    ids = cur.fetchall()

    cur.execute("SHOW meta")
    meta = cur.fetchall()
    # find row with 'total' and retrive it's value
    total = int([item[1] for item in meta if item[0] == 'total'][0])

    return ids, total
