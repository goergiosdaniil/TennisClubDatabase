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


def insert_atomo(): #prosthiki ylikou 
    global curs,con
    while (True):
        try:
            choice = input('Πατήστε 1 για εισαγωγή παίκτη, 2 για εισαγωγή προπονητή\n')
            if choice!='1' and choice!='2':
                print('Άκυρη επιλογή!')
            else:                
                atomo_AMKA,atomo_eponimo,atomo_onoma = input('Να γίνει εισαγωγή βασικών στοιχείων με την ακόλουθη μορφή: ΑΜΚΑ Επόνυμο Όνομα\n').split()            
                atomo_tilefono,atomo_email=input('Να γίνει εισαγωγή στοιχείων επικοινωνίας με την ακόλουθη μορφή: Τηλέφωνο Email\n').split()
                atomo_odos=input('Να γίνει εισαγωγή της Οδός Κατοικείας του ατόμου\n')
                atomo_arithmos,atomo_poli,atomo_TK=input('Να γίνει εισαγωγή στοιχείων της υπόλοιπης διεύθυνσης με την ακόλουθη μορφή:Αριθμός Πόλη και TK\n').split()
                insert1 = "INSERT INTO atomo(AMKA,Eponimo,Onoma,Tilefono,Email,Odos,Arithmos,Poli,TK) VALUES('"+atomo_AMKA+"','"+atomo_eponimo+"','"+atomo_onoma+"','"+atomo_tilefono+"','"+atomo_email+"','"+atomo_odos+"','"+atomo_arithmos+"','"+atomo_poli+"','"+atomo_TK+"');"
                if choice=='1':
                    paiktis_im = input('Να γίνει εισαγωγή της ημερομηνίας λήξης του δελτίου ηγείας σε μορφή YYYY-MM-DD:\n')
                    insert2 = "INSERT INTO paiktis(AMKA,Hm_Lixis_Deltiou) VALUES('"+atomo_AMKA+"','"+paiktis_im+"');"
                elif choice=='2':
                    prop_AFM = input('Να γίνει εισαγωγή του ΑΦΜ του εργαζόμενου:\n')
                    prop_wage = input('Να γίνει εισαγωγή του ορομισθίου του εργαζόμενου:\n')
                    prop_bio = input('Να γίνει εισαγωγή του βιογραφικού του εργαζόμενου:\n')
                    insert2 = "INSERT INTO proponitis(AMKA,AFM,Oromisthio,Viografiko) VALUES('"+atomo_AMKA+"','"+prop_AFM+"','"+prop_wage+"','"+prop_bio+"');"
                curs.execute(insert1)
                curs.execute(insert2)
                con.commit()
            ans = input('Θες να προσθέσουμε κάποιο άλλο άτομο; Αν ναι πατήστε 1, αλλιώς πατήστε κενό και μετά enter για επιστροφή στο αρχικό μενού!\n')
            if (ans!='1'):
                print('Εγινε η προσθήκη')
                return
        except:
            print("Αδυναμία προσθήκης ατόμου.")
            return


def view_atomo(a_type): #Για να εμφανίζονται είτε οι προπονητές είτε οι παίκτες
    global curs,con
    
    if (a_type==1):
        curs.execute("SELECT atomo.AMKA,atomo.Onoma,atomo.Eponimo FROM `atomo` WHERE atomo.AMKA IN (SELECT AMKA FROM `paiktis`)")
    elif (a_type==2):
        curs.execute("SELECT atomo.AMKA,atomo.Onoma,atomo.Eponimo FROM `atomo` WHERE atomo.AMKA IN (SELECT AMKA FROM `proponitis`)")    
    result=curs.fetchall()

    for i in result:
        print(i)





        


