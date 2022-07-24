import sqlite3

class DB_users():
	def __init__(self):
		self.conn = sqlite3.connect('results.db')

	def conect(self):
		self.conn = sqlite3.connect('results.db')

	def get_list_of_users(self):
		cursor = self.conn.execute("SELECT _USER_ID_ FROM USERS WHERE _STATUS_='on';")
		return cursor

	def db_add_user(self, user_id):
		cursor = self.conn.execute("SELECT MAX(ID) FROM USERS;")
		for i in cursor:
			x=i;
			break

		if x[0]==None:
			x = 0;
		else:
			x = x[0] + 1
		self.conn.execute(
			"INSERT INTO USERS (ID, _USER_ID_, _STATUS_)\
			VALUES({0},'{1}','{2}');".format(x,user_id,'on')
				)
		self.conn.commit()

	def change_status(self, user_id,user_status):
		cursor = self.conn.execute("UPDATE USERS SET _STATUS_='{0}' WHERE _USER_ID_='{1}';".format(user_status,user_id))
		self.conn.commit()

	def close_db(self):
		self.conn.close()