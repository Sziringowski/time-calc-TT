import sqlite3 as sql

def update_database():
    connection = sql.connect('database.db')
    cursor = connection.cursor()

    try:
        cursor.execute("BEGIN")

        cursor.execute()


        cursor.execute("COMMIT")

    except:
        cursor.execute("ROLLBACK")


    connection.commit()
    connection.close()


