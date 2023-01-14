import datetime
from random import randrange
from mysql.connector import Error

def printData(connection):
  with connection.cursor() as cursor:
    cursor.execute("SHOW TABLES")
    for i in cursor:
      print(i)
    table = input("What table would you like to see?: ")
    query = "SELECT * FROM {};".format(table)
    cursor.execute(query)
    print("-----------------------------------------------")
    print(cursor.column_names)
    for i in cursor:
      print(i)
    print("-----------------------------------------------")

def addLic(connection, id):
  if id == None:
    print("You need to be logged in in order to add your driver's licence.")
    return 0
  try:
    with connection.cursor() as cursor:
      query = "SELECT id_user FROM document WHERE id_user = '{}'".format(id)
      cursor.execute(query)
      result = cursor.fetchone()
      if result is not None:
        print("Document already in database.")
        return 0

      formNum = input("Please provide your drivers license's 8 digit form number: ").upper()
      print(formNum)
      while True:
        if len(formNum) != 8:
          formNum = input("Incorrect number, try again: ").upper()
        else:
          break

      while True:
        try:
          year = int(input('Enter a year: '))
          month = int(input('Enter a month: '))
          day = int(input('Enter a day: '))

          expDate = datetime.date(year, month, day)
          print("date:", expDate)
          print("date now:", datetime.date.today())
          if expDate <= datetime.date.today():
            raise Exception
          break
        except:
          print("Wrong date format, try again.")  

      i = randrange(100)
      if i <= 85:
        query1 = "INSERT INTO document (id_user, api_url, exp_date, document_number, ext_checker_info, img_obverse, img_reverse, img_selfie) VALUES ('{}', 'example.com','{}','{}','B',LOAD_FILE('C:/Users/Marek/Desktop/Nauka/sem5/Bazy Danych/DatabaseProject/awers.jpg'),LOAD_FILE('C:/Users/Marek/Desktop/Nauka/sem5/Bazy Danych/DatabaseProject/Prawo_jazdy_rewers.png'),LOAD_FILE('C:/Users/Marek/Desktop/Nauka/sem5/Bazy Danych/DatabaseProject/selfie.jpeg'))".format(id, expDate, formNum)
        query2 = "UPDATE users SET status = 'B' WHERE id = '{}'".format(id)
        
        cursor.execute(query1)
        cursor.execute(query2)
        connection.commit()
        print("Your document have been verified, you have a B type driver's licence")
      elif i > 85 and i <= 95:
        query1 = "INSERT INTO document (id_user, api_url, exp_date, document_number, ext_checker_info, img_obverse, img_reverse, img_selfie) VALUES ('{}', 'example.com','{}','{}','B1',LOAD_FILE('C:/Users/Marek/Desktop/Nauka/sem5/Bazy Danych/DatabaseProject/awers.jpg'),LOAD_FILE('C:/Users/Marek/Desktop/Nauka/sem5/Bazy Danych/DatabaseProject/Prawo_jazdy_rewers.png'),LOAD_FILE('C:/Users/Marek/Desktop/Nauka/sem5/Bazy Danych/DatabaseProject/selfie.jpeg'))".format(id, expDate, formNum)
        query2 = "UPDATE users SET status = 'B1' WHERE id = '{}'".format(id)
        
        cursor.execute(query1)
        cursor.execute(query2)
        connection.commit()
        print("Your document have been verified, you have a B1 type driver's licence")
      else:
        print("Unfortunately, you don't have a valid Driver's License.")
        return 0
  except Error as e:
    print(e)
  

def addCred(connection, id):
  if id == None:
    print("You need to be logged in in order to add your driver's licence.")
    return 0
  try:
    with connection.cursor() as cursor:
      print("User is transfered to a 3rd party card storage/payment site which returns a value token that enables us to bill the user by issuing a payment request to that 3rd party card storage/payment site.")
      query = "SELECT id_user FROM payment WHERE id_user = '{}'".format(id)
      cursor.execute(query)
      result = cursor.fetchone()
      if result is not None:
        while True:
            ch = input("Credit card already in database, do you want to add a different one? [Y/N] (this will delete your former credit card!).").upper()
            if ch == 'Y':
              cursor.execute("DELETE FROM carsharing.payment WHERE (id_user = '{}')".format(id))
              break
            if ch == 'N':
              return 0
      
      print("After user fills in card details, the site returns limited information to our application:")
      lastDigits = input("Last 4 digits: ")
      pro = input("provider: ")
      token = input("token: ")
      while True:
        try:
          year = int(input('Enter a year: '))
          month = int(input('Enter a month: '))
          day = int(input('Enter a day: '))

          expDate = datetime.date(year, month, day)
          print("date:", expDate)
          print("date now:", datetime.date.today())
          if expDate <= datetime.date.today():
            raise Exception
          break
        except:
          print("Wrong date format, try again.") 

      query = "INSERT INTO payment (id_user, card_last_digits, provider, payment_token, exp_date) VALUES ('{}', '{}', '{}', '{}', '{}')".format(id, lastDigits, pro, token, expDate)
      cursor.execute(query)
      connection.commit()
  except Error as e:
    print(e)