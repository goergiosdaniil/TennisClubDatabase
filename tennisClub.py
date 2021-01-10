import mysql.connector
from mysql.connector import errorcode
from prettytable import PrettyTable
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
   
def str_len_check(word_in,mode): #έλεγχος για ΑΜΚΑ (mode 1) τηλέφωνο (mode 2) ΑΦΜ (mode 3)  ΤΚ (mode 4) η  αριθμός κατοικείας (mode 5)
    #Ακόμα πιο σημαντικός έλεγχος για τον ΑΜΚΑ αν υπάρχει ήδη από άλλο χρήστη ή όχι
    global curs,con
    if mode==1:
        if len(word_in)==11 and word_in.isdigit():
            query= "SELECT * FROM atomo WHERE AMKA='"+word_in+"';"
            curs.execute(query)
            results = curs.fetchall()
            if (len(results) == 0):  
                return True
            elif (len(results) == 1):
                print("Αυτό το ΑΜΚΑ υπάρχει στη βάση μας. Δεν γίνεται δύο διαφορετικά άτομα να έχουν το ίδιο αμκα")

            
    if mode==2:
        if len(word_in)==10 and word_in.isdigit():
            return True
    if mode==3:
        if len(word_in)==9 and word_in.isdigit():
            return True
    if mode==4:
        if len(word_in)==5 and word_in.isdigit():
            return True
    if mode==5:
        if word_in.isdigit():
            return True
    return False
    
    
def str_len_check_loop(msg,mode):
    if(mode==1):
        inp = " AMKA"
    elif (mode==2):
        inp =" τηλέφωνο"
    elif (mode==3):
        inp =" ΑΦΜ"
    elif (mode==4):
        inp ="ς ΤΚ"
    elif (mode==5):
        inp ="ς αριθμός κατοικείας."
    while True:
        word_in = input(msg)
        if(str_len_check(word_in,mode)):
           return word_in                   
        else:
            print("Άκυρο"+inp+" ! Παρακαλώ να γίνει εισαγωγή έγκυρου αριθμού.")
    
    
    

            

def atomo_validate(values,a_type): #Μύνημα και έλεγχος για έγκριση εισαγωγής στοιχείων Παίκτη η Προπονητή
    if (a_type==1):
        str_type="παίκτη"
        valid4 = "Ημερομηνία Λήξης δελτίου Υγείας: "+values[9]
    elif(a_type==2):
        str_type="προπονητή"
        valid4 = "ΑΦΜ: "+values[9]+"\nOρομίσθιο: "+values[10]+ "\nΒιογραφικό: "+values[11]
    
    valid1 = "Να γίνει εισαγωγή "+str_type+" με τα ακόλουθα στοιχεία;\n AMKA: "+values[0]+"\nΌνομα: "+values[1]+" "+values[2]
    valid2 = "Τηλεφώνο: "+values[3]+"\nemail: "+values[4]
    valid3 = "Στοιχεία Κατοικείας:\nΟδός: "+values[5]+" Αριθμός: "+values[6]+"\nΠόλη: "+values[7]+"\nΤΚ: "+values[8]
    print(valid1+"\n"+valid2+"\n"+valid3+"\n"+valid4)
    ans = input("Πατήστε 1 για έγκριση.\n")
    return int(ans)
   
    

