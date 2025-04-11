import mysql.connector
db = mysql.connector.connect(user='root', password='',host='localhost')
code = "'CREATE DATABASE `TEST1` "

mycursor = db.cursor()
mycursor.execute(code)