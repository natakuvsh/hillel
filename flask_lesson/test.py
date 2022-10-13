import sqlite3

def db_connect(db_name):
    connection = sqlite3.connect(db_name)
    connection.commit()
    connection.close()
    return connection

@db_connect('')
def create_table(connection):
    curs = connection. curs.execute("""
        CREATE TABLE IF NOT EXISTS testTable (
            id INTEGER PRIMARY KEY,
            test_text TEXT NOT NULL
            );""")
    return "table created"

@db_connect
def insert_item(curs, item):
    curs.execute("INSERT INTO testTable(test_text) VALUES (:item)",{"item": item})
    return f"{item} inserted"

@db_connect
def select_all(curs):
    result = curs.execute("SELECT * from testTable")
    return result.fetchall()

print(create_table())