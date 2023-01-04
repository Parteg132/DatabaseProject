from getpass import getpass
from mysql.connector import connect, Error

def print_menu():
  print("-----------------------------------------------")
  print("1. Print out all data in a table")
  print("2. Option 2")
  print("0. Quit")
  print("-----------------------------------------------")

def sqlconnection():
  try:
    with connect(
        host="localhost",
        user=input("Enter username: "),
        password=getpass("Enter password: "),
    ) as connection:
      print(connection)
      return True, connection
  except Error as e:
    print(e)
    return False, None

def main():
  try:
    with connect(
        host="localhost",
        user=input("Enter username: "),
        password=getpass("Enter password: "),
        database="carsharing"
    ) as connection:
      print(connection)

      while True:    
        print_menu()
        choice = input("Enter your choice: ")
        if choice == "1":
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
        # elif choice == "2":
        #   # Code for Option 2
        elif choice == "0":
          break
        else:
          print("Invalid choice. Please try again.")
  except Error as e:
    print(e)

if __name__ == "__main__":
  main()