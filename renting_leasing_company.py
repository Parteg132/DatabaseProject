#julek renting leasing leasing company
from mysql.connector import connect, Error
import datetime
import random

def localization():
	return (round(random.uniform(-180,180),5), round(random.uniform(-180,180),5))


def add_leasing_deal():
	leasing_company_is = 6
	month = 36
	monthly_price = 623
	start_date = '2023-01-10'

	addTechniqueStatement = "INSERT INTO leasing (leasing_company_id,month,monthly_price,start_date) VALUES (%s, %s, %s, %s)"
	val = (leasing_company_is,month,monthly_price,start_date)
	cursor.execute(addTechniqueStatement, val)
	connection.commit()



def add_leasing_company():
	name = "John CARS"
	address = "Aleje ujazdowskie 32"
	phone_number = '123321123'
	bank_number = '10920047622245892624399321'
	addTechniqueStatement = "INSERT INTO leasing_company (name,address,phone_number,bank_number) VALUES (%s, %s, %s, %s)"
	val = (name, address,phone_number,bank_number)
	cursor.execute(addTechniqueStatement, val)
	connection.commit()




def start_renting():
	id_user = 1
	id_car = 1
	time_start = datetime.datetime.now()

	status=1
	route = localization()
	addTechniqueStatement = "INSERT INTO renting (id_user,id_car,time_start,route) VALUES (%s, %s, %s, %s)"
	val = (id_user,id_car,time_start,str(route))
	cursor.execute(addTechniqueStatement, val)
	connection.commit()

def calculateKilometers(id_rent): #liczy dlugosc trasy w km na podstawie wspolrzednych z wiersza renting o id = id_rent
	return random.randint(5,50)

#auto wysyla lokalizacje przy kazdym skrecie
def update_route_info(): 
	ID =506
	route = localization()
	addTechniqueStatement = "update renting set route = CONCAT(route,%s) WHERE id=%s"
	val = (str(route),ID)
	cursor.execute(addTechniqueStatement, val)
	connection.commit()

def calculateTime(end,start):
	#print("end: ",end,' start: ',start)
	time = end-start
	seconds = time.total_seconds()
	minutes = seconds//60
	#print("delta: ",minutes)
	return minutes


def end_renting():
	ID =506

	statement = """SELECT %s FROM %s WHERE %s = %s;"""
	tup = ('id_car','renting','id',ID)
	l = statement % tup
	cursor.execute(l)
	result = cursor.fetchall()
	id_car = result[0][0]

	statement = """SELECT %s FROM %s WHERE %s = %s;"""
	tup = ('class_id','cars','id',id_car)
	l = statement % tup
	cursor.execute(l)
	result = cursor.fetchall()
	id_class = result[0][0]

	statement = """SELECT %s,%s,%s,%s,%s FROM %s WHERE %s = %s;"""
	tup = ('start_fee','minute_fee','kilometer_fee','stop_7_23','stop_23_7','classes','id',id_class)
	l = statement % tup
	cursor.execute(l)
	result = cursor.fetchmany(size=9)

	car_pricing_info = result[0]
	start_fee = car_pricing_info[0]
	kilometer_fee = car_pricing_info[2]
	minute_fee = car_pricing_info[1]
	stopCost = (car_pricing_info[3],car_pricing_info[4])

	statement = """SELECT %s FROM %s WHERE %s = %s;"""
	tup = ('time_start','renting', 'id',ID)
	l = statement % tup
	cursor.execute(l)
	time_start = cursor.fetchall()[0][0]
	#print("Time start: ",time_start)
	
	time_finished = datetime.datetime.now()
	time_stop = random.randint(0,25)	#ilosc minut, te informacje dostaje od auta
	time_reservation = random.randint(0,25)	#ilosc minut te informacje dostaje od auta
	status = 0

	route = localization()
	addTechniqueStatement = "update renting set route = CONCAT(route,%s) WHERE id=%s"
	val = (str(route),ID)
	cursor.execute(addTechniqueStatement, val)
	connection.commit()
	if time_finished.hour<23:
		stopCost=stopCost[0]
	else:
		stopCost = stopCost[1]
	kmdriven = calculateKilometers(ID)
	timedriven = calculateTime(time_finished,time_start)
	#print("KM: ",kmdriven," time: ",timedriven," stop time: ",time_stop+time_reservation)
	cost = kmdriven*kilometer_fee + timedriven*minute_fee + (time_stop+time_reservation)*stopCost + start_fee
	addTechniqueStatement = "update renting set car_route = %s,time_finished=%s,time_stop=%s,time_reservation=%s,status=%s,cost=%s WHERE id=%s;"
	val = (kmdriven,time_finished,time_stop,time_reservation,status,cost,ID)
	cursor.execute(addTechniqueStatement, val)
	connection.commit()



print('Database connecting script ')
with connect(
	host='localhost',
	user='root',
	password='root',
	database='carsharing'
) as connection:
	with connection.cursor() as cursor:
		# start_renting() #funkcja wykonujaca proces rozpoczecia wynajmu
		# update_route_info() #funkcja aktualizująca pozycje auta
		# end_renting() #funkcja uzupelnia brakujace informacje po wynajmie
		# add_leasing_deal() #dodanie leasingu (umowy) na konkretne auto
		# add_leasing_company() #dodanie firmy leasingowej
		connection.commit()
		
		