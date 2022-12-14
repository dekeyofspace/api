

"""
Возможные запросы:
/
/?amount=2 (сколько показать)
/?column=названиеCтолбца (author или content)
"""

from flask import Flask, request, jsonify
import sqlite3
import logging as l

l.basicConfig(level=l.DEBUG, format='%(levelname)s %(lineno)d, %(funcName)s - %(message)s')

app = Flask(__name__)

conn = sqlite3.connect('db.sqlite3', check_same_thread=False)
cur = conn.cursor()


@app.route('/')
def get_all():
    """
    Get all data from the database
    :return: {"content":[], "authors":[]}
    """
    args = request.args
    column = args.get('column')
    column = column or '*'
    amount = args.get('amount')  

    query = f'SELECT {column} FROM news'

    cur.execute(query)

    try:
        amount = int(amount)
    except:
        l.error('converting to int has failed', exc_info=True)

    data = cur.fetchmany(amount) if amount else cur.fetchall()
    if column == '*':
        return_var = []
        for t in data:
            return_var.append(
                {
                    'content': t[0],
                    'author': t[1],
                }
            )
    # If column arg is provided
    else:
        return_var = {}
        for t in data:
            return_var.setdefault(column, [])
            return_var[column].append(t[0])

    return_var = jsonify(return_var)
    return return_var


if __name__ == '__main__':
    app.run(debug=True, port=5001)