def kratisi():# Θέλει βελτίωση
    global curs,con
    ans = input("Βάλτε εδώ τον ΑΜΚΑ, το τηλέφωνο ή το Επώνυμο του Παίκτη.")
    if (ans.isdigit()): # Εδώ ελέγχω αν είναι νούμερο ή γράμματα. Ώστε να ξέρω τι μου δίνει, αν μου δίνει όνομα ή κάτι με νούμερα
        #Εχω κάτι με νούμερα. Πρέπει να ελέξω αν είναι ΑΜΚΑ ή τηλέφωνο. Αρα αν είναι 11 ή 10 ψηφία
        if (len(str(ans)) == 11):#Αυτό είναι το μέγεθος του ΑΜΚΑ
            curs.execute("SELECT * FROM `atomo` WHERE AMKA='"+ans+"';")
            result=curs.fetchone()
            print(ans)
            print(result)
        elif(len(str(ans)) == 10):#Αυτό είναι το μέγεθος του τηλεφώνου
            curs.execute("SELECT * FROM `atomo` WHERE Tilefono='"+ans+"';")
            result=curs.fetchall()
            print(result[0][0])
    else:
        #Εχω όνομα αρα κάνω αντίστοιχο query
        eponimo= ans.capitalize()
        curs.execute("SELECT * FROM `atomo` WHERE Eponimo='"+eponimo+"';")
        print(eponimo) 
        results=curs.fetchall()
        if (len(results) == 0):
            print("Δεν υπάρχει παίκτης με αυτό το όνομα. ")
            kratisi()
            exit()
        elif (len(results) == 1):
            print("Ο παίκτης είναι: ")
            print(results[0][1],results[0][2])
            inp = input("Σωστό. Ν(αι) ή Ο(χι): ")
            if (inp == "Ν" or inp == "N"):#greek or engilsh
                amka = results[0][0]
                print(amka)
            else:
                kratisi()
                exit()
        elif (len(results) > 1):
            print("Εχουμε πάνω από έναν παίκτη")
            print("Ποιον παίκτη θέλετε;")
            counter = 0
            print("Ε Όνομα Επώνυμο")
            for result in  results :
                print(counter,result[1],result[2])
                counter = counter + 1
            print("Ποιος είναι ο αριθμός του παίκτη;")
            selection = input("Αν δεν είναι κανένας πατήστε κενό και μετά enter")
            if (selection == " " or selection == ""):
                kratisi()
                exit()
            elif (selection.isdigit()):
                amka = results[int(selection)][0]

    print("Το αμκα του παίκτη για τον οποίο γιίνεται η κράτηση είναι: ",amka)
            
            
        

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


def view_gipedo(mode): # Αυτό απλώς εκτυπώνει τα γήπεδα πρέπει να γίνει πιο όμορφη παρουσιασή του πχ σαν πίνακα
    global curs,con
    
    if (mode==1):
        print("Αυτά είναι όλα τα γήπεδα μας")
        curs.execute("SELECT * FROM `gipedo`")
    elif (mode==2):
        print("Αυτά είναι όλα τα διαθέσιμα γήπεδα μας")
        curs.execute("SELECT * FROM `gipedo` WHERE Texn_Diathesimotita = '1'")        
    result=curs.fetchall()

    for i in result:
        print(i)


def alter_gipedo():
    global curs,con
    ids = input('Εισάγετε τα ID των γηπέδων των οποίων θα θέλατε να αλλάξετε την διαθεσημότητα, χωρισμένα ανα κενό:\n').split()
    for i in ids:
        curs.execute("SELECT Texn_Diathesimotita FROM `gipedo` WHERE Id = "+i)
        old_d=curs.fetchall();
        new_d = str(int(not old_d[0][0]));
        curs.execute("UPDATE`gipedo` SET Texn_Diathesimotita = '"+new_d+"' WHERE Id = "+i)
    curs.commit()
        
    
        

def gipedo_menu(): #Ένα γενικό μενου για τις διάφορες ενέργειες που μπορούν να γίνουν πάνω στα γήπεδα
    
    while True:
        print('Για να δείτε όλα τα γήπεδα μας πατήστε 1\nΓια να δείτε τα διαθέσιμα γήπεδα πατήστε 2')
        print('Για να προσθέσετε γήπεδο πατήστε 3\nΓια να αλλάξετε την διαθεσιμότητα ενος γηπέδου πατήστε 4')
        print('Για επιστροφή στο αρχικό μενού πατήστε κενό και μετά enter')
        ans =input()
                   
        if ans=='1':
            view_gipedo(1)
        if ans=='2':
            view_gipedo(2)
        if ans=='3':
            insert_gipedo()
        if ans=='4':
            alter_gipedo()
        if ans==' ':
            return
        