def insert_atomo(pre_AMKA,pre_eponimo,pre_tilefono,mode,tourmode): #Εδώ γίνεται η εισαγωγή ενός παίκτη η προπονητή, κάνωντας χρήση των παραπάνω
    #mode==0: έρχομαι απο αρχικό μενου, χωρίς κανένα στοιχείο
    #mode==1 έχω είδη ΑΜΚΑ, mode==2 έχω είδη επώνυμο, mode==3 έχω είδη τηλέφωνο
    #tourmode το προσέθεσα ώστε να μην δίνει τη δυνατότητα όταν είναι από το τουρνουά να βάζει και 2ο άτομο
    global curs,con
    values=[]
    while (True):
        try:
            if(mode==0):
                choice = input('Πατήστε 1 για εισαγωγή παίκτη, 2 για εισαγωγή προπονητή\n')
            else:
                choice='1'
            if choice!='1' and choice!='2':
                print('Άκυρη επιλογή!')
            else:
                if(mode!=1):
                    atomo_AMKA = str_len_check_loop('Να γίνει εισαγωγή του ΑΜΚΑ\n',1)
                else:
                    atomo_AMKA = pre_AMKA
                if(mode!=2):
                    atomo_eponimo = input('Να γίνει εισαγωγή του Επώνυμου:\n')
                else:
                    atomo_eponimo = pre_eponimo
                atomo_onoma = input('Να γίνει εισαγωγή του Όνόματος:\n')
                if(mode!=3):
                    atomo_tilefono = str_len_check_loop('Να γίνει εισαγωγή του τηλεφώνου:\n',2)
                else:
                    atomo_tilefono=pre_tilefono
                atomo_email=input('Να γίνει εισαγωγή του email:\n')
                atomo_odos=input('Να γίνει εισαγωγή της Οδού Κατοικείας του ατόμου:\n')
                atomo_arithmos = str_len_check_loop('Να γίνει εισαγωγή του Αριθμού Κατοικείας του ατόμου:\n',5)
                atomo_poli=input('Να γίνει εισαγωγή της Πόλης:\n')
                atomo_TK=str_len_check_loop('Να γίνει εισαγωγή του ΤΚ:\n',4)
                values.extend((atomo_AMKA,atomo_onoma,atomo_eponimo,atomo_tilefono,atomo_email,atomo_odos,atomo_arithmos,atomo_poli,atomo_TK))
                
                insert1 = "INSERT INTO atomo(AMKA,Eponimo,Onoma,Tilefono,Email,Odos,Arithmos,Poli,TK) VALUES('"+atomo_AMKA+"','"+atomo_eponimo+"','"+atomo_onoma+"','"+atomo_tilefono+"','"+atomo_email+"','"+atomo_odos+"','"+atomo_arithmos+"','"+atomo_poli+"','"+atomo_TK+"');"
                if choice=='1':
                    
                    paiktis_im = valid_date_loop('Να γίνει εισαγωγή της ημερομηνίας λήξης του δελτίου ηγείας σε μορφή YYYY-MM-DD:\n')
                    values.append(paiktis_im)
                    insert2 = "INSERT INTO paiktis(AMKA,Hm_Lixis_Deltiou) VALUES('"+atomo_AMKA+"','"+paiktis_im+"');"
                    
                elif choice=='2':
                    
                    prop_AFM = str_len_check_loop('Να γίνει εισαγωγή του ΑΦΜ του εργαζόμενου:\n',3)
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
            if (tourmode == "tour"):#Αν είναι tournament τότε να μην ζητάει νέο παίκτη
                return
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


    while True:    
        ans = input("Βάλτε εδώ τον ΑΜΚΑ, το τηλέφωνο ή το Επώνυμο του Παίκτη.")
        if (ans.isdigit()): # Εδώ ελέγχω αν είναι νούμερο ή γράμματα. Ώστε να ξέρω τι μου δίνει, αν μου δίνει όνομα ή κάτι με νούμερα

            
            #Εχω κάτι με νούμερα. Πρέπει να ελέξω αν είναι ΑΜΚΑ ή τηλέφωνο. Αρα αν είναι 11 ή 10 ψηφία            
            if (len(str(ans)) == 11):#Αυτό είναι το μέγεθος του ΑΜΚΑ. Εδώ ελέγχω αν έχω αυτόν τον ΑΜΚΑ στη βάση
                curs.execute("SELECT * FROM `atomo` WHERE AMKA='"+ans+"';")
                results=curs.fetchall()
                
                if (len(results) == 0):
                    
                    print("Δεν υπάρχει παίκτης με αυτό το αμκα. Να γίνει προσθήκη νεου ατόμου με αυτό το στοιχείο; ")
                    inp = input("Πατήστε Ν για ναι, άλλο κουμπί για όχι: ")
                    if(inp=="Ν" or inp=="N"):
                        insert_atomo(ans,"","",1,"")
                    continue                    
                elif (len(results) == 1):
                    print("Ο παίκτης είναι: ")
                    print(results[0][1],results[0][2])
                    inp = input("Σωστό; Ν(αι) ή Ο(χι): ")
                    if (inp == "Ν" or inp == "N" or inp == "n" or inp == "ν"):#greek or engilsh
                        amka = results[0][0]
                        onoma = results[0][1]
                        eponymo = results[0][2]
                    else:
                        continue
                kratisi_insert(amka,onoma,eponymo)
            #Αυτό είναι το μέγεθος του τηλεφώνου και ελέγχω αν το έχω στη βάση αλλά και πόσες φορές το έχω. Αν το έχω πάνω από μία δίνω επιλογές για το ποιον θέλει               
            elif(len(str(ans)) == 10):#Αυτό είναι το μέγεθος του τηλεφώνου και ελέγχω αν το έχω στη βάση αλλά και πόσες φορές το έχω. Αν το έχω πάνω από μία δίνω επιλογές για το ποιον θέλει
                curs.execute("SELECT * FROM `atomo` WHERE Tilefono='"+ans+"';")
                results=curs.fetchall()
                if (len(results) == 0):
                    print("Δεν υπάρχει παίκτης με αυτό το τηλέφωνο. Να γίνει προσθήκη νεου ατόμου με αυτό το στοιχείο; ")
                    inp = input("Πατήστε Ν για ναι, άλλο κουμπί για όχι: ")
                    if(inp=="Ν" or inp=="N"):
                        insert_atomo("","",ans,3,"")
                    continue
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
                        continue
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
                        continue
                    elif (selection.isdigit()):
                        amka = results[int(selection)][0]
                        onoma = results[int(selection)][1]
                        eponymo = results[int(selection)][2]
                kratisi_insert(amka,onoma,eponymo)

        else:
            #Εχω όνομα αρα κάνω αντίστοιχο query. Κάνω ελέγχους αν είναι πάνω από ένας με αυτό το όνομα
            eponimo= ans.capitalize()
            curs.execute("SELECT * FROM `atomo` WHERE Eponimo='"+eponimo+"';")
            results=curs.fetchall()
            if (len(results) == 0):            
                print("Δεν υπάρχει παίκτης με αυτό το επόνυμο. Να γίνει προσθήκη νεου ατόμου με αυτό το στοιχείο; ")
                inp = input("Πατήστε Ν για ναι, άλλο κουμπί για όχι: ")
                if(inp=="Ν" or inp=="N"):
                    insert_atomo("",ans,"",2,"")
                  
                continue
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
                    continue
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
                    continue
                elif (selection.isdigit()):
                    amka = results[int(selection)][0]
                    onoma = results[int(selection)][1]
                    eponymo = results[int(selection)][2]
            kratisi_insert(amka,onoma,eponymo)

        ans=input("Πατήστε Ν για να εισάγετε κι αλλη κράτηση, άλλο κουμπί για επιστροφή στο αρχικό μενού: ")
        if(ans!="Ν" or ans!="N" or ans!="n" or ans!="ν"):
            return
        
      

def kratisi_insert(amka,onoma,eponymo):
    global curs,con

    (input_date,input_time,input_diarkeia,kostos,gipedo_id,selected_gipedo_name) = kratisi_input(onoma,eponymo)
    final_datetime = str(input_date)+" "+str(input_time)
    confirm = kratisi_confirm(input_date,input_time,input_diarkeia,kostos,gipedo_id,selected_gipedo_name,onoma,eponymo,final_datetime)
    if(confirm):
        query = "INSERT INTO `kratisi` (`Id`, `Imerominia`, `Diarkeia`, `Kostos`, `Id_Gipedou`, `Id_Paikti`, `Id_Group`, `Id_Agona`) VALUES (NULL, '"+str(final_datetime)+"', '"+str(input_diarkeia)+"', '"+str(kostos)+"', '"+str(gipedo_id)+"', '"+str(amka)+"', NULL, NULL)"
        curs.execute(query)
        con.commit()
        
def display_kratisi(res):
    hour=str(res[1].hour)
    minute=str(res[1].minute)
    if(len(hour)==1):
        hour="0"+hour
    if(len(minute)==1):
        minute="0"+minute
    print("ID Κράτησης: "+str(res[0])+" Γήπεδο ID: "+str(res[3])+" Ημερομηνία: " +str(res[1].year)+"-"+str(res[1].month)+"-"+str(res[1].day)+" Ώρα: "+hour+":"+minute+"  διάρκεια: "+str(res[2])+" ώρες")

    
    


