import sqlite3

connection = sqlite3.connect('mydatabase.db')

cursor = connection.cursor()

command1  = """CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY, username TEXT, password TEXT);"""
cursor.execute(command1)

cursor.execute("INSERT INTO users VALUES (1,'user1','password1')")
# cursor.execute("INSERT INTO users VALUES (2, 'user2','password2')")

cursor.execute("SELECT * FROM users")
print(cursor.fetchall())

# cursor.execute("UPDATE users SET password = 'new_password' WHERE id=2")

# cursor.execute("DELETE FROM users WHERE id=1")
cursor.execute("SELECT * FROM users")
print(cursor.fetchall())
connection.commit()
connection.close()
