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


curs = ''
con = ''

def connect_to_db(): #Για να συνεδέεται στη βάση μας
    global curs,con
    try:
        con = mysql.connector.connect(host=host_db,user=user_db, password=password_db, database=database)
        curs = con.cursor()
        print("Επιτυχής σύνδεση στην βάση δεδομένων!\n")
    except:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
        exit()



def insert_gipedo(): #prosthiki gipedoy
    global curs,con
    while (True):
        try:
            gipedo_onoma= input('Πως λέγεται το γήπεδο;\n')
            gipedo_eidos = input('Τι είδους είναι το γήπεδο;\n')
            gipedo_texn_diath = input('To γήπεδο είναι τεχν διαθέσιμο 0 ή 1 :\n')
            insert = "INSERT INTO gipedo(Id,Eidos,Onoma,Texn_Diathesimotita) VALUES(NULL,'"+gipedo_eidos+"','"+gipedo_onoma+"','"+gipedo_texn_diath+"');"
            curs.execute(insert)
            con.commit()
            ans = input('Θες να προσθέσουμε κάποιο άλλο γήπεδο; Αν ναι πατήστε 1, αλλιώς πατήστε κενό και μετά enter για επιστροφή στο αρχικό μενού!\n')
            if (ans!='1'):
                print('Εγινε η προσθήκη')
                return
        except:
            print("Αδυναμία προσθήκης γηπέδου!")
            return

def kratisi():
    while True:
        ans =input('Για να κάνει κράτηση ένα άτομο πατήστε 1\nΓια έξοδο πατήστε κενό και μετά enter\n')#Μετά να δούμε αν θέλουμε και άλλα εδώ
        if ans=='1':
            kratisi_atomo()
        if ans==' ':
            return

def kratisi_atomo():# Θέλει βελτίωση
    global curs,con
    ans = input("Βάλτε εδώ τον ΑΜΚΑ, το τηλέφωνο ή το Επώνυμο του Πάικτη.")
    if (ans.isdigit()): # Εδώ ελέγχω αν είναι νούμερο ή γράμματα. Ώστε να ξέρω τι μου δίνει, αν μου δίνει όνομα ή κάτι με νούμερα
        #Εχω κάτι με νούμερα. Πρέπει να ελέξω αν είναι ΑΜΚΑ ή τηλέφωνο. Αρα αν είναι 11 ή 10 ψηφία
        if (len(str(ans)) == 11):#Αυτό είναι το μέγεθος του ΑΜΚΑ
            curs.execute("SELECT * FROM `atomo` WHERE AMKA='"+ans+"';")
            result=curs.fetchone()
            print(result)
        elif(len(str(ans)) == 10):#Αυτό είναι το μέγεθος του τηλεφώνου
            curs.execute("SELECT * FROM `atomo` WHERE Tilefono='"+ans+"';")
            result=curs.fetchall()
            print(result)
    else:
        #Εχω όνομα αρα κάνω αντίστοιχο query
        eponimo= ans
        curs.execute("SELECT * FROM `atomo` WHERE Eponimo='"+eponimo+"';")
        result=curs.fetchall()
        print(result)
    exit()

def view_gipedo(): # Αυτό απλώς εκτυπώνει τα γήπεδα πρέπει να γίνει πιο όμορφη παρουσιασή του πχ σαν πίνακα
    global curs,con
    print("Αυτά είναι τα γήπεδα μας")
    curs.execute("SELECT * FROM `gipedo`")
    result=curs.fetchall()

    for i in result:
        print(i)

def menu(): #Σε αυτό το μενού πρέπει να σχεδιάσουμε τις επιλογές
    print('Καλησπέρα!\n')
    while True:
        ans =input('Για να προσθέσετε γήπεδο πατήστε....1\nΓια να δείτε όλα τα γήπεδα μας πατήστε 2\nΓια να κάνετε καινούργια κράτηση πατήστε το 4\nΓια έξοδο πατήστε κενό και μετά enter\n')
        if ans=='1':
            insert_gipedo()
        if ans=='2':
            view_gipedo()
        if ans=='4':
            kratisi()
        if ans==' ':
            return

def main():#Εδώ μέσα βάζεις όποια συνάρτηση θέλεις να γίνει.
    connect_to_db()
    menu()
    con.close()



if __name__=="__main__":
    main()