def kratisi_input(onoma,eponymo):

    print("Η κράτηση θα γίνει για : ",onoma,eponymo)
    (input_date,input_time,input_diarkeia) = input_time_for_kratisi()
    kostos = str(int(input_diarkeia)*20) 
    (gipedo_id,selected_gipedo_name) = gipedo_selection()
    (check,res)=kratisi_overlap(input_date,input_time,input_diarkeia,gipedo_id)
    
    while check==True:
            
        print("Δεν μπορεί να γίνει η κράτηση για αυτο ο γήπεδο για αυτήν την ώρα, υπάρχει σύγκρουση με τις εξής κρατήσεις:")
        for i in res:
            display_kratisi(i)
        print("Για να δείτε το πρόγραμμα κρατήσεων για την ίδια μέρα και ώρα για πατήστε 1, ενώ μόνο για την ίδια μέρα πατήστε 2")
        print("Αλλιώς πατήστε οποιοδήποτε άλλο κουμπί.")
        ans=input()
        if(ans=='1'):
            res2 = prog_query_return(4,gipedo_id,input_date,input_time)
        if(ans=='2'):
            res2 = prog_query_return(1,gipedo_id,input_date,"")
        for i in res2:            
            display_kratisi(i)

        mode = input("Πατήστε 1 για να αλλάξετε μόνο την μέρα,ωρα και διάρκεια, 2 μόνο το γήπεδο.\n")
        if(mode=='1'):
            (input_date,input_time,input_diarkeia) = input_time_for_kratisi()
        if(mode=='2'):
            (gipedo_id,selected_gipedo_name) = gipedo_selection()
        
        (check,res)=kratisi_overlap(input_date,input_time,input_diarkeia,gipedo_id)    
    return (input_date,input_time,input_diarkeia,kostos,gipedo_id,selected_gipedo_name)


def input_time_for_kratisi():
    
    print("Για πότε θέλετε να γίνει κράτηση;")
    print("Σε μορφή χρονιά-μήνας-ημέρα.")
    print("πχ σήμερα έχουμε:",today)
    input_date_dt = date_check_for_kratisi('Να γίνει εισαγωγή της ημερομηνίας  σε μορφή YYYY-MM-DD:\n',"Δεν μπορείτε να κάνετε κράτηση σε παλαιότερη ημερομηνία από τη σημερινή",0,today)#Γίνεται έλεγχος για την εγκυρότητα της ημερομηνίας
    input_date = input_date_dt.strftime('%Y-%m-%d')
    print("Η κράτηση θα γίνει για ",input_date)
    now = datetime.datetime.now()
    current_time = now.strftime("%H:%M")
    print("Η ώρα πρέπει να είναι σε μορφή ",current_time)
    input_time = input("Τι ώρα θέλετε; ")# Θα αλλάξει για να γίνεται έλεγχος εγκυρότητας 
    input_diarkeia = input("Πόσες ώρες; ")#  Θέλει συζήτηση αυτό
    return(input_date,input_time,input_diarkeia)





def kratisi_confirm(input_date,input_time,input_diarkeia,kostos,selected_gipedo_id,selected_gipedo_name,onoma,eponymo,final_datetime):
    print("Η κράτηση θα γίνει για:")
    print("Ονομα",onoma)
    print("Επώνυμο",eponymo)
    print("Ημερομηνία",input_date)
    print("Ώρα",input_time)
    print("Με διάρκεια",input_diarkeia)
    print("Κόστος",kostos)
    print("ID Γηπέδου: ",selected_gipedo_id," Όνομα Γηπέδου: ",selected_gipedo_name)
    print(final_datetime)
    inp = input("Σωστά; Ν(αι) ή Ο(χι): ")
    if (inp == "Ν" or inp == "N" or inp == "n" or inp == "ν"):#greek or english
        return True
    return False
    


    
def gipedo_selection():
    global curs,con
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
    return(str(selected_gipedo_id),str(selected_gipedo_name))
    
    



def kratisi_overlap(date_in,time,dur,idn):
    #dur is in hours
    global curs,con
    start = time[:-3]
    end = str(int(time[:-3]) + int(dur))
    date = date_in+" 00:00:00"
    
    select = "SELECT * FROM `kratisi` K WHERE K.Id_Gipedou='"+idn+"' and (K.Imerominia >= DATE_ADD('"+date+"', INTERVAL "+start+" hour) and K.Imerominia < DATE_ADD('"+date+"', INTERVAL "+end+" hour));"
    curs.execute(select)    
    result=curs.fetchall()
    if(len(result)!=0):
        return (True,result)
    return (False,result)

   

def date_check_for_kratisi(msginput,msgoutput,compare,otherdate):#Ελέγχω αν είναι πριν τη σημερινή ημερομηνία. Με το compare ελέγχω αν είναι ένα κάνω σύγκριση με την ημερομηνία έναρξης

    while True:
        input_date = valid_date_loop(msginput)#'Να γίνει εισαγωγή της ημερομηνίας  σε μορφή YYYY-MM-DD:\n'
        if (today <= strtodate(input_date)):
            if (compare == '0'):

                print("Σωστή ημερομηνία")
                return (strtodate(input_date))
            else:
                print(strtodate(input_date),otherdate)
                if (strtodate(input_date)<otherdate):
                    print(strtodate(input_date),otherdate)
                    print("Δεν μπορεί η ημερομηνία λήξης να είναι πριν την ημερομηνία έναρξης")
                elif (strtodate(input_date)>otherdate):
                    print("Σωστή ημερομηνία")
                    return (strtodate(input_date))
        else:
            print(msgoutput)#"Δεν μπορείτε να κάνετε κράτηση σε παλαιότερη ημερομηνία από τη σημερινή"

    

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
        old_d=curs.fetchall()
        new_d = str(int(not old_d[0][0]))
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
    result=prog_query_return(1,0,date,"")
    
    if(len(result)==0):
        print("Δέν υπάρχουν κρατήσεις για αυτήν την ημερομηνία.")
    else:
        for i in result:
            display_kratisi(i)
    while(True):
        if(input("Πατήστε κενό και ENTER για επιστροφή.\n")):
            return


def programma_for_gipedo(): #εμφανίζει τις κρατήσεις για ένα συγκεκριμένο γήπεδο
    global curs,con
   
    view_gipedo(2)
    idn = valid_gipedo_loop("Εισάγετε τον αριθμό του ID του γηπέδου για το οποίο θέλετε να δείτε όλες τις κρατήσεις.\n")
    print("Οι συνολικές κρατήσεις για το γήπεδο αυτό είναι:")   
    result=prog_query_return(2,idn,"","")
    
    if(len(result)==0):
        print("Δέν υπάρχουν κρατήσεις για αυτο το γήπεδο")
    else:
        for i in result:
            display_kratisi(i)
    while(True):
        if(input("Πατήστε κενό και ENTER για επιστροφή.\n")):
            return
    
