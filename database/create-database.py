import sqlite3 as sql

connection = sql.connect('database.db')
cursor = connection.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS table_name (
id INTEGER PRIMARY KEY
)
''')

connection.commit()
connection.close()


