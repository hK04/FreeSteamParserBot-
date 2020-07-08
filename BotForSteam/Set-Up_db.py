import sqlite3 

conn = sqlite3.connect('results.db')

print('Succesfully connected!')

conn.execute('''CREATE TABLE USERS
	(ID INT PRIMARY KEY NOT NULL,
	_USER_ID_ TEXT NOT NULL,
	_STATUS_ TEXT NOT NULL);
	''')
conn.commit()
conn.close()