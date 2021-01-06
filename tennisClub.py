import mysql.connector
from mysql.connector import errorcode

import os #Αυτό χρειάζεται για το dotenv. 
from os.path import join, dirname
from dotenv import load_dotenv #Το dotenv χρειάζεται για να μπορούμε να τραβάμε τα στοιχεία για τη βάση και να μην φαίνονται στο git
import datetime
from datetime import date
today = date.today()
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

def strtodate(string): #Μετατρέπει ένα str σε datetime ώστε να το στέλνουμε στη βάση
    #string format day - month - year
    string = string.split('-')
    year = int(string[0])
    month = int(string[1])
    day = int(string[2])
    return datetime.date(year,month,day)

def strtodate_time(string):
    #string format day - month - year  hour:minute
    string = string.split('-')
    month = int(string[1])
    day = int(string[0])
    string = string[2].split(' ')
    year = int(string[0])
    string  = string[1].split(':')
    minute = int(string[1])
    hour = int(string[0])
    return datetime.datetime(year,month,day,hour,minute)

def valid_date(str_in): #Έλεγχος για την εγκυρότητα μιας ημερομηνίας που έχει εισηχθεί σε μορφή YYYY-MM-DD
    try:
        newDate = datetime.datetime(year=int(str_in[0:4]),month=int(str_in[5:7]),day=int(str_in[8:10]))
        return True
    except ValueError:
        return False


def valid_date_loop(msg): #Loop μέχρι να εισηχθεί έγκυρη ημερομηνία
    while True:
        date = input(msg)
        if(valid_date(date)):
           return date                   
        else:
            print("Άκυρη ημερομηνία! Παρακαλώ να γίνει εισαγωγή έγκυρης ημερομηνίας σε μορφή YYYY-MM-DD.")


def available_gipedo(idn): #έλεγχος διαθεσιμότητας γηπέδου
    global curs,con   
    curs.execute("SELECT Id FROM `gipedo` WHERE Texn_Diathesimotita = '1';")
    result = curs.fetchall()
    available_ids = [i[0] for i in result]
    if(int(idn) not in available_ids):
        return False
    return True
    
def valid_gipedo(idn): #έλεγχος ύπαρξης γηπέδου στην βάση
    global curs,con

    curs.execute("SELECT MAX(Id) as MaxId FROM `gipedo`;")
    last_id=int(curs.fetchall()[0][0])  
    if (int(idn) > last_id):
        return False
    return True
    


def valid_gipedo_loop(msg):  #loop μέχρι να δοθεί Id διαθέσιμου γηπέδου  
  
    while True:
        idn = input(msg)
        if(not idn.isdigit() or not valid_gipedo(idn)):
           print("Άκυρο Id! Παρακαλώ να γίνει εισαγωγή έγκυρου Id γηπέδου.")                  
        elif (not available_gipedo(idn)):
            print("Αυτο το γήπεδο δεν είναι διαθέσιμο. Παρακαλώ να γίνει εισαγωγή διαθέσιμου Id γηπέδου.")
        else:
            return idn
   
    
    

            

def atomo_validate(values,a_type): #Μύνημα και έλεγχος για έγκριση εισαγωγής στοιχείων Παίκτη η Προπονητή
    if (a_type==1):
        str_type="παίκτη"
        valid4 = "Ημερομηνία Λήξης δελτίου Υγείας: "+values[9]
    elif(a_type==2):
        str_type="προπονητή"
        valid4 = "ΑΦΜ: "+values[10]+"\nOρομίσθιο: "+values[11]+ "\nΒιογραφικό: "+values[12]
    
    valid1 = "Να γίνει εισαγωγή "+str_type+" με τα ακόλουθα στοιχεία;\n AMKA: "+values[0]+"\nΌνομα: "+values[1]+" "+values[2]
    valid2 = "Τηλεφώνο: "+values[3]+"\nemail: "+values[4]
    valid3 = "Στοιχεία Κατοικείας:\nΟδός: "+values[5]+" Αριθμός: "+values[6]+"\nΠόλη: "+values[7]+"\nΤΚ: "+values[8]
    print(valid1+"\n"+valid2+"\n"+valid3+"\n"+valid4)
    ans = input("Πατήστε 1 για έγκριση.\n")
    return int(ans)
   
    

