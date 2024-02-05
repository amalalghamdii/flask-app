import sqlite3

conn = sqlite3.connect('user.db')
print ("Opened database successfully")
cur = conn.cursor

conn.execute('CREATE TABLE user (username TEXT PRIMARY KEY unique, password TEXT, firstname TEXT, lastname TEXT , email TEXT)')
print ("Table created successfully")
conn.commit()
conn.close()



