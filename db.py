import sqlite3

conn = sqlite3.connect('patients.sqlite')

cursor = conn.cursor()
sql_query = """CREATE TABLE patients 
(id integer PRIMARY KEY ,
firstname TEXT NOT NULL,
lastname TEXT NOT NULL,
cin TEXT NOT NULL,
dose1 TEXT NOT NULL,
dose2 TEXT NOT NULL,
dose3 TEXT NOT NULL)"""
cursor.execute(sql_query)

sql = "INSERT INTO patients(firstname,lastname,cin,dose1,dose2,dose3) VALUES(?,?,?,?,?,? )"
cursor.execute(sql,("simo","lastname","cin","dose1","dose2","dose3"))
conn.commit()