def programma_for_gipedo_on_date(): #εμφανίζει το πρόγραμμα για ενα γήπεδο σε σηγκεκριμένη μέρα
    global curs,con
   
    view_gipedo(2)
    idn = valid_gipedo_loop("Εισάγετε τον αριθμό του ID του γηπέδου για το οποίο θέλετε να δείτε όλες τις κρατήσεις.\n")
    date=valid_date_loop("Να εισηχθεί η επιθημητή ημερομηνία:\n")
    
    print("Οι συνολικές κρατήσεις για το γήπεδο αυτό για την ημερομηνία "+date+" είναι:")
    result=prog_query_return(3,idn,date,"")
    
    if(len(result)==0):
        print("Δέν υπάρχουν κρατήσεις για αυτον τον συνδιασμό")
    else:
        for i in result:
            display_kratisi(i)
    while(True):
        if(input("Πατήστε κενό και ENTER για επιστροφή.\n")):
            return
    

def prog_query_return(mode,idn,date,hour): #επιστρέφει τα αποτελέσματα για τα αντίστοιχα query. για χρήση στις απο πάνω συναρτήσεις αλλα και σε άλλα κομμάτια του προγράμματος
    global curs,con

    if(mode==1):
        select = "SELECT * FROM `kratisi` K WHERE  K.Imerominia >= '"+date+"' and K.Imerominia < DATE_ADD('"+date+"', INTERVAL 24 hour)"
    if(mode==2):
        select = "SELECT * FROM `kratisi` K WHERE  K.Id_Gipedou ='"+idn+"'"
    if(mode==3):
        select = "SELECT * FROM `kratisi` K WHERE  K.Id_Gipedou ='"+idn+"' AND K.Imerominia >= '"+date+"' and K.Imerominia < DATE_ADD('"+date+"', INTERVAL 24 hour)"
    if(mode==4):
        select = "SELECT * FROM `kratisi` K WHERE AND K.Imerominia = '"+date+" '"+hour+"'"    
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

def number_check(mode):#Ελέγχω αν επιλέγει μία από τις επιλογές που του δίνω

    while True:
        if (mode=="orio"):
            orio = input("4,8,16,32,64\n")
            if (int(orio) == 4 or int(orio) == 8 or int(orio) == 16 or int(orio) == 32 or int(orio) == 64):
                return (int(orio))
            else:
                print("Μπορείτε να βάλετε μόνο 4 ή 8 ή 16 ή 32 ή 64")
        elif (mode=="paiktes"):
            paiktes = input("Είδος τουρνουά. 1 για ατομικό 2 για ομαδικό\n")
            if (int(paiktes) == 1 or int(paiktes) == 2):
                return (int(paiktes))
            else:
                print("Μπορείτε να βάλετε μόνο 1 ή 2 ")

           

def create_tournament():#Εδώ δημιουργούμε το τουρνουά
    global curs,con
    print("Είστε έτοιμοι να δημιουργήσετε ένα τουρνουά")
    print("Πως θα λέγετε αυτό το τουρνουά;")
    onoma = input("")
    im_enarxis = date_check_for_kratisi('Να γίνει εισαγωγή της ημερομηνίας εναρξης σε μορφή YYYY-MM-DD:\n','Δεν μπορεί η ημερομηνία έναρξης να είναι νωρίτερα από σήμερα','0','')
    im_lixis = date_check_for_kratisi('Να γίνει εισαγωγή της ημερομηνίας λήξης σε μορφή YYYY-MM-DD:\n','Δεν μπορεί η ημερομηνία λήξης να είναι νωρίτερα από σήμερα','1',im_enarxis) 
    print("Πόσες ομάδες να μπουν στο τουρνουά")
    orio_omadon = number_check("orio") 
    paiktes_se_omada = number_check("paiktes") 
    confirm = tounament_confirm(onoma,im_enarxis,im_lixis,orio_omadon,paiktes_se_omada)
    if (confirm):
        query = "INSERT INTO `tournoua` (`Id`, `Onoma`, `Hm_Enarxis`, `Hm_Lixis`, `Orio_Omadon`, `Paiktes_se_omada`) VALUES (NULL, '"+onoma+"', '"+str(im_enarxis)+"', '"+str(im_lixis)+"', '"+str(orio_omadon)+"', '"+str(paiktes_se_omada)+"')"
        curs.execute(query)
        con.commit()
    ans=input("Πατήστε Ν για να εισάγετε κι αλλο τουρνουα, άλλο κουμπί για επιστροφή στο αρχικό μενού: ")
    if(ans!="Ν" or ans!="N"):
        return


def tounament_confirm(onoma,im_enarxis,im_lixis,orio_omadon,paiktes_se_omada):
    print("Τα στοιχεία του τουρνουά που πάτε να δημιουργήσετε είναι")
    print("Ονομα:",onoma)
    print("Ημερομηνία Έναρξης:",im_enarxis)
    print("Ημερομηνία Λήξης:",im_lixis)
    print("Οριο Ομάδων",orio_omadon)
    if (paiktes_se_omada == 1 ):
        print("Είδος Τουρνουά","Ατομικό")
    elif (paiktes_se_omada == 2 ):
        print("Είδος Τουρνουά","Ομαδικό")
    inp = input("Σωστά; Ν(αι) ή Ο(χι): ")
    if (inp == "Ν" or inp == "N" or inp == "n" or inp == "ν"):#greek or english
        return True
    return False
    
def show_tournament():
    global curs,con
    t = PrettyTable(['ID','Όνομα','Είδος','Έναρξη','Λήξη','Όριο ομάδων','Έχουν γραφτεί']) 
    query = " SELECT tournoua.Id, Onoma, Hm_Enarxis, Hm_Lixis, Orio_Omadon, Paiktes_se_omada, count(omada.Id) as Grammenes FROM `tournoua` INNER JOIN omada ON omada.Id_tournoua = tournoua.Id GROUP BY omada.Id_tournoua"
    eidos = ''
    curs.execute(query)
    results=curs.fetchall()
    for result in results:
        if (result[5] == 1):
            eidos = "Ατομικό"
        elif (result[5] == 2):
            eidos = "Ομαδικό"
        t.add_row([result[0],result[1],eidos,result[2],result[3],result[4],result[6]])
    print(t)

    return


