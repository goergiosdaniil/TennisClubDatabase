import mysql.connector
from mysql.connector import errorcode

import os #Αυτό χρειάζεται για το dotenv. 
from os.path import join, dirname
from dotenv import load_dotenv #Το dotenv χρειάζεται για να μπορούμε να τραβάμε τα στοιχεία για τη βάση και να μην φαίνονται στο git

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

host_db=os.environ.get("HOST_DB") # Στα παρακάτω θέτω τις μεταβλητές για τη σύνδεση
user_db=os.environ.get("USER_DB")
password_db=os.environ.get("PASSWORD_DB")
database=os.environ.get("DATABASE_DB")


try:

    con = mysql.connector.connect(host=host_db,
                                  user=user_db, password=password_db, database=database)

except mysql.connector.Error as err:
  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    print("Something is wrong with your user name or password")
  elif err.errno == errorcode.ER_BAD_DB_ERROR:
    print("Database does not exist")
  else:
    print(err)
else:
    curs=con.cursor()
    curs.execute("INSERT INTO `gipedo` (`Id`, `Eidos`, `Onoma`, `Texn_Diathesimotita`) VALUES (NULL, 'test', 'okok', '2')")

    curs.execute("SELECT * FROM `gipedo`")
    result=curs.fetchall()

    for i in result:
        print(i)

    con.commit()
    con.close()







