import datetime

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
  
  query = "INSERT INTO document (id_user, api_url, exp_date, document_number, img_obverse, img_reverse, img_selfie) VALUES ('{}', 'example.com','{}','{}',LOAD_FILE('C:/Users/Marek/Desktop/Nauka/sem5/Bazy Danych/DatabaseProject/awers.jpg'),LOAD_FILE('C:/Users/Marek/Desktop/Nauka/sem5/Bazy Danych/DatabaseProject/Prawo_jazdy_rewers.png'),LOAD_FILE('C:/Users/Marek/Desktop/Nauka/sem5/Bazy Danych/DatabaseProject/selfie.jpeg'))".format(id, expDate, formNum)
  # DON'T KNOW WHY THIS QUERY ISN'T WORKING 
  with connection.cursor() as cursor:
    cursor.execute(query)
    connection.commit()

def addCred(connection, id):
  print("User is transfered to a 3rd party card storage")
  print("id:", id)