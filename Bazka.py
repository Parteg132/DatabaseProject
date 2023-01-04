import mysql.connector
import bcrypt
from datetime import datetime
#from time import localtime, strftime

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="root",
  database = "carsharing"
)
mycursor = mydb.cursor()

def email_creation():
  while True:
    # email = "nkoss@gmail.com"
    # email = "lura@hotmail.com"
    email= input("Wprowadź email: ").lower()
    #TEST REGEX FOR EMAIL!!!#

    sqlPswd = "SELECT email FROM users WHERE email = %s"
    mycursor.execute(sqlPswd, (email, ))
    myresult_0 = mycursor.fetchone()

    sqlPswd = "SELECT email FROM unverified_users WHERE email = %s"
    mycursor.execute(sqlPswd, (email, ))
    myresult_1 = mycursor.fetchone()

    if myresult_0 is not None:
      if email in myresult_0:
        print("Konto z podanym adresem mail już istnieje!")
        continue
    elif myresult_1 is not None:
      if email in myresult_1:
        print("Konto z podanym adresem mail już istnieje! [Potwierdź swój email!]")
        continue
    else:
      break
  
  return email

def login_creation():
  while True:
    # login = maxvideo
    login = 'bananek'
    #login= input("Wprowadź login: ")

    sqlPswd = "SELECT login FROM users WHERE login = %s"
    mycursor.execute(sqlPswd, (login, ))
    myresult_0 = mycursor.fetchone()

    sqlPswd = "SELECT login FROM unverified_users WHERE login = %s"
    mycursor.execute(sqlPswd, (login, ))
    myresult_1 = mycursor.fetchone()

    if myresult_0 is not None:
        if login in myresult_0:
          print("Podany login jest zajęty")
          continue
    elif myresult_1 is not None:
        if login in myresult_1:
          print("Podany login jest zajęty")
          continue
    
    else:
      break

  return login

def hash_password():
  #PASSWORD POLICY NEEDED!
  password = input('Hasło: ')
  bytes = password.encode('utf-8')
  salt = bcrypt.gensalt()
  hash = bcrypt.hashpw(bytes, salt)

  return hash, salt

def creating_account(): 
  email = email_creation()
  login = login_creation()
  hpass, salt = hash_password()
  url = 'example@com'
  #ttl = datetime.strptime(strftime("%Y-%m-%d %H:%M:%S", localtime()), "%Y-%m-%d %H:%M:%S")
  ttl = datetime.now()
  status = 0

  sqlFormula = "INSERT INTO unverified_users (email,login,password_hash,password_salt,url,ttl,status) VALUES (%s, %s, %s, %s, %s, %s, %s)" 
  data = (email,login,hpass,salt,url,ttl,status)

  mycursor.execute(sqlFormula, data)
  mydb.commit()

  print('[NA ADRES EMAIL ZOSTAŁ WYSŁANY LINK AKTYWACYJNY!]')

def email_verification(email = None):
  if email is None:
    email = input("Podaj adres email: ")

  sqlPswd = "SELECT url FROM unverified_users WHERE email = %s"
  mycursor.execute(sqlPswd, (email, ))
  myresult = mycursor.fetchone()

  print(f'''
  WERYFIKACJA
  Email: {email}
  URL: {myresult}
  ''')

  while True:
    print('[VERIFY] / [EXIT]')

    choice = input('Wybierz opcję: ').upper()
    if choice == 'VERIFY':

      query = "UPDATE unverified_users SET status = 1 WHERE email = %s"
      mycursor.execute(query,(email,))
      mydb.commit()

      print('Zweryfikowano adres email!')
      
      while True:
        print('[OK]')
        ch = input().upper()
        if ch == 'OK':
          break
      break 
    elif choice == 'EXIT':
      break

  print('Zaloguj się aby dokończyć zakładanie konta')

def refresh_users():
  query = "SELECT email, login, password_hash, password_salt FROM unverified_users WHERE status = 1"
  mycursor.execute(query)
  myresult = mycursor.fetchall()

  if myresult is not None:
    query = "INSERT INTO users (name,surname,street,city,phone_number,email,login,status,discount) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"

    for row in myresult:
      data = (None, None , None, None, None, row[0], row[1], 'Verified', 0 )
      # mycursor.execute(query, data)
      # mydb.commit()

      query2 = 'SELECT id FROM users WHERE email = %s'
      mycursor.execute(query2,(row[0],))
      myresult2=mycursor.fetchone()

      query3 = 'INSERT INTO credentials (id_user, email, login, password_hash, password_salt) VALUES (%s, %s, %s, %s, %s)'
      data =  (myresult2[0],row[0],row[1],row[2],row[3])
      # mycursor.execute(query3, data)
      # mydb.commit()
    
  else:
    pass
   

   

  








#creating_account()
#email_verification()
refresh_users()
mycursor.close()
mydb.close()
print("CLEAN")