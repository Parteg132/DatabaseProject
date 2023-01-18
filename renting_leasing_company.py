# julek renting leasing leasing company
from mysql.connector import connect, Error
import datetime
import random
import cars_brands_classes
import time

def localization():
    return (round(random.uniform(-180, 180), 5), round(random.uniform(-180, 180), 5))


def calculateKilometers(
        id_rent):  # liczy dlugosc trasy w km na podstawie wspolrzednych z wiersza renting o id = id_rent
    return random.randint(5, 50)


def calculateTime(end, start):
    # print("end: ",end,' start: ',start)
    time = end - start
    seconds = time.total_seconds()
    minutes = seconds // 60
    # print("delta: ",minutes)
    return minutes


def add_leasing_deal(connection):
    with connection.cursor() as cursor:
        leasing_company_id = int(input("Podaj id_leasing_company: "))
        month = int(input("Podaj dlugosc leasingu w miesiacach: "))
        monthly_price = int(input("Podaj miesieczny koszt: "))
        start_date = input("Podaj date rozpoczecia leasingu w formacie YYYY-MM-DD: ")

        addTechniqueStatement = "INSERT INTO leasing (leasing_company_id,month,monthly_price,start_date) VALUES (%s, %s, %s, %s)"
        val = (leasing_company_id, month, monthly_price, start_date)
        cursor.execute(addTechniqueStatement, val)
        connection.commit()


def add_leasing_company(connection):
    with connection.cursor() as cursor:
        name = input("Podaj nazwe leasingodawcy: ")
        address = input("Podaj adres: ")
        phone_number = input("Podaj telefon kontaktowy: ")
        bank_number = input("Podaj numer konta: ")
        addTechniqueStatement = "INSERT INTO leasing_company (name,address,phone_number,bank_number) VALUES (%s, %s, %s, %s)"
        val = (name, address, phone_number, bank_number)
        cursor.execute(addTechniqueStatement, val)
        connection.commit()


def start_renting(connection):
    with connection.cursor() as cursor:
        id_user = int(input("Podaj user_id: "))
        id_car = int(input("Podaj car_id: "))


        statement = """SELECT %s FROM %s WHERE %s = %s;"""
        tup = ('status', 'cars', 'id', id_car)
        l = statement % tup
        cursor.execute(l)
        result = cursor.fetchall()
        status = result[0][0]

        if status == "Ready_to_rent":
            time_start = datetime.datetime.now()
            status = 1
            route = localization()
            addTechniqueStatement = "INSERT INTO renting (id_user,id_car,time_start,status,route) VALUES (%s, %s,%s, %s, %s)"
            val = (id_user, id_car, time_start, status,str(route))
            cursor.execute(addTechniqueStatement, val)
            connection.commit()
        else:
            print("Auto niedostepne")
            time.sleep(1)


# auto wysyla lokalizacje przy kazdym skrecie
def update_route_info(connection):
    with connection.cursor() as cursor:
        ID = int(input("Podaj ID rentingu: "))
        route = localization()
        addTechniqueStatement = "update renting set route = CONCAT(route,%s) WHERE id=%s"
        val = (str(route), ID)
        cursor.execute(addTechniqueStatement, val)
        connection.commit()


def end_renting(connection):
    with connection.cursor() as cursor:
        ID = int(input("Podaj ID rentingu: "))

        statement = """SELECT %s FROM %s WHERE %s = %s;"""
        tup = ('status', 'renting', 'id', ID)
        l = statement % tup
        cursor.execute(l)
        result = cursor.fetchall()
        status = result[0][0]

        if status:
            statement = """SELECT %s FROM %s WHERE %s = %s;"""
            tup = ('id_car', 'renting', 'id', ID)
            l = statement % tup
            cursor.execute(l)
            result = cursor.fetchall()
            id_car = result[0][0]

            statement = """SELECT %s FROM %s WHERE %s = %s;"""
            tup = ('class_id', 'cars', 'id', id_car)
            l = statement % tup
            cursor.execute(l)
            result = cursor.fetchall()
            id_class = result[0][0]

            statement = """SELECT %s,%s,%s,%s,%s FROM %s WHERE %s = %s;"""
            tup = ('start_fee', 'minute_fee', 'kilometer_fee', 'stop_7_23', 'stop_23_7', 'classes', 'id', id_class)
            l = statement % tup
            cursor.execute(l)
            result = cursor.fetchmany()

            car_pricing_info = result[0]
            start_fee = car_pricing_info[0]
            kilometer_fee = car_pricing_info[2]
            minute_fee = car_pricing_info[1]
            stopCost = (car_pricing_info[3], car_pricing_info[4])

            statement = """SELECT %s FROM %s WHERE %s = %s;"""
            tup = ('time_start', 'renting', 'id', ID)
            l = statement % tup
            cursor.execute(l)
            time_start = cursor.fetchall()[0][0]
            # print("Time start: ",time_start)

            time_finished = datetime.datetime.now()
            time_stop = random.randint(0, 25)  # ilosc minut, te informacje dostaje od auta
            time_reservation = random.randint(0, 25)  # ilosc minut te informacje dostaje od auta
            status = 0

            route = localization()
            addTechniqueStatement = "update renting set route = CONCAT(route,%s) WHERE id=%s"
            val = (str(route), ID)
            cursor.execute(addTechniqueStatement, val)
            connection.commit()
            if time_finished.hour < 23:
                stopCost = stopCost[0]
            else:
                stopCost = stopCost[1]
            kmdriven = calculateKilometers(ID)
            timedriven = calculateTime(time_finished, time_start)
            # print("KM: ",kmdriven," time: ",timedriven," stop time: ",time_stop+time_reservation)


            statement = """SELECT %s FROM %s WHERE %s = %s;"""
            tup = ('id_user', 'renting', 'id', ID)
            l = statement % tup
            cursor.execute(l)
            result = cursor.fetchall()
            id_user = result[0][0]


            statement = """SELECT %s FROM %s WHERE %s = %s;"""
            tup = ('discount', 'users', 'id', id_user)
            l = statement % tup
            cursor.execute(l)
            result = cursor.fetchall()
            discount = result[0][0]


            cost = kmdriven * kilometer_fee + timedriven * minute_fee + (
                        time_stop + time_reservation) * stopCost + start_fee

            #print(cost)
            if discount:
                if cost>discount:
                    cost = cost - discount
                    #discount zmienic na 0
                    addTechniqueStatement = "update users set discount = %s WHERE id=%s;"
                    val = (0,id_user)
                    cursor.execute(addTechniqueStatement, val)
                    connection.commit()
                else:
                    
                    discount = discount-cost
                    addTechniqueStatement = "update users set discount = %s WHERE id=%s;"
                    val = (discount,id_user)
                    cursor.execute(addTechniqueStatement, val)
                    connection.commit()
            #print(discount, cost)
            addTechniqueStatement = "update renting set car_route = %s,time_finished=%s,time_stop=%s,time_reservation=%s,status=%s,cost=%s WHERE id=%s;"
            val = (kmdriven, time_finished, time_stop, time_reservation, status, cost, ID)
            cursor.execute(addTechniqueStatement, val)
            connection.commit()

            cars_brands_classes.update_car_info(connection, ID)

        else:
            print("Wynajem juz zakonczony")