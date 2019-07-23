import mysql.connector as mysql

#establish a connection to the mysql server
db = mysql.connect(
    host='localhost',
    user='codork',
    passwd='passwd') #password hidden

#get cursor object
csr = db.cursor()
#creating database for observation-planner
csr.execute("CREATE DATABASE obsplanner")

#show all dbs; check if creation was successful
csr.execute("SHOW DATABASES")
for x in csr:
    print(x)

#connect to the database obsplanner
db = mysql.connect(
    host="localhost",
    user="codork",
    passwd="passwd",
    database="obsplanner")

#get cursor
csr = db.cursor()
#create a table to store field information
csr.execute("CREATE TABLE fields (id INT AUTO_INCREMENT PRIMARY KEY)")
               " ra CHAR(9),"
               " dec CHAR(9), "
               " area FLOAT(6), "
               " rising_time DATETIME, "
               " setting_time DATETIME, "
               " SNR_req FLOAT(6),"
               " SNR_achieved FLOAT(6),"
               " visits INT(3),"
               " visible_for INT(4))")

#check if table has been created
csr.execute("SHOW TABLES")
for x in csr:
    print(x)