def add_team_in_tournament():
    global curs,con
    #Αρχικά πρέπει να βρούμε αν θέλει ατομικό ή ομαδικό τουρνουά
    #Να ελέγχουμε αν μπορεί να γραφτεί στο τουρνουά που θέλει. Γιατί πχ μπορεί να έχει ήδη γίνει η κλήρωση
    print("Ενδιαφέρεται για ατομικό (1) ή ομαδικό (2) τουρνουά")
    eidos_noumero = input("")
    query = "SELECT tournoua.Id, Onoma, Hm_Enarxis, Hm_Lixis, Orio_Omadon, Paiktes_se_omada, count(omada.Id) as Grammenes FROM `tournoua` INNER JOIN omada ON omada.Id_tournoua = tournoua.Id WHERE Paiktes_se_omada = '"+eidos_noumero+"' GROUP BY omada.Id_tournoua  HAVING Orio_Omadon > Grammenes ;"
    curs.execute(query)
    results = curs.fetchall()
    t = PrettyTable(['ID','Όνομα','Είδος','Έναρξη','Λήξη','Όριο ομάδων','Έχουν γραφτεί']) 
    for result in results:
        if (result[5] == 1):
            eidos_lektiko = "Ατομικό"
        elif (result[5] == 2):
            eidos_lektiko = "Ομαδικό"
        t.add_row([result[0],result[1],eidos_lektiko,result[2],result[3],result[4],result[6]])
    print(t)
    selection = input("Επιλέξτε ποιο τουρνουά θέλετε. Αν τελικά δεν είναι κανένα πατήστε το κενό ")
    if (selection == " " or selection == ""):
        return
    elif (selection.isdigit()):#ΘΕΛΕΙ ΔΙΟΡΘΩΣΗ ΓΙΑΤΙ ΑΝ ΒΑΛΕΙΣ ΛΑΘΟΣ ΝΟΥΜΕΡΟ ΓΙΝΕΤΑΙ ΧΑΟΣ
        id_tournoua=selection
    #Να βρούμε αν είναι ήδη γραμμένος παίκτης. Να βρούμε ποιος είναι και να παίρνουμε το αμκα του
    if (eidos_noumero == "1"):
        player_amka_1 = add_player_in_omada()
        query = "INSERT INTO `omada` (`Id`, `AMKA_1`, `AMKA_2`, `Id_tournoua`) VALUES (NULL, '"+str(player_amka_1)+"', NULL, '"+str(id_tournoua)+"');"
    elif(eidos_noumero == "2"):
        player_amka_1 = add_player_in_omada()
        player_amka_2 = add_player_in_omada()
        query = "INSERT INTO `omada` (`Id`, `AMKA_1`, `AMKA_2`, `Id_tournoua`) VALUES (NULL, '"+str(player_amka_1)+"', '"+str(player_amka_2)+"', '"+str(id_tournoua)+"');"
    curs.execute(query)
    con.commit()#Κάποιο error handling

    #Να εκτυπώνει το όνομα του τουρνουά και τα ονόματα των παικτών. 
    #Με λίγο πιο περίπλοκη sql
    if (eidos_noumero == "1"):
        query = "SELECT tournoua.onoma, tournoua.Hm_Enarxis, atomo.onoma,atomo.eponimo FROM `omada` INNER JOIN tournoua ON omada.Id_tournoua = tournoua.Id INNER JOIN atomo ON atomo.AMKA = omada.AMKA_1 WHERE AMKA_1 = '"+str(player_amka_1)+"' AND Id_tournoua = '"+str(id_tournoua)+"';"
        curs.execute(query)
        results = curs.fetchall()
        t = PrettyTable(['Ονομα Τουρνουά','Ημ.Εναρξης','Παίκτης ']) 
        t.add_row([results[0][0],results[0][1],results[0][2]+" "+results[0][3]])
    elif(eidos_noumero == "2"):
        query = "SELECT tournoua.onoma, tournoua.Hm_Enarxis, atomo.Onoma, atomo.Eponimo, atomo2.Onoma, atomo2.Eponimo FROM `omada` INNER JOIN tournoua ON omada.Id_tournoua = tournoua.Id INNER JOIN atomo on atomo.AMKA = omada.AMKA_1 INNER JOIN atomo AS atomo2 on atomo2.AMKA = omada.AMKA_2 WHERE AMKA_1 = '"+str(player_amka_1)+"' AND AMKA_2 = '"+str(player_amka_2)+"' AND Id_tournoua = '"+str(id_tournoua)+"';"
        curs.execute(query)
        results = curs.fetchall()
        t = PrettyTable(['Ονομα Τουρνουά','Ημ.Εναρξης','Παίκτης 1','Παίκτης 2']) 
        t.add_row([results[0][0],results[0][1],results[0][2]+" "+results[0][3],results[0][4]+" "+results[0][5]])

    print(t)
    return

def add_player_in_omada():
    global curs,con
    while True:  
        ans = input("Βάλτε εδώ τον ΑΜΚΑ, το τηλέφωνο ή το Επώνυμο του Παίκτη.Αν ο παίκτης δεν έχει γραφτεί πατήστε το 0\n")
        if (ans == "0"):#Εδώ κατευθείαν προσθέτω νέο άτομο
            final_amka= str_len_check_loop('Να γίνει εισαγωγή του ΑΜΚΑ\n',1)
            insert_atomo(final_amka,"","",1,"tour")
            return final_amka
        elif(ans.isdigit()):#Εδώ ελέγχω αν είναι νούμερο ή γράμματα
            if (len(str(ans)) == 11):#Αυτό είναι το μέγεθος του ΑΜΚΑ. Εδώ ελέγχω αν έχω αυτόν τον ΑΜΚΑ στη βάση
                curs.execute("SELECT * FROM `atomo` WHERE AMKA='"+ans+"';")
                results=curs.fetchall()
                
                if (len(results) == 0):#ΛΕΙΤΟΥΡΓΕΙ ΣΩΣΤΑ
                    
                    print("Δεν υπάρχει παίκτης με αυτό το αμκα. Να γίνει προσθήκη νεου ατόμου με αυτό το στοιχείο; ")
                    inp = input("Πατήστε Ν για ναι, άλλο κουμπί για όχι: ")
                    if(inp=="Ν" or inp=="N"):
                        insert_atomo(ans,"","",1,"tour")
                    return (ans)                    
                elif (len(results) == 1):#Λειτουργεί σίγουρα
                    print("Ο παίκτης είναι: ")
                    print(results[0][1],results[0][2])
                    inp = input("Σωστό; Ν(αι) ή Ο(χι): ")
                    if (inp == "Ν" or inp == "N" or inp == "n" or inp == "ν"):#greek or engilsh
                        amka = results[0][0]
                        onoma = results[0][1]
                        eponymo = results[0][2]
                        return amka
                    else:
                        continue
                final_amka = amka
            
            elif(len(str(ans)) == 10):#Αυτό είναι το μέγεθος του τηλεφώνου και ελέγχω αν το έχω στη βάση αλλά και πόσες φορές το έχω. Αν το έχω πάνω από μία δίνω επιλογές για το ποιον θέλει
                curs.execute("SELECT * FROM `atomo` WHERE Tilefono='"+ans+"';")
                results=curs.fetchall()
                if (len(results) == 0):
                    print("Δεν υπάρχει παίκτης με αυτό το τηλέφωνο. Να γίνει προσθήκη νεου ατόμου ; ")
                    inp = input("Πατήστε Ν για ναι, άλλο κουμπί για όχι: ")
                    if(inp=="Ν" or inp=="N"):
                        final_amka= str_len_check_loop('Να γίνει εισαγωγή του ΑΜΚΑ\n',1)
                        insert_atomo(final_amka,"","",1,"tour")
                        return final_amka
                elif (len(results) == 1):
                    print("Ο παίκτης είναι: ")
                    print(results[0][1],results[0][2])
                    inp = input("Σωστό. Ν(αι) ή Ο(χι): ")
                    if (inp == "Ν" or inp == "N" or inp == "n" or inp == "ν"):#greek or engilsh
                        amka = results[0][0]
                        return amka
                    else:
                        continue
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
                        continue
                    elif (selection.isdigit()):
                        amka = results[int(selection)][0]
                        return amka
        else:
            #Εχω όνομα αρα κάνω αντίστοιχο query. Κάνω ελέγχους αν είναι πάνω από ένας με αυτό το όνομα
            eponimo= ans.capitalize()
            curs.execute("SELECT * FROM `atomo` WHERE Eponimo='"+eponimo+"';")
            results=curs.fetchall()
            if (len(results) == 0):            
                print("Δεν υπάρχει παίκτης με αυτό το επόνυμο. Να γίνει προσθήκη νεου ατόμου ; ")
                inp = input("Πατήστε Ν για ναι, άλλο κουμπί για όχι: ")
                if(inp=="Ν" or inp=="N"):
                    final_amka= str_len_check_loop('Να γίνει εισαγωγή του ΑΜΚΑ\n',1)
                    insert_atomo(final_amka,"","",1,"tour")
                    return final_amka   
                continue
            elif (len(results) == 1):
                print("Ο παίκτης είναι: ")
                print(results[0][1],results[0][2])
                inp = input("Σωστό. Ν(αι) ή Ο(χι): ")
                if (inp == "Ν" or inp == "N" or inp == "n" or inp == "ν"):#greek or engilsh
                    amka = results[0][0]
                    return  amka
                else:
                    continue
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
                    continue
                elif (selection.isdigit()):
                    amka = results[int(selection)][0]
                    return amka
        exit


