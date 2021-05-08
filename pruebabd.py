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

def imprimirEmpleado(sql):
    cursor.execute(sql)
    result=cursor.fetchall()
    for row in result:
            print("Cedula: ", row[0])
            print("Nombre: ", row[1])
            print("Apellido: ", row[2])
            print("Correo: ", row[3])
            print("UUID: ", row[4])
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
    print("Seleccione 1 para visualizar los datos de la base de datos\n")
    print("Seleccione 2 para agregar un nuevo empleado\n")
    print("Seleccione 3 para eliminar a algun empleado\n")
    print("Presione 0 para salir")
    a = input()
    cursor=mydb.cursor()
    if a == "1":
        sql="select * from empleado"
        imprimirEmpleado(sql)
        mydb.commit()
        cursor.close()
    elif a == "2":
       sql = ingresarEmpleado()
       cursor.execute(sql)
       sql="select * from empleado"
       imprimirEmpleado(sql)
       mydb.commit()
       cursor.close()
    elif a == "3":
        cedula = input("Ingrese el nro de cedula que desea eliminar")
        try:
            sql = "DELETE FROM empleado WHERE cedula='{}'".format(cedula)
            cursor.execute(sql)
            mydb.commit()
            cursor.close()
            print("Se ha eliminado con éxito al empleado con CI:{}\n".format(cedula))
        except:
            print("No se encuentra la cedula en la base de datos")
    else:
        exit = "1"
mydb.close()