def insert_atomo(): #Εδώ γίνεται η εισαγωγή ενός παίκτη η προπονητή, κάνωντας χρήση των παραπάνω
    global curs,con
    values=[]
    while (True):
        try:
            choice = input('Πατήστε 1 για εισαγωγή παίκτη, 2 για εισαγωγή προπονητή\n')
            if choice!='1' and choice!='2':
                print('Άκυρη επιλογή!')
            else:
                
                atomo_AMKA = input('Να γίνει εισαγωγή του ΑΜΚΑ\n')
                atomo_eponimo = input('Να γίνει εισαγωγή του Επόνυμου:\n')
                atomo_onoma = input('Να γίνει εισαγωγή του Όνόματος:\n')
                atomo_tilefono = input('Να γίνει εισαγωγή του τηλεφώνου:\n')
                atomo_email=input('Να γίνει εισαγωγή του email:\n')
                atomo_odos=input('Να γίνει εισαγωγή της Οδός Κατοικείας του ατόμου:\n')
                atomo_arithmos = input('Να γίνει εισαγωγή του Αριθμού Κατοικείας του ατόμου:\n')
                atomo_poli=input('Να γίνει εισαγωγή της Πόλης:\n')
                atomo_TK=input('Να γίνει εισαγωγή του ΤΚ:\n')
                values.extend((atomo_AMKA,atomo_onoma,atomo_eponimo,atomo_tilefono,atomo_email,atomo_odos,atomo_arithmos,atomo_poli,atomo_TK))
                
                insert1 = "INSERT INTO atomo(AMKA,Eponimo,Onoma,Tilefono,Email,Odos,Arithmos,Poli,TK) VALUES('"+atomo_AMKA+"','"+atomo_eponimo+"','"+atomo_onoma+"','"+atomo_tilefono+"','"+atomo_email+"','"+atomo_odos+"','"+atomo_arithmos+"','"+atomo_poli+"','"+atomo_TK+"');"
                if choice=='1':
                    
                    paiktis_im = valid_date_loop('Να γίνει εισαγωγή της ημερομηνίας λήξης του δελτίου ηγείας σε μορφή YYYY-MM-DD:\n')
                    values.append(paiktis_im)
                    insert2 = "INSERT INTO paiktis(AMKA,Hm_Lixis_Deltiou) VALUES('"+atomo_AMKA+"','"+paiktis_im+"');"
                    
                elif choice=='2':
                    
                    prop_AFM = input('Να γίνει εισαγωγή του ΑΦΜ του εργαζόμενου:\n')
                    prop_wage = input('Να γίνει εισαγωγή του ορομισθίου του εργαζόμενου:\n')
                    prop_bio = input('Να γίνει εισαγωγή του βιογραφικού του εργαζόμενου:\n')
                    values.extend((prop_AFM,prop_wage,prop_bio))
                    insert2 = "INSERT INTO proponitis(AMKA,AFM,Oromisthio,Viografiko) VALUES('"+atomo_AMKA+"','"+prop_AFM+"','"+prop_wage+"','"+prop_bio+"');"

                v = atomo_validate(values,int(choice))
                if(v==1):
                    curs.execute(insert1)
                    curs.execute(insert2)
                    con.commit()
                    print('Εγινε η προσθήκη.')
                else:
                    print("Η εισαγωγή ακυρώθηκε.")
            ans = input('Θες να προσθέσουμε κάποιο άλλο άτομο; Αν ναι πατήστε 1, αλλιώς πατήστε κενό και μετά enter για επιστροφή στο αρχικό μενού!\n')
            if (ans!='1'):        
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





        


