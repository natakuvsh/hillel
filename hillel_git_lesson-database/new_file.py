import sqlite3
from sqlite3 import connect

def sqlite_connect(db_name):
    def connect(func):
        def _db_connect():

            connection = connect(db_name)
            try:
                result = func(connection)
                connection.commit()
            except sqlite3.Error:
                result = None
            finally:
                connection.close()
            return result
        return _db_connect
    return connect


@sqlite_connect('library_db.sqlite3')
def all_books(connection):
    curs = connection.cursor()
    books = curs.execute("SELECT * from author")
    return books.fetchall()


print(all_books())
