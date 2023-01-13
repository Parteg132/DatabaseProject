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

def addLic(connection, a):
    x = True
    formNum = input("Please provide your drivers license's form number: ").upper()
    print(formNum)
    while x == True:
      if len(formNum) != 8:
        formNum = input("Incorrect number, try again: ").upper()
      else:
        x = False
    
    x = True
    expDate = input("and expiry date (YYYY-MM-DD): ")
    print(datetime.datetime.strptime(expDate, '%Y-%m-%d'))
    while x == True:
      if datetime.datetime.strptime(expDate, '%Y-%m-%d') == False or datetime.datetime.strptime(expDate, '%Y-%m-%d') <= datetime.datetime.now():
        expDate = input("Incorrect date, try again (YYYY-MM-DD): ")
      else:
        x = False
    
    query = "INSERT INTO document (exp_date, document_number, img_obverse, img_reverse, img_selfie) VALUES ({},{},LOAD_FILE('awers.jpg'),LOAD_FILE('Prawo_jazdy_rewers.png'),LOAD_FILE('selfie.jpeg'))".format(expDate, formNum)
    with connection.cursor() as cursor:
      cursor.execute(query)

def addCred(connection, a):
    print("User is transfered to a 3rd party card storage")
    print("a:", a)