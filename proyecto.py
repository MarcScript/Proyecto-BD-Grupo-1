import mysql.connector
from datetime import datetime, timedelta
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
from tkinter import *
from tkinter import ttk
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522


k = 65
reader = SimpleMFRC522()
#Creamos la ventana principal
ventana = Tk()
height = 500
witdh = 500
ventana.geometry("{}x{}".format(height, witdh))
ventana.title("Interfaz de marcación de entrada de EMPRESA S.A")
ventana.resizable(width=False, height=False)

# Conexion a base de datos
mydb=mysql.connector.connect(
        host="localhost",
        user="root",   
        passwd="123456",
        database="empleados"
        )
cursor=mydb.cursor()
#Entradas de sensores y tiempo
#time = datetime.now()
#time_old = time - timedelta(seconds=3)
#hora_ent = time.strftime("%H:%M:%S")
#Funciones 
def consultar(sql):
    cursor.execute(sql)
    result=cursor.fetchall()
    return result

def imprimirRegistro():
    result=consultar("SELECT * FROM registro_ent")
    for row in result:
            print("id_registro: ", row[0])
            print("hora_ent: ", row[1])
            print("cedula: ", row[2])
            print("\n")
    top = Toplevel()

    tab_emp = ttk.Treeview(top, column=("c1", "c2", "c3"), show='headings')

    tab_emp.column("#1", anchor=CENTER)

    tab_emp.heading("#1", text="ID")

    tab_emp.column("#2", anchor=CENTER)

    tab_emp.heading("#2", text="Hora de entrada")

    tab_emp.column("#3", anchor=CENTER)

    tab_emp.heading("#3", text="Cedula")

    sql = "SELECT * FROM registro_ent"
    cursor.execute(sql)
    result = cursor.fetchall()
    for row in result:
        tab_emp.insert("", END, values=row)
    tab_emp.pack()
    top.title('Registro de entrada')
    
def limpiarTabla():
    sql = "TRUNCATE TABLE registro_ent"
    cursor.execute(sql)
def registroCompletado():
    messagebox.showinfo("Info","Usted ya se ha registrado")
# Creacion de botones

ImpReg = Button(ventana, text="Imprimir Registro", command=imprimirRegistro,
                width=40, height=5, font="Times 12 italic bold")
ImpReg.place(x=height/6, y=300+k)
regEntrada = Label(ventana, text=" ")
regEntrada.place(x=height/6, y=int(k/3))
def leerSensor():
    time = datetime.now()
    time_old = time - timedelta(seconds=0)
    hora_ent = time.strftime("%H:%M:%S")
    try:
            UU_ID = reader.read_id_no_block()
            if UU_ID != None:
                print(UU_ID)
                cedula = consultar("SELECT cedula FROM empleado WHERE UU_ID = '{}'".format(UU_ID))
                for row in cedula:
                    hora=consultar("SELECT hora_ent FROM registro_ent WHERE cedula = '{}'".format(row[0]))
                
                if len(hora)==0:
                    
                    for row in cedula:
                        sql="INSERT INTO registro_ent(hora_ent,cedula) VALUES ('{}','{}')".format(hora_ent,row[0])
                    cursor.execute(sql)
                    mydb.commit()
                    imprimirRegistro()
                    
                else:
                     print("Ya se ha registrado el usuario en el sistema")
                     #regEntrada['text'] = "Ya se ha registrado el usuario en el sistema"
                     registroCompletado()
    finally:
            GPIO.cleanup()
            delta = int(time.strftime('%s')) - int(time_old.strftime('%s'))#calculo del tiempo transcurrido
            print(delta)
            if delta>=10:
                time_old=time
                limpiarTabla()
                print("Se trunco la tabla")
                
ventana.after(25,leerSensor)
ventana.mainloop() 
mydb.close()


