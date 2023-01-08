
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

def addLic(connection):
    print("holder")

def addCred(connection):
    print("User is transfered to a 3rd party card storage,")