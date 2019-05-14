import mysql.connector
from Scripts_UI.CNN.Page_2 import Settings_CNN
from Scripts_UI._DataBase_ import Converter
from Scripts_UI._MainPage_._Auth_ import Auth_Page
from Scripts_UI._MainPage_.Main_Create import Choose_Model

import datetime

class Connection():

	def __init__(self):
		super(Connection, self).__init__()


	def check_existing_profile(self):

		# ----- Connection ----- #

		config = {
		    'user'    : 'flo',
		    'host'    : 'localhost',
		    'password': '',
		    'database': 'automatic_learning'
		}

		conn = mysql.connector.connect(**config)
		conn.set_converter_class(Converter.NumpyMySQLConverter)

		cursor = conn.cursor()

		# ----- Get Variables ----- #

		username, password = Auth_Page.Auth.check(self)

		# ----- Execute Query ----- #

		query = "SELECT username, password FROM profile WHERE username = '" + str(username) + "' AND password = '" + str(password) + "'"

		cursor.execute(query)

		# ----- Get and Return Datas ----- #

		rows = cursor.fetchall()

		try:
			return rows[0][0], rows[0][1]
		except IndexError:
			return str('✗')

		# ------------------------- #


	def sign_up(self):

		# ----- Connection ----- #

		config = {
		    'user'    : 'flo',
		    'host'    : 'localhost',
		    'password': '',
		    'database': 'automatic_learning'
		}

		conn = mysql.connector.connect(**config)
		conn.set_converter_class(Converter.NumpyMySQLConverter)

		cursor = conn.cursor()

		# ----- Get Variables ----- #

		username, password = Auth_Page.Auth.stock_profile_datas(self)

		# ----- Preparation of the Request ----- #

		sql = 'INSERT INTO profile (username, password) VALUES (%s, %s)'
		val = (username, password)

		# ----- Execute Query ----- #

		cursor.execute(sql, val)
		conn.commit()

		print(cursor.rowcount, 'Query ✓')

		# ------------------------- #


	def query(self):

		# ----- Connection ----- #

		config = {
		    'user'    : 'flo',
		    'host'    : 'localhost',
		    'password': '',
		    'database': 'automatic_learning'
		}

		conn = mysql.connector.connect(**config)
		conn.set_converter_class(Converter.NumpyMySQLConverter)

		cursor = conn.cursor()

		# ----- Get Variables ----- #

		acc = Settings_CNN.Set_Settings_CNN.stock_acc(self)
		loss = Settings_CNN.Set_Settings_CNN.stock_loss(self)
		model_name = Settings_CNN.Set_Settings_CNN.stock_model_name(self)

		print(acc)
		print(loss)

		# Test #

		if query == 'set':
			sql = 'INSERT INTO ' + algo + ' VALUES ('.join(str(p) for p in params_list) + ')'
		elif query == 'get':
			sql = 'IF EXISTS SELECT * FROM ' + algo + ' WHERE client = ' + client

		# ----- Final Request ----- #

		sql = 'INSERT INTO stats (' + algo + ', accuracy, loss, model_name) VALUES (%s, %s, %s, %s)'
		val = (algo, acc, loss, model_name)


        # ---- END TESTING ---- #

		# ----- Preparation of the Request ----- #

		sql = 'INSERT INTO cnn (accuracy, loss, model_name) VALUES (%s, %s, %s)'
		val = (acc, loss, model_name)

		# ----- Execute Query ----- #

		cursor.execute(sql, val)
		conn.commit()

		print(cursor.rowcount, 'Query ✓')

		# ------------------------- #