def change_kratisi():
    alter_kratisi(1)



def alter_kratisi(mode):
    #mode==1 κράτηση ατόμου mode==2 κράτηση γκρουπ mode==3 κράτηση αγώνα
    if(mode==1):
        amka=select_apo_stoixeia()
        to_be_altered = find_kratisi_by_atomo(amka)       
    kratisi_update(to_be_altered)
    

    
##def find_kratisi_by_tournament():
##    print("Αυτά είναι τα Τουρνουά μας:")
##    show_tournament()
##    idn = input("Διαλέξτε το Id του γηπέδου που θέλετε να αλλάξουμε: ")
##    
##    curs.execute("SELECT * FROM `agonas` WHERE Id_Tournoua='"+idn+"';")
##    results=curs.fetchall()
##    
##    t = PrettyTable(['Id','Score','Id Ομάδας 1','Id Ομάδας 2','Id Τουρνουά']) 
##    for result in results:
##        t.add_row([result[0],result[1],result[2],result[3],result[4]])
##    print(t)
##    
##    ida = input("Για ποιόν αγώνα θέλετε να αλλάξετε κράτηση; Εισάγετε το Id του: ")
##    print("Αυτός ο αγώνας έχει τις εξής κρατήσεις:")
##    curs.execute("SELECT * FROM `kratisi` WHERE Id_Agona='"+ida+"';")
##    res2=curs.fetchall()
## 
##    for i in res2:
##        display_kratisi(i)
##    print(t)
##
##    idk = input("Εισάγετε το Id της κράτησης που θέλετε να αλλάξει: ")
##    return idk
    
    
    
def find_kratisi_by_atomo(amka):
    print("Αυτό το άτομο έχει κάνει τις εξής κρατήσεις: ")

    curs.execute("SELECT * FROM `kratisi` WHERE Id_Paikti='"+str(amka)+"';")
    res2=curs.fetchall()
 
    for i in res2:
        display_kratisi(i)

    idk = input("Εισάγετε το Id της κράτησης που θέλετε να αλλάξει: ")
    return idk
    

def kratisi_update(idk):

    while True:
        global curs,con
        ans = input("Πατήστε 1 για να διαγραφεί η κράτηση, 2 για να γίνει αλλαγή στοιχείων: ")
        if ans=='1':
            curs.execute("DELETE FROM `kratisi` WHERE Id='"+idk+"';")
            con.commit()
            print("Έγινε η διαγραφή. ")
        else:        
            table_for_kratisi(idk)
            ans = input("Ποιό απο τα στοιχεία θέλετε να αλλάξουν;\n")
            table_for_kratisi(idk)
            
            if(ans=='2'):
                (input_date,input_time,input_diarkeia,kostos,gipedo_id,selected_gipedo_name)=update_datetime_loop(1,idk)
                curs.execute("UPDATE `kratisi` SET Diarkeia='"+input_diarkeia+"' WHERE Id='"+idk+"'")
                final_datetime = str(input_date)+" "+str(input_time)
                curs.execute("UPDATE `kratisi` SET Imerominia='"+final_datetime+"' WHERE Id='"+idk+"'")
            if(ans=='1'):
                (input_date,input_time,input_diarkeia,kostos,gipedo_id,selected_gipedo_name)=update_datetime_loop(2,idk)
                curs.execute("UPDATE `kratisi` SET Id_Gipedou='"+gipedo_id+"' WHERE Id='"+idk+"'")
            con.commit()
            print("Έγινε η αλλαγή. ")
        ans=input("Πατήστε Ν για να εισάγετε κι αλλη κράτηση, άλλο κουμπί για επιστροφή στο αρχικό μενού: ")
        if(ans!="Ν" or ans!="N" or ans!="n" or ans!="ν"):
            return
        
    
        
        
    
    
        
