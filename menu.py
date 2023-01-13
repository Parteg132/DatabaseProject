from getpass import getpass
from mysql.connector import connect, Error

import userModule
import docPay

def print_menu():
  print("-----------------------------------------------")
  print("1. Print out all data in a table")
  print("2. Registration")
  print("3. Email verification")
  print("4. Log in")
  print("5. Refresh user database")
  print("6. Add your drivers licence")
  print("7. Add your credit card")
  print("0. Quit")
  print("-----------------------------------------------")

 #'''SPRAWDZIC refresh_users w userModule ! KOMENTARZ'''

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
          docPay.printData(connection)
        elif choice == "2":
          userModule.creating_account(connection)
        elif choice == "3":
          userModule.email_verification(connection)
        elif choice == "4":
          x = userModule.log_in(connection)
        elif choice == "5":
          userModule.refresh_users(connection)
        elif choice == "6":
          docPay.addLic(connection, x)
        elif choice == "7":
          docPay.addCred(connection, x)
        elif choice == "0":
          break
        else:
          print("Invalid choice. Please try again.")
  except Error as e:
    print(e)

if __name__ == "__main__":
  main()
