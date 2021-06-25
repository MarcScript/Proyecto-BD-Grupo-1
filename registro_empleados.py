import mysql.connector
from datetime import datetime, timedelta
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
from tkinter import *
from tkinter import ttk
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import multiprocessing
from multiprocessing import Process
from multiprocessing import Pool
import tkinter as tk
from threading import Thread
import time
k = 65
reader = SimpleMFRC522()
# Creamos la ventana principal


# Conexion a base de datos
mydb=mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="123456",
        database="empleados"
        )
cursor=mydb.cursor()
#Inicializamos

# Entradas de sensores y tiempo
#time = datetime.now()
#time_old = time - timedelta(seconds=3)
#hora_ent = time.strftime("%H:%M:%S")
# Clase App


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        height = 500
        witdh = 500
        self.geometry("{}x{}".format(height, witdh))
        self.title("Interfaz de marcación de entrada de EMPRESA S.A")
        self.resizable(width=False, height=False)
        ImpReg = Button(self, text="Imprimir Registro", command=imprimirRegistro,
                        width=40, height=5, font="Times 12 italic bold")

        ImpReg.place(x=height/6, y=300+k)
        regEntrada = Label(self, text=" ")
        regEntrada.place(x=height/6, y=int(k/3))

        AgEmp = Button(self, text="Agregar Empleado", command=AgregarEmpleado,
                       width=40, height=5, font="Times 12 italic bold")
        AgEmp.place(x=height/6, y=50+k)

        ListEmp = Button(self, text="Registro de Empleados", command=listarEmpleados,
                         width=40, height=5, font="Times 12 italic bold")
        ListEmp.place(x=height/6, y=175+k)
        self.times()
        self.leerSensor()
    def times(self):
        clock=Label(self,font=("times",50,"bold"))
        clock.grid(row=2,column=1,pady=25,padx=100)
        current_time=time.strftime("%H:%M:%S") 
        clock.config(text=current_time,bg="black",fg="green",font="Arial 50 bold")
        clock.after(200,self.times)
        clock.after(5000,self.leerSensor)
    def leerSensor(self):
        try:
                GPIO.setwarnings(False)
                UU_ID = reader.read_id_no_block()
                time = datetime.now()
                time_old = time - timedelta(seconds=0)
                hora_ent = time.strftime("%H:%M:%S")
                if UU_ID != None:
                    print(UU_ID)
                    cedula = consultar(
                        "SELECT cedula FROM empleado WHERE UU_ID = '{}'".format(UU_ID))
                    for row in cedula:
                        hora = consultar(
                            "SELECT hora_ent FROM registro_ent WHERE cedula = '{}'".format(row[0]))

                    if len(hora) == 0:
                        for row in cedula:
                            sql = "INSERT INTO registro_ent(hora_ent,cedula) VALUES ('{}','{}')".format(
                                hora_ent, row[0])
                        cursor.execute(sql)
                        mydb.commit()
                        result = consultar("SELECT * FROM registro_ent")
                        for row in result:
                            print("id_registro: ", row[0])
                            print("hora_ent: ", row[1])
                            print("cedula: ", row[2])
                            print("\n")
                            mensaje = " ID:{} \n Hora de entrada: {} \n Cédula:{}".format(
                                row[0], row[1], row[2])
                            messagebox.showinfo(
                                title="Registro Correcto ", message=mensaje)
                    else:
                        print("Ya se ha registrado el usuario en el sistema")
                        #regEntrada['text'] = "Ya se ha registrado el usuario en el sistema"
                        registroCompletado()
        finally:
                GPIO.cleanup()
                # delta = int(time.strftime('%s')) - int(time_old.strftime('%s'))#calculo del tiempo transcurrido
                # tiempo = instanteFinal - instanteInicial # Devuelve un objeto timedelta
                #segundos = tiempo.seconds
                # if segundos>=10:
                #    instanteInicial = datetime.now()
                #    #time_old=time
                #    limpiarTabla()
                #    cont = 0
                #    print("Se trunco la tabla")      
        

# Funciones


def consultar(sql):
    cursor.execute(sql)
    result = cursor.fetchall()
    return result


def listarEmpleados():

    top = Toplevel()

    list_emp = ttk.Treeview(top, column=(
        "c1", "c2", "c3", "c4", "c5"), show='headings')

    list_emp.column("#1", anchor=CENTER)

    list_emp.heading("#1", text="Cedula")

    list_emp.column("#2", anchor=CENTER)

    list_emp.heading("#2", text="Nombre")

    list_emp.column("#3", anchor=CENTER)

    list_emp.heading("#3", text="Apellido")

    list_emp.column("#4", anchor=CENTER)

    list_emp.heading("#4", text="Correo")

    list_emp.column("#5", anchor=CENTER)

    list_emp.heading("#5", text="UU_ID")
    sql = "SELECT * FROM empleado"
    cursor.execute(sql)
    result = cursor.fetchall()
    for row in result:
        list_emp.insert("", END, values=row)
    list_emp.pack()
    top.title('Registro de empleados')


def AgregarEmpleado():
    def clear_text():
        #sql="INSERT INTO tarjeta(UU_ID) VALUES ('{}')".format(UUID)
        # cursor.execute(sql)
        # mydb.commit()
        # print(UUID)
        #sql="INSERT INTO empleado(cedula,nombre,apellido,correo,UU_ID) VALUES ('{}','{}','{}','{}','{}')".format(ced,nom,ap,correo,UUID)
        # cursor.execute(sql)
        # mydb.commit()
        result = consultar("SELECT * FROM empleado")
        for row in result:
            print("Cedula: ", row[0])
            print("Nombre: ", row[1])
            print("Apellido: ", row[2])
            print("Correo: ", row[3])
            print("UU_ID: ", row[4])
            print("\n")
        ap.delete(0, END)
        ced.delete(0, END)
        nom.delete(0, END)
        UUID.delete(0, END)
        correo.delete(0, END)
    top = Toplevel()
    top.geometry("500x500")
    top.title('Agregar empleado')
    ced_lab = Label(top, text="Cédula:")
    ced_lab.place(x=20, y=20)
    ced = Entry(top, width=10)
    ced.place(x=100, y=20)
    nom_lab = Label(top, text="Nombre:")
    nom_lab.place(x=20, y=80)
    nom = Entry(top, width=20)
    nom.place(x=100, y=80)
    ap_lab = Label(top, text="Apellido:")
    ap_lab.place(x=20, y=140)
    ap = Entry(top, width=20)
    ap.place(x=100, y=140)
    correo_lab = Label(top, text="Correo:")
    correo_lab.place(x=20, y=200)
    correo = Entry(top, width=40)
    correo.place(x=100, y=200)
    UUID_lab = Label(top, text="UU_ID:")
    UUID_lab.place(x=20, y=260)
    UUID = Entry(top, width=30)
    UUID.place(x=100, y=260)
    enviar = Button(top, text="Enviar", command=clear_text)
    enviar.place(x=150, y=320)


def imprimirRegistro():
    result = consultar("SELECT * FROM registro_ent")
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
    messagebox.showinfo("Info", "Usted ya se ha registrado")


# Limpiamos la tabla
limpiarTabla()
# Creacion de botones


      


if __name__ == '__main__':
    app = App()
    app.mainloop()