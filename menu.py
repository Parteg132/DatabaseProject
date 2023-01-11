from getpass import getpass
from mysql.connector import connect, Error

import userModule
import docPay
import renting_leasing_company
import cars_brands_classes

def print_menu():
  print("-----------------------------------------------")
  print("1. Print out all data in a table")
  print("2. Registration")
  print("3. Email verification")
  print("4. Log in")
  print("5. Refresh user database")
  print("6. Add your drivers licence")
  print("7. Add your credit card")
  print("8. Start renting")
  print("9. Update renting info")
  print("10. End renting")
  print("11. Add leasing info")
  print("12. Add leasing company")
  print("13. Add a new car")
  print("14. Add a new brand")
  print("15. Add a new class")
  print("16. Edit class")
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
          userModule.log_in(connection)
        elif choice == "5":
          userModule.refresh_users(connection)
        elif choice == "6":
          docPay.addLic(connection)
        elif choice == "7":
          docPay.addCred(connection)
        elif choice == "8":
          renting_leasing_company.start_renting(connection)
        elif choice == "9":
          renting_leasing_company.update_route_info(connection)
        elif choice == "10":
          renting_leasing_company.end_renting(connection)
        elif choice == "11":
          renting_leasing_company.add_leasing_deal(connection)
        elif choice == "12":
          renting_leasing_company.add_leasing_company(connection)
        elif choice == "13":
          cars_brands_classes.add_cars(connection)
        elif choice == "14":
          cars_brands_classes.add_brand(connection)
        elif choice == "15":
          cars_brands_classes.add_class(connection)
        elif choice == "16":
          cars_brands_classes.edit_class(connection)
        elif choice == "0":
          break
        else:
          print("Invalid choice. Please try again.")
  except Error as e:
    print(e)

if __name__ == "__main__":
  main()