def update_datetime_loop(mode,idk):
    
    (dt,dur,cost,gipedo_id) = extract_kratisi_values(idk)
    
    input_date,input_time=dt.strftime("%Y-%m-%d %H:%m").split()
    input_diarkeia=dur

    if(mode==1):
        (input_date,input_time,input_diarkeia) = input_time_for_kratisi()
    if(mode==2):
        (gipedo_id,selected_gipedo_name) = gipedo_selection()

    
    (check,res)=kratisi_overlap(input_date,input_time,input_diarkeia,gipedo_id)
    while check==True:
        print("Δεν μπορεί να γίνει η κράτηση για αυτο ο γήπεδο για αυτήν την ώρα, υπάρχει σύγκρουση με τις εξής κρατήσεις:")
        for i in res:
            display_kratisi(i)
            
        if(mode==1):           
           print("Επιλέξτε άλλη ώρα/ημερομηνία:")
           (input_date,input_time,input_diarkeia) = input_time_for_kratisi()
           cost=str(20*int(dur))
        if(mode==2):           
           print("Επιλέξτε άλλο Id γήπεδο")
           (gipedo_id,selected_gipedo_name) = gipedo_selection()
           
        (check,res)=kratisi_overlap(input_date,input_time,input_diarkeia,gipedo_id)
        
    return (input_date,input_time,input_diarkeia,cost,gipedo_id,"")
   
        
def extract_kratisi_values(idk):   
    curs.execute("SELECT * FROM `kratisi` WHERE Id='"+idk+"';")
    res=curs.fetchall()
    vals=res[0]
    #datetime,dur,cost,gipedo_id
    return (vals[1],str(vals[2]),str(vals[3]),str(vals[4]))
    

def table_for_kratisi(idk):
    (dt,dur,cost,gipedo_id) = extract_kratisi_values(idk)
    t = PrettyTable(['Επιλογή','Περιγραφή','Τιμή']) 
    t.add_row([1,"Γήπεδο","id γηπέδου "+str(gipedo_id)])
    t.add_row([2,"Ημερομηνία/ώρα/διάρκεια",dt.strftime("%Y-%m-%d %H:%m")+" "+str(dur)])
    print(t)



def alter_atomo(): #Να αλλάξει στοιχεία για έναν χρήστη
    global curs,con
    print("Θέλετε να αλλάξετε για έναν συγκεκριμένο χρήστη(1) ή θέλετε αρχικά να τους δείτε όλους;(2)")
    while True:
        ans =input()
        if ans=='1':
            amka = select_apo_stoixeia()
            show_the_person_with(amka)
        elif ans=='2':
            amka = select_apo_all_atoma()
            show_the_person_with(amka)
        elif ans==' ':
            return
        break


def select_apo_stoixeia():
    global curs,con
    while True:  
        ans = input("Βάλτε εδώ τον ΑΜΚΑ, το τηλέφωνο ή το Επώνυμο του Παίκτη.\n")
        if(ans.isdigit()):#Εδώ ελέγχω αν είναι νούμερο ή γράμματα
            if (len(str(ans)) == 11):#Αυτό είναι το μέγεθος του ΑΜΚΑ. Εδώ ελέγχω αν έχω αυτόν τον ΑΜΚΑ στη βάση
                curs.execute("SELECT * FROM `atomo` WHERE AMKA='"+ans+"';")
                results=curs.fetchall()
                if (len(results) == 0):#ΛΕΙΤΟΥΡΓΕΙ ΣΩΣΤΑ
                    print("Δεν υπάρχει παίκτης με αυτό το αμκα.  ")
                    continue                
                elif (len(results) == 1):#Λειτουργεί σίγουρα
                    print("Ο παίκτης είναι: ")
                    print(results[0][1],results[0][2])
                    inp = input("Σωστό; Ν(αι) ή Ο(χι): ")
                    if (inp == "Ν" or inp == "N" or inp == "n" or inp == "ν"):#greek or engilsh
                        amka = results[0][0]
                        return amka
                    else:
                        continue
            elif(len(str(ans)) == 10):#Αυτό είναι το μέγεθος του τηλεφώνου και ελέγχω αν το έχω στη βάση αλλά και πόσες φορές το έχω. Αν το έχω πάνω από μία δίνω επιλογές για το ποιον θέλει
                curs.execute("SELECT * FROM `atomo` WHERE Tilefono='"+ans+"';")
                results=curs.fetchall()
                if (len(results) == 0):
                    print("Δεν υπάρχει παίκτης με αυτό το τηλέφωνο. Να γίνει προσθήκη νεου ατόμου ; ")
                    inp = input("Πατήστε Ν για ναι, άλλο κουμπί για όχι: ")
                    if(inp=="Ν" or inp=="N"):
                        final_amka= str_len_check_loop('Να γίνει εισαγωγή του ΑΜΚΑ\n',1)
                        insert_atomo(final_amka,"","",1,"tour")
                        return final_amka
                elif (len(results) == 1):
                    print("Ο παίκτης είναι: ")
                    print(results[0][1],results[0][2])
                    inp = input("Σωστό. Ν(αι) ή Ο(χι): ")
                    if (inp == "Ν" or inp == "N" or inp == "n" or inp == "ν"):#greek or engilsh
                        amka = results[0][0]
                        return amka
                    else:
                        continue
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
                        continue
                    elif (selection.isdigit()):
                        amka = results[int(selection)][0]
                        return amka
        else:
            #Εχω όνομα αρα κάνω αντίστοιχο query. Κάνω ελέγχους αν είναι πάνω από ένας με αυτό το όνομα
            eponimo= ans.capitalize()
            curs.execute("SELECT * FROM `atomo` WHERE Eponimo='"+eponimo+"';")
            results=curs.fetchall()
            if (len(results) == 0):            
                print("Δεν υπάρχει παίκτης με αυτό το επόνυμο. Να γίνει προσθήκη νεου ατόμου ; ")
                inp = input("Πατήστε Ν για ναι, άλλο κουμπί για όχι: ")
                if(inp=="Ν" or inp=="N"):
                    final_amka= str_len_check_loop('Να γίνει εισαγωγή του ΑΜΚΑ\n',1)
                    insert_atomo(final_amka,"","",1,"tour")
                    return final_amka   
                continue
            elif (len(results) == 1):
                print("Ο παίκτης είναι: ")
                print(results[0][1],results[0][2])
                inp = input("Σωστό. Ν(αι) ή Ο(χι): ")
                if (inp == "Ν" or inp == "N" or inp == "n" or inp == "ν"):#greek or engilsh
                    amka = results[0][0]
                    return  amka
                else:
                    continue
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
                    continue
                elif (selection.isdigit()):
                    amka = results[int(selection)][0]
                    return amka
        exit


