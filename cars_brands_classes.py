import mysql.connector

connection = mysql.connector.connect(
  host="localhost",
  user="root",
  password="root",
  database = "carsharing"
)

def print_final_menu():
    print("-----------------------------------------------")
    print("1. Yes")
    print("2. No")
    print("-----------------------------------------------")

def print_status_menu():
    print("-----------------------------------------------")
    print("1. Ready_to_rent")
    print("2. Rented")
    print("3. Broken")
    print("4. Need_fuel")
    print("-----------------------------------------------")

def print_enginetype_menu():
    print("-----------------------------------------------")
    print("1. benzynowy")
    print("2. elektryczny")
    print("-----------------------------------------------")

def print_gearbox_menu():
    print("-----------------------------------------------")
    print("1. automatyczna")
    print("2. manualna")
    print("-----------------------------------------------")

def car_brand():
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM car_brands;")
        print("-----------------------------------------------")
        print(cursor.column_names)
        for i in cursor:
            print(i)
        print("-----------------------------------------------")
        cursor.execute("SELECT * FROM car_brands;")
        results = cursor.fetchall()
        id_list = [id[0] for id in results]
        while True:
            car_brand_id = int(input("Select car brand: "))
            if car_brand_id in id_list:
                return car_brand_id
            else:
                print("Invalid value. Please try again")

def car_class():
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM classes;")
        print("-----------------------------------------------")
        print(cursor.column_names)
        for i in cursor:
            print(i)
        print("-----------------------------------------------")
        cursor.execute("SELECT * FROM classes;")
        results = cursor.fetchall()
        id_list = [id[0] for id in results]
        while True:
            car_class_id = int(input("Select car class: "))
            if car_class_id in id_list:
                return car_class_id
            else:
                print("Invalid value. Please try again")

def car_status(fuel_battery_level):
    while True:
        print_status_menu()
        choice = input("Select car status: ")
        if choice == "1":
            carstatus = "Ready_to_rent"
            break
        elif choice == "2":
            carstatus = "Rented"
            break
        elif choice == "3":
            carstatus = "Broken"
            break
        elif choice == "4":
            carstatus = "Need_fuel"
            break
        else:
            print("Invalid choice. Please try again")
    if fuel_battery_level > 15 and carstatus == "Need_fuel":
        return "Ready_to_rent"
    elif fuel_battery_level < 15 and carstatus != "Broken" and carstatus != "Rented":
        return "Need_fuel"
    else:
        return carstatus

def car_enginetype():
    while True:
        print_enginetype_menu()
        choice = input("Select engine type: ")
        if choice == "1":
            return "benzynowy"
        elif choice == "2":
            return "elektryczny"
        else:
            print("Invalid choice. Please try again")

def car_gearboxtype():
    while True:
        print_gearbox_menu()
        choice = input("Select gearbox type: ")
        if choice == "1":
            return "automatyczna"
        elif choice == "2":
            return "manualna"
        else:
            print("Invalid choice. Please try again")

def add_cars(connection):
    with connection.cursor() as cursor:
        add_new_car = True
        while add_new_car:
            brand_id = car_brand()
            class_id = car_class()
            fuel_card = input("Enter fuel card number: ")
            #regex 00-000-0000
            VIN_number = input("Enter VIN number: ")
            #17 znakow, uppercase
            model = input("Enter car model: ")
            generation = input("Enter car generation: ")
            car_year = int(input("Enter car production year: "))
            # sprawdz czy int 1950-2023
            engine_type = car_enginetype()
            gearbox = car_gearboxtype()
            fuel_battery_level = int(input("Enter fuel/battery level: "))
            #sprawdz czy int 0-100
            car_mileage = int(input("Enter car mileage: "))
            status = car_status(fuel_battery_level)
            localization_x = input("Enter X coordinate of location: ")
            localization_y = input("Enter Y coordinate of location: ")

            query = "INSERT INTO cars (brand_id, class_id, fuel_card, VIN_number, model, generation, car_year, engine_type, gearbox, fuel_battery_level, car_mileage, status, localization_x, localization_y) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            data = (brand_id, class_id, fuel_card, VIN_number, model, generation, car_year, engine_type, gearbox, fuel_battery_level, car_mileage, status, localization_x, localization_y)
            cursor.execute(query, data)
            print("The car has been added")
            connection.commit()

            while True:
                print_final_menu()
                choice = input("Do you want to add another car?: ")
                if choice == "1":
                    break
                elif choice == "2":
                    add_new_car = False
                    break
                else:
                    print("Invalid choice. Please try again")


def add_brand(connection):
    with connection.cursor() as cursor:
        add_new_brand = True
        while add_new_brand:
            manufacturer = input("Enter the manufacturer: ")

            query = "INSERT INTO car_brands (manufacturer) VALUES (%s)"
            data = (manufacturer,)
            cursor.execute(query, data)
            print("The brand has been added")
            connection.commit()

            while True:
                print_final_menu()
                choice = input("Do you want to add another brand?: ")
                if choice == "1":
                    break
                elif choice == "2":
                    add_new_brand = False
                    break
                else:
                    print("Invalid choice. Please try again")

def add_class(connection):
    with connection.cursor() as cursor:
        add_new_class = True
        while add_new_class:
            name = input("Enter a class name: ")
            start_fee = float(input("Enter start fee: "))
            minute_fee = float(input("Enter minute fee: "))
            kilometer_fee = float(input("Enter kilometer fee: "))
            stop_7_23 = float(input("Enter stop fee between 7-23: "))
            stop_23_7 = float(input("Enter stop fee between 23-7: "))

            query = "INSERT INTO classes (name, start_fee, minute_fee, kilometer_fee, stop_7_23, stop_23_7) VALUES (%s, %s, %s, %s, %s, %s)"
            data = (name, start_fee, minute_fee, kilometer_fee, stop_7_23, stop_23_7)
            cursor.execute(query, data)
            print("The class has been added")
            connection.commit()

            while True:
                print_final_menu()
                choice = input("Do you want to add another class?: ")
                if choice == "1":
                    break
                elif choice == "2":
                    add_new_class = False
                    break
                else:
                    print("Invalid choice. Please try again")


#add_cars(connection) #dodanie auta
#add_brand(connection) #dodanie marki
#add_class(connection) #dodanie klasy
