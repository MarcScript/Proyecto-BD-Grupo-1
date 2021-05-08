import mysql.connector
from datetime import datetime
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
#Variables
exit = "0"
#Entradas de sensores y tiempo
time = datetime.now()

hora_ent = time.strftime("%H:%M:%S")
#Lectura RFID
reader = SimpleMFRC522()

mydb=mysql.connector.connect(
    host="localhost",
    user="root",   
    passwd="123456",
    database="empleados"
    )
cursor=mydb.cursor()

def imprimirEmpleado():
    sql="SELECT * FROM empleado"
    cursor.execute(sql)
    result=cursor.fetchall()
    for row in result:
            print("Cedula: ", row[0])
            print("Nombre: ", row[1])
            print("Apellido: ", row[2])
            print("Correo: ", row[3])
            print("UUID: ", row[4])
            print("\n")
def imprimirRegistro():
    sql="SELECT * FROM registro_ent"
    cursor.execute(sql)
    result=cursor.fetchall()
    for row in result:
            print("id_registro: ", row[0])
            print("hora_ent: ", row[1])
            print("cedula: ", row[2])
            print("\n")
def ingresarEmpleado():
   nombre = input("Ingrese su nombre\n")
   apellido = input("Ingrese su apellido\n")
   cedula = input("Ingrese su cedula\n")
   correo = input("Ingrese su correo\n")
   UU_ID = input("Ingrese su codigo UUID\n")
   sql="INSERT INTO empleado(cedula,nombre,apellido,correo,UU_ID) VALUES ('{}','{}','{}','{}','{}')".format(cedula,nombre,apellido,correo,UU_ID)
   return sql

while exit == "0":
    try:
        time = datetime.now()
        hora_ent = time.strftime("%H:%M:%S")
        UU_ID = reader.read_id()
        #print(id)
        print(UU_ID)
        sql = "SELECT cedula FROM empleado WHERE UU_ID = '{}'".format(UU_ID)
        cursor.execute(sql)
        result=cursor.fetchall()
        print(result)
        for row in result:
            sql="INSERT INTO registro_ent(hora_ent,cedula) VALUES ('{}','{}')".format(hora_ent,row[0])
        cursor.execute(sql)
        mydb.commit()
        imprimirRegistro()
    finally:
        GPIO.cleanup()
mydb.close()
