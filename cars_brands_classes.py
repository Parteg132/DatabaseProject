import re
import random

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

def car_brand(connection):
    with connection.cursor() as cursor:
        query = "SELECT * FROM car_brands;"
        cursor.execute(query)
        print("-----------------------------------------------")
        print(cursor.column_names)
        for i in cursor:
            print(i)
        print("-----------------------------------------------")
        cursor.execute(query)
        results = cursor.fetchall()
        id_list = [id[0] for id in results]
        while True:
            car_brand_id = int(input("Select car brand: "))
            if car_brand_id in id_list:
                return car_brand_id
            else:
                print("Invalid value. Please try again")

def car_class(connection):
    with connection.cursor() as cursor:
        query = "SELECT * FROM classes;"
        cursor.execute(query)
        print("-----------------------------------------------")
        print(cursor.column_names)
        for i in cursor:
            print(i)
        print("-----------------------------------------------")
        cursor.execute(query)
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
    if fuel_battery_level >= 15 and carstatus == "Need_fuel":
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
            brand_id = car_brand(connection)
            class_id = car_class(connection)
            while True:
                fuel_card = input("Enter a fuel card number in the format of 00-000-0000: ")
                match = re.search(r"^\d{2}-\d{3}-\d{4}$", fuel_card)
                if match:
                    break
                else:
                    print("Invalid fuel card number. Please try again.")
            while True:
                VIN_number = input("Please enter a 17 character VIN number: ").upper()
                if len(VIN_number) != 17:
                    print("Invalid string length. Please try again.")
                else:
                    break
            model = input("Enter car model: ")
            generation = input("Enter car generation: ")
            while True:
                car_year = int(input("Enter car production year between 1950 and 2023: "))
                try:
                    if car_year < 1950 or car_year > 2023:
                        raise ValueError
                except ValueError:
                    print("Invalid year. Please enter a valid year between 1950 and 2023.")
                    continue
                break
            engine_type = car_enginetype()
            gearbox = car_gearboxtype()
            while True:
                fuel_battery_level = int(input("Enter fuel/battery level [0-100]: "))
                try:
                    if fuel_battery_level < 0 or fuel_battery_level > 100:
                        raise ValueError
                except ValueError:
                    print("Invalid fuel/battery level. Please enter a valid fuel/battery level between 0 and 100.")
                    continue
                break
            car_mileage = int(input("Enter car mileage: "))
            status = car_status(fuel_battery_level)
            localization_x = float(input("Enter X coordinate of location: "))
            localization_y = float(input("Enter Y coordinate of location: "))

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

def edit_class(connection):
    with connection.cursor() as cursor:
        edit = True
        while edit:
            query = "SELECT * FROM classes;"
            cursor.execute(query)
            print("-----------------------------------------------")
            print(cursor.column_names)
            for i in cursor:
                print(i)
            print("-----------------------------------------------")
            cursor.execute(query)
            results = cursor.fetchall()
            id_list = [id[0] for id in results]
            class_id = int(input("Select class: "))
            if class_id in id_list:
                query2 = "SELECT * FROM classes WHERE id = %s"
                cursor.execute(query2, (class_id,))
                for i in cursor:
                    print(i)
                start_fee = float(input("Enter start fee: "))
                minute_fee = float(input("Enter minute fee: "))
                kilometer_fee = float(input("Enter kilometer fee: "))
                stop_7_23 = float(input("Enter stop fee between 7-23: "))
                stop_23_7 = float(input("Enter stop fee between 23-7: "))
                query3 = "UPDATE classes SET start_fee = %s, minute_fee = %s, kilometer_fee = %s, stop_7_23 = %s, stop_23_7 = %s WHERE id = %s"
                data = (start_fee, minute_fee, kilometer_fee, stop_7_23, stop_23_7, class_id)
                cursor.execute(query3, data)
                print("The class has been updated")
                connection.commit()
            else:
                print("Invalid value. Please try again")

            while True:
                print_final_menu()
                choice = input("Do you want to edit another class?: ")
                if choice == "1":
                    break
                elif choice == "2":
                    edit = False
                    break
                else:
                    print("Invalid choice. Please try again")

def update_car_info(connection, ID):
    with connection.cursor() as cursor:
        query = "SELECT %s FROM %s WHERE %s = %s"
        tup = ('car_route', 'renting', 'id', ID)
        cursor.execute(query % tup)
        results = cursor.fetchall()
        car_route = results[0][0]

        query2 = "SELECT %s FROM %s WHERE %s = %s;"
        tup2 = ('id_car', 'renting', 'id', ID)
        cursor.execute(query2 % tup2)
        results2 = cursor.fetchall()
        id_car = results2[0][0]

        query3 = "SELECT %s FROM %s WHERE %s = %s;"
        tup3 = ('fuel_battery_level', 'cars', 'id', id_car)
        cursor.execute(query3 % tup3)
        results3 = cursor.fetchall()
        fuel_battery_level = results3[0][0]

        query4 = "SELECT %s FROM %s WHERE %s = %s;"
        tup4 = ('car_mileage', 'cars', 'id', id_car)
        cursor.execute(query4 % tup4)
        results4 = cursor.fetchall()
        car_mileage = results4[0][0]

        new_car_mileage = int(car_mileage) + int(car_route)
        new_fuel_battery_level = int(fuel_battery_level) - ((random.uniform(8, 13)/100)*int(car_route))
        new_localization_x = random.uniform(-180, 180)
        new_localization_y = random.uniform(-180, 180)

        if new_fuel_battery_level >= 15:
            status = "Ready_to_rent"
        elif new_fuel_battery_level < 15:
            status = "Need_fuel"

        query5 = "UPDATE cars SET car_mileage = %s, fuel_battery_level = %s, status = %s, localization_x = %s, localization_y = %s WHERE id = %s"
        data = (new_car_mileage, new_fuel_battery_level, status, new_localization_x, new_localization_y, id_car)
        cursor.execute(query5, data)
        connection.commit()