def view_group(): # Αυτό απλώς εκτυπώνει τα γήπεδα πρέπει να γίνει πιο όμορφη παρουσιασή του πχ σαν πίνακα
    global curs,con
    
    print("Αυτά είναι όλα τα γγκρούπ μας")
    curs.execute("SELECT * FROM `group_Ekmathisis`")   
    result=curs.fetchall()

    for i in result:
        print(i)

def insert_group(): #Συνάρτηση για εισαγωγή ατόμου, παίκτη η προπονητή, στην βάση
    global curs,con
    while (True):
        try:
            group_onoma= input('Πως λέγεται το γκρουπ;\n')
            group_epipedo = input('Το επίπεδο του γκρουπ θα είναι:\n')
            group_im_enarxis = input('Να γίνει εισαγωγή της ημερομηνίας έναρξης σε μορφή YYYY-MM-DD:\n')
            group_im_lixis = input('Να γίνει εισαγωγή της ημερομηνίας λήξης σε μορφή YYYY-MM-DD:\n')
            print("Ποιούς απο τους προπονητές θα εκπαιδεύσει το group;")
            view_atomo(2)
            AMKA_prop = input('To ΑΜΚΑ του προπονητή:\n')
            
            insert = "INSERT INTO group_Ekmathisis(Id,Onoma,Epipedo,Hm_Lixis,Hm_Enarxis,AMKA_Proponiti) VALUES(NULL,'"+group_onoma+"','"+group_epipedo+"','"+group_im_enarxis+"','"+group_im_lixis+"','"+AMKA_prop+"');"
            curs.execute(insert)
            con.commit()
            ans = input('Θες να προσθέσουμε κάποιο άλλο γκρουπ; Αν ναι πατήστε 1, αλλιώς πατήστε κενό και μετά enter για επιστροφή στο αρχικό μενού!\n')
            if (ans!='1'):
                print('Εγινε η προσθήκη')
                return
        except:
            print("Αδυναμία προσθήκης γηπέδου!")
            return

    



def group_menu(): #Ένα γενικό μενου για τις διάφορες ενέργειες που μπορούν να γίνουν πάνω στα γκρουπ
    
    while True:
        print('Για να δείτε όλα τα γκρούπ πατήστε 1\nΓια να προσθέσετε νέο γκρούπ εκμάθησης πατήστε 2')
        ans =input()
                   
        if ans=='1':
            view_group()
        if ans=='2':
            insert_group()
        if ans==' ':
            return

def epipleon_menu(): #Ενα μενού για τις μη συχνές λειτουργίες της εφαρμογής μας
    
    while True:
        print('Για αλλαγή πληροφορίας γηπέδου πατήστε το 1')
        print('Για αλλαγή πληροφορίας ατόμου πατήστε το 2')
        ans =input()
                   
        if ans=='1':
            alter_gipedo()
        if ans=='2':
            alter_atomo()
        if ans==' ':
            return




def menu(): #Σε αυτό το μενού πρέπει να σχεδιάσουμε τις επιλογές
    print('Καλησπέρα!\n')
    while True:
        print('Για να κάνετε καινούργια κράτηση πατήστε το 1')
        print('Για να κάνετε αλλαγή σε κράτηση πατήστε το 2')
        print('Για να προσθέσετε καινούργιο παίκτη πατήστε το 3')
        print('Περισσότερες πληροφορίες για τα τουρνουά στο 4')
        print('Για να δείτε το πρόγραμμα πατήστε το 5')
        print('Περισσότερες πληροφορίες για τα γκρουπ εκμάθησης στο 6')
        print('Περισσότερες λειτουργίες στο 7')
        print('Για έξοδο πατήστε κενό και μετά enter')
        ans =input()
                   
        if ans=='1':
            kratisi()
        if ans=='2':
            change_kratisi()
        if ans=='3':
            insert_atomo()
        if ans=='4':
            tournoua_menu()
        if ans=='5':
            programma()
        if ans=='6':
            group_menu()
        if ans=='7':
            epipleon_menu()
        if ans==' ':
            return

def main():#Εδώ μέσα βάζεις όποια συνάρτηση θέλεις να γίνει.
    connect_to_db()
    menu()
    con.close()



if __name__=="__main__":
    main()