def kratisi():#Ελεγχος για ΑΜΚΑ τηλ ή Επώνυμο του παίκτη. Με αυτόν τον τρόπο μπορούμε να κάνουμε εύκολη τη δουλειά του γραμματέα
    global curs,con
    ans = input("Βάλτε εδώ τον ΑΜΚΑ, το τηλέφωνο ή το Επώνυμο του Παίκτη.")
    if (ans.isdigit()): # Εδώ ελέγχω αν είναι νούμερο ή γράμματα. Ώστε να ξέρω τι μου δίνει, αν μου δίνει όνομα ή κάτι με νούμερα
        #Εχω κάτι με νούμερα. Πρέπει να ελέξω αν είναι ΑΜΚΑ ή τηλέφωνο. Αρα αν είναι 11 ή 10 ψηφία
        if (len(str(ans)) == 11):#Αυτό είναι το μέγεθος του ΑΜΚΑ. Εδώ ελέγχω αν έχω αυτόν τον ΑΜΚΑ στη βάση
            curs.execute("SELECT * FROM `atomo` WHERE AMKA='"+ans+"';")
            results=curs.fetchall()
            if (len(results) == 0):
                print("Δεν υπάρχει παίκτης με αυτό το αμκα. ")
                kratisi()
                exit()
            elif (len(results) == 1):
                print("Ο παίκτης είναι: ")
                print(results[0][1],results[0][2])
                inp = input("Σωστό. Ν(αι) ή Ο(χι): ")
                if (inp == "Ν" or inp == "N" or inp == "n" or inp == "ν"):#greek or engilsh
                    amka = results[0][0]
                    onoma = results[0][1]
                    eponymo = results[0][2]
                else:
                    kratisi()
                    exit()
        elif(len(str(ans)) == 10):#Αυτό είναι το μέγεθος του τηλεφώνου και ελέγχω αν το έχω στη βάση αλλά και πόσες φορές το έχω. Αν το έχω πάνω από μία δίνω επιλογές για το ποιον θέλει
            curs.execute("SELECT * FROM `atomo` WHERE Tilefono='"+ans+"';")
            results=curs.fetchall()
            if (len(results) == 0):
                print("Δεν υπάρχει παίκτης με αυτό το τηλέφωνο. ")
                kratisi()
                exit()
            elif (len(results) == 1):
                print("Ο παίκτης είναι: ")
                print(results[0][1],results[0][2])
                inp = input("Σωστό. Ν(αι) ή Ο(χι): ")
                if (inp == "Ν" or inp == "N" or inp == "n" or inp == "ν"):#greek or engilsh
                    amka = results[0][0]
                    onoma = results[0][1]
                    eponymo = results[0][2]
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
                selection = input("Αν δεν είναι κανένας πατήστε κενό και μετά enter ")
                if (selection == " " or selection == ""):
                    kratisi()
                    exit()
                elif (selection.isdigit()):
                    amka = results[int(selection)][0]
                    onoma = results[int(selection)][1]
                    eponymo = results[int(selection)][2]

    else:
        #Εχω όνομα αρα κάνω αντίστοιχο query. Κάνω ελέγχους αν είναι πάνω από ένας με αυτό το όνομα
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
            if (inp == "Ν" or inp == "N" or inp == "n" or inp == "ν"):#greek or engilsh
                amka = results[0][0]
                onoma = results[0][1]
                eponymo = results[0][2]
                
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
                onoma = results[int(selection)][1]
                eponymo = results[int(selection)][2]

    print("Η κράτηση θα γίνει για : ",onoma,eponymo)
    print("Για πότε θέλετε να γίνει κράτηση;")
    print("Σε μορφή χρονιά-μήνας-ημέρα.")
    print("πχ σήμερα έχουμε:",today)
    input_date = date_check_for_kratisi()#Γίνεται έλεγχος για την εγκυρότητα της ημερομηνίας
    print("Η κράτηση θα γίνει για ",input_date)
    now = datetime.datetime.now()
    current_time = now.strftime("%H:%M")
    print("Η ώρα πρέπει να είναι σε μορφή ",current_time)
    input_time = input("Τι ώρα θέλετε;")# Θα αλλάξει για να γίνεται έλεγχος εγκυρότητας 
    input_diarkeia = input("Πόσες ώρες;")#  Θέλει συζήτηση αυτό
    kostos = "0"
    #Εδώ χρειάζεται να γίνεται έλεγχος για τη διαθεσιμότητα των γηπέδων. Πρέπει να το αλλάξουμε αλλά για τώρα 5/01/2021 09:09 θα το αφήσω ως εξής
    #Απλώς να ρωτάει σε ποιο γήπεδο θες
    print("Αυτά είναι όλα τα διαθέσιμα γήπεδα μας")

    curs.execute("SELECT * FROM `gipedo` WHERE Texn_Diathesimotita = '1'") 
    results=curs.fetchall()
    counter = 0
    for result in results:
        print("Enter ",counter,"for :",result[1], "Type of :",result[2])
        counter = counter + 1
    selected_option_for_gipedo = input("Για ποιο γήπεδο θέλετε;")
    selected_gipedo_id = results[int(selected_option_for_gipedo)][0]
    selected_gipedo_name = results[int(selected_option_for_gipedo)][1]
    print("Η κράτηση θα γίνει για:")
    print("Ονομα",onoma)
    print("Επώνυμο",eponymo)
    print("Ημερομηνία",input_date)
    print("Ώρα",input_time)
    print("Με διάρκεια",input_diarkeia)
    print("Κόστος",kostos)
    print("ID Γηπέδου: ",selected_gipedo_id," Όνομα Γηπέδου: ",selected_gipedo_name)
    final_datetime = str(input_date)+" "+str(input_time)
    print(final_datetime)
    inp = input("Σωστά; Ν(αι) ή Ο(χι): ")
    if (inp == "Ν" or inp == "N" or inp == "n" or inp == "ν"):#greek or engilsh
        query = "INSERT INTO `kratisi` (`Id`, `Imerominia`, `Diarkeia`, `Kostos`, `Id_Gipedou`, `Id_Paikti`, `Id_Group`, `Id_Agona`) VALUES (NULL, '"+str(final_datetime)+"', '"+str(input_diarkeia)+"', '"+str(kostos)+"', '"+str(selected_gipedo_id)+"', '"+str(amka)+"', NULL, NULL)"
        curs.execute(query)
        con.commit()
        print("Θεωρητικά έγινε η κράτηση")
    
    

    


    
    
            
        

    exit()