def select_apo_all_atoma():#Τους δείχνει όλους και επιστρέφει τον αμκα ενός συγκεκριμένου ατόμου
    global curs,con
    query = "SELECT * FROM atomo"
    curs.execute(query)
    results = curs.fetchall()
    t = PrettyTable(['Προσ.ID','ΑΜΚΑ', 'ΕΠΩΝΥΜΟ','ONOMA','ΤΗΛΕΦΩΝΟ','EMAIL','ΟΔΟΣ','ΑΡΙΘΜΟΣ','ΠΟΛΗ','ΤΚ'])    
    counter = 0
    for result in results:
        t.add_row([counter,result[0],result[1],result[2],result[3],result[4],result[5],result[6],result[7],result[8]])
        counter = counter + 1
    print(t)
    print("Ποιο είναι το προσωρινό id του παίκτη που θέλετε να αλλάξετε;")
    while True:
        id = input("")
        if (id.isdigit()):
            if(int(id)>=0 and int(id)<counter):
                amka = results[int(id)][0]
                break
            else:
                print("Δεν έχετε επιλέξει σωστό νούμερο")
        else:
            print("Δεν έχετε επιλέξει σωστό νούμερο")

    
    return amka


def show_the_person_with(amka):
    global curs,con
    query = "SELECT * FROM atomo WHERE amka= '"+str(amka)+"'"
    curs.execute(query)
    results = curs.fetchall()
    
    while (True):
        t = PrettyTable(['ΑΜΚΑ(1)', 'ΕΠΩΝΥΜΟ(2)','ONOMA(3)','ΤΗΛΕΦΩΝΟ(4)','EMAIL(5)','ΟΔΟΣ(6)','ΑΡΙΘΜΟΣ(7)','ΠΟΛΗ(8)','ΤΚ(9)'])    
        for result in results:
            t.add_row([result[0],result[1],result[2],result[3],result[4],result[5],result[6],result[7],result[8]])
        print(t)
        print("Ποιά στήλης θέλετε να αλλάξετε το περιεχόμενο;")
        column = input("")
        try:
            print("Η προηγούμενη τιμή ήταν: ", results[0][int(column)-1])
            if (column == "1"):
                new_value = str_len_check_loop('Να γίνει εισαγωγή του ΑΜΚΑ: ',1)
                amka= results[0][int(column)-1]
                column_name = "AMKA"
            elif (column == "2"):
                new_value = input('Να γίνει εισαγωγή του Επώνυμου: ')
                column_name = "Eponimo"
            elif (column == "3"):
                new_value = input('Να γίνει εισαγωγή του Όνόματος: ')
                column_name = "Onoma"
            elif (column == "4"):
                new_value = str_len_check_loop('Να γίνει εισαγωγή του τηλεφώνου: ',2)
                column_name = "Tilefono"
            elif (column == "5"):
                new_value = input('Να γίνει εισαγωγή του email: ')
                column_name = "Email"
            elif (column == "6"):
                new_value = input('Να γίνει εισαγωγή της Οδού Κατοικείας του ατόμου: ')
                column_name = "Odos"
            elif (column == "7"):
                new_value = str_len_check_loop('Να γίνει εισαγωγή του Αριθμού Κατοικείας του ατόμου: ',5)
                column_name = "Arithmos"
            elif (column == "8"):
                new_value = input('Να γίνει εισαγωγή της Πόλης:\n')
                column_name = "Poli"
            elif (column == "9"):
                new_value = str_len_check_loop('Να γίνει εισαγωγή του ΤΚ:\n',4)
                column_name = "TK"

            query = "UPDATE `atomo` SET `"+column_name+"` = '"+new_value+"' WHERE `atomo`.`AMKA` = "+str(amka)+""
            curs.execute(query)
            con.commit()

            break
        except:
                print("Λάθος Επιλογή")
                print(err)
                return
    if (column == "1"):
        query = "SELECT * FROM atomo WHERE amka= '"+new_value+"'"
    else:
        query = "SELECT * FROM atomo WHERE amka= '"+str(amka)+"'"
    
    curs.execute(query)
    results = curs.fetchall()
    print("Μετά την αλλαγή")
    t = PrettyTable(['ΑΜΚΑ', 'ΕΠΩΝΥΜΟ','ONOMA','ΤΗΛΕΦΩΝΟ','EMAIL','ΟΔΟΣ','ΑΡΙΘΜΟΣ','ΠΟΛΗ','ΤΚ'])    
    for result in results:
        t.add_row([result[0],result[1],result[2],result[3],result[4],result[5],result[6],result[7],result[8]])
    print(t)
    return 

def draw_tournament():
    print("Try")
    #

    


def tournoua_menu(): #Μενού για τα τουρνουά
    while True:
        print("Τουρνουά")
        t = PrettyTable(['Επιλογή','Περιγραφή',]) 
        t.add_row([0,"Δείτε όλα τα τουρνουά"])
        t.add_row([1,"Προσθέστε παίκες σε σε τουρνουά"])
        t.add_row([2,"Αλλαγή στοιχείων τουρνουά"])
        t.add_row([3,"Δημιουργήστε καινούργιο τουρνουά"])
        t.add_row([4,"Καταχώρυση αποτελέσματος αγώνα τουρνουά"])
        t.add_row([5,"Κάντε την κλήρωση τουρνουά"])
        t.add_row(["Κενό","Έξοδος"])
        print(t)
        print("Ανάλογα με το ποια λειτουργία θέλετε επιλέξτε το αντίστοιχο νούμερο")
        print("Αν θέλετε να κλείσετε την εφαρμογή πατήστε το κενό και μετά το enter")
        ans =input("Επιλογή: ")
        if ans=='0':
            show_tournament()    
        if ans=='1':
            add_team_in_tournament()
        if ans=='2':
            alter_tournament()
        if ans=='3':
            create_tournament()
        if ans=='4':
            insert_scores_in_tournament()
        if ans=='5':
            draw_tournament()

        if ans==' ':
            return



def menu(): #Σε αυτό το μενού πρέπει να σχεδιάσουμε τις επιλογές
    print('Καλησπέρα!\n')
    while True:
        print("Κεντρικό Μενού")
        t = PrettyTable(['Επιλογή','Περιγραφή',]) 
        t.add_row([1,"Νέα κράτηση"])
        t.add_row([2,"Αλλαγή σε κράτηση"])
        t.add_row([3,"Καινούργιο παίκτη"])
        t.add_row([4,"Τουρνουά"])
        t.add_row([5,"Πρόγραμμα"])
        t.add_row([6,"Γκρουπ Εκμάθησης"])
        t.add_row([7,"Περισσότερα"])
        t.add_row(["Κενό","Έξοδος"])
        print(t)
        print("Ανάλογα με το ποια λειτουργία θέλετε επιλέξτε το αντίστοιχο νούμερο")
        print("Αν θέλετε να κλείσετε την εφαρμογή πατήστε το κενό και μετά το enter")
        ans =input("Επιλογή: ")
                   
        if ans=='1':
            kratisi()
        if ans=='2':
            change_kratisi()
        if ans=='3':
            insert_atomo("","","",0,"")
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