def date_check_for_kratisi():#Ελέγχω αν είναι πριν τη σημερινή ημερομηνία
    input_date = valid_date_loop('Να γίνει εισαγωγή της ημερομηνίας  σε μορφή YYYY-MM-DD:\n') 
    if (today <= strtodate(input_date)):
        print("Σωστή ημερομηνία")
    else:
        print("Δεν μπορείτε να κάνετε κράτηση σε παλαιότερη ημερομηνία από τη σημερινή")
        date_check_for_kratisi()
        exit()
    return (strtodate(input_date))

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

def insert_group(): #Συνάρτηση για εισαγωγή γκρουπ εκμάθησης στην βάση
    global curs,con
    while (True):
        try:
            group_onoma= input('Πως λέγεται το γκρουπ;\n')
            group_epipedo = input('Το επίπεδο του γκρουπ θα είναι:\n')
            group_im_enarxis = valid_date_loop('Να γίνει εισαγωγή της ημερομηνίας έναρξης σε μορφή YYYY-MM-DD:\n')       
            group_im_lixis = valid_date_loop('Να γίνει εισαγωγή της ημερομηνίας λήξης σε μορφή YYYY-MM-DD:\n')
            
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
            print("Αδυναμία προσθήκης γκρούπ!")
            return



def programma_on_date(): #εμφανίζει κρατήσεις για συγκεκριμένη ημερομηνία
    global curs,con
    date=valid_date_loop("Να εισηχθεί η επιθημητή ημερομηνία:\n")
    print("Οι κρατήσεις για την ημερομηνία "+date+" είναι:")
    result=prog_query_return(1,0,date)
    
    if(len(result)==0):
        print("Δέν υπάρχουν κρατήσεις για αυτήν την ημερομηνία.")
    else:
        for i in result:
            print(i)
    while(True):
        if(input("Πατήστε κενό και ENTER για επιστροφή.\n")):
            return


def programma_for_gipedo(): #εμφανίζει τις κρατήσεις για ένα συγκεκριμένο γήπεδο
    global curs,con
   
    view_gipedo(2)
    idn = valid_gipedo_loop("Εισάγετε τον αριθμό του ID του γηπέδου για το οποίο θέλετε να δείτε όλες τις κρατήσεις.\n")
    print("Οι συνολικές κρατήσεις για το γήπεδο αυτό είναι:")   
    result=prog_query_return(2,idn,"")
    
    if(len(result)==0):
        print("Δέν υπάρχουν κρατήσεις για αυτο το γήπεδο")
    else:
        for i in result:
            print(i)
    while(True):
        if(input("Πατήστε κενό και ENTER για επιστροφή.\n")):
            return
    
def programma_for_gipedo_on_date(): #εμφανίζει το πρόγραμμα για ενα γήπεδο σε σηγκεκριμένη μέρα
    global curs,con
   
    view_gipedo(2)
    idn = valid_gipedo_loop("Εισάγετε τον αριθμό του ID του γηπέδου για το οποίο θέλετε να δείτε όλες τις κρατήσεις.\n")
    date=valid_date_loop("Να εισηχθεί η επιθημητή ημερομηνία:\n")
    
    print("Οι συνολικές κρατήσεις για το γήπεδο αυτό για την ημερομηνία "+date+" είναι:")
    result=prog_query_return(3,idn,date)
    
    if(len(result)==0):
        print("Δέν υπάρχουν κρατήσεις για αυτον τον συνδιασμό")
    else:
        for i in result:
            print(i)
    while(True):
        if(input("Πατήστε κενό και ENTER για επιστροφή.\n")):
            return
    

def prog_query_return(mode,idn,date): #επιστρέφει τα αποτελέσματα για τα αντίστοιχα query. για χρήση στις απο πάνω συναρτήσεις αλλα και σε άλλα κομμάτια του προγράμματος
    global curs,con

    if(mode==1):
        select = "SELECT * FROM `kratisi` K WHERE  K.Imerominia >= '"+date+"' and K.Imerominia < DATE_ADD('"+date+"', INTERVAL 24 hour)"
    if(mode==2):
        select = "SELECT * FROM `kratisi` K WHERE  K.Id_Gipedou ='"+idn+"'"
    if(mode==3):
        select = "SELECT * FROM `kratisi` K WHERE  K.Id_Gipedou ='"+idn+"' AND K.Imerominia >= '"+date+"' and K.Imerominia < DATE_ADD('"+date+"', INTERVAL 24 hour)"
    
    curs.execute(select)    
    result=curs.fetchall()
    return result


        
       

def programma():
    global curs,con
    try:
        while (True):
            print('Για να δείτε όλες τις κρατήσεις για συγκεκριμένη ημερομηνία πατήστε 1\nΓια να δείτε όλες τις κρατήσεις για συγκεκριμένο γήπεδο πατήστε 2')
            print('Για να δείτε όλες τις κρατήσεις για συγκεκριμένη ημερομηνία μόνο για συγκεκριμένο γήπεδο πατήστε 3\n Για επιστροφή πατήστε κενό.')
            ans =input()
            if ans=='1':
                programma_on_date()
            if ans=='2':
                programma_for_gipedo()
            if ans=='3':
                programma_for_gipedo_on_date()
            if ans==' ':
                return
    except:
        print("Υπήρξε σφάλμα.")
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
