# -*- coding: utf-8 -*-
"""
Created on Thu May 31 15:16:20 2018

@author: Capta
"""

import sys
from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox, QButtonGroup
from PyQt5.uic import loadUi
from PyQt5 import QtGui
import smtplib
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from email.message import EmailMessage



class prueba_Daltonismo(QDialog):#Se crea la clase prueba daltonismo, menu principal
    def __init__(self):
        super(prueba_Daltonismo,self).__init__()
        loadUi('menu_principal.ui',self)
        self.ingresar_paciente=IngresarPaciente()#Guardamos la clase Ingresar Paciente
        self.ingresar.clicked.connect(self.Boton1)#Si da click en ingresar, lo conecta con el boton1
        self.hacertest=verificacionCedula()
        self.test.clicked.connect(self.Boton2)
        self.verestadisticas=VerEstadisticas()
        self.estadisticas.clicked.connect(self.Boton4)
        self.verInfoPaciente=verInfoPaciente()
        self.ver.clicked.connect(self.Boton3)
        
    def Boton1(self):
        self.ingresar_paciente.show()
    def Boton2(self):
        self.hacertest.show()
    def Boton4(self):
        self.verestadisticas.show()
    def Boton3(self):
        self.verInfoPaciente.show()
 
class IngresarPaciente(QDialog):#Se crea la clase ingrearPaciente
    def __init__(self):
        super(IngresarPaciente,self).__init__()
        loadUi('ingresar_p.ui',self)
        self.ingresar_pa.clicked.connect(self.on_clicked)#Conectar el boton para hacer una accion
        self.cedula.setValidator(QtGui.QDoubleValidator())#Validador de numeros
        self.grupo1 = QButtonGroup()
        self.grupo1.addButton(self.femenino)
        self.grupo1.addButton(self.masculino)
        self.grupo2 = QButtonGroup()
        self.grupo2.addButton(self.quince)
        self.grupo2.addButton(self.mayor)
        
    
    def generoP(self):    #Metodo para recibir el genero    
        if self.masculino.isChecked():
            genero = 1 #el genero sera igual a 1 si es hombre
        elif self.femenino.isChecked():
            genero= 2 #el genero sera igual a 2 si es mujer
        else:
            genero=None #el genero sera igual a None si no ingresa nada
        return genero
        
    def Edad(self): #Metodo para recibir la edad
        if self.quince.isChecked():
            Edad = 1 #La edad sera igual a 1 si esta entre 15 y 25
        elif self.mayor.isChecked():
            Edad = 2 #La edad sera igual a 1 si es mayor a 25
        else:
            Edad = None #si no la ingresa sera igual a None
        return Edad
        
    def on_clicked(self): #Metodo que se realizara despues de dar click en el boton
        nombre=self.nombre_paciente.text()#Recibir el nombre
        cedula=self.cedula.text()#Recibir la cedula
        edad=self.Edad()#Recibir la edad
        genero=self.generoP()#Recibir el genero
        dalt='Falta por ingresar' #el daltonismo se deja como standar para todos los pacientes neuvos
        correo=self.correo.text() #recibir el correo
        correo2=self.core.currentText() #recibir el domino del correo
        correost= correo + correo2 #almacenar todo el correo
        if cedula=='' or genero==None or edad== None:#Ciclo para comprobar que se ingresen los datos obligatorios, aun no funciona no se porque, sin el guarda el paciente 
            QMessageBox.about(self,'AVISO','Faltaron seleccionar datos obligatorios, intentelo nuevamente.')#Mesaje si noingreso datos necesarios
        else:
            paciente=Paciente(nombre,cedula,edad,genero,dalt,correost)#creo el paciente con los datos anteriores
            if medico.agregarPaciente(paciente): #condicional prara limpiar los campos
                self.grupo1.setExclusive(False)
                self.grupo2.setExclusive(False)
                self.femenino.setChecked(False)
                self.masculino.setChecked(False)
                self.quince.setChecked(False)
                self.mayor.setChecked(False)
                self.grupo1.setExclusive(True)
                self.grupo2.setExclusive(True)
                QMessageBox.about(self,'Aviso','El paciente fue agregado con exito')#Mesnaje que muetsra si el paciente fue agregado exitosamnte
                
            else:
                QMessageBox.about(self,'Aviso','El paciente ya existe')#Mesnaje si el paciente ya existe en el diccionario
        self.nombre_paciente.setText('')
        self.cedula.setText('')
        self.correo.setText('')
        
class verInfoPaciente(QDialog):#se crea la clas verInfoPaciente
    def __init__(self):
        super(verInfoPaciente,self).__init__()
        loadUi('verPacienteCedula.ui',self)
        self.okay.clicked.connect(self.on_clicked)#Cuando de click conectar con on?clicked
        
    def on_clicked(self):#Metodo que se realizara cuando se de click
        cedula=self.cedula.text()#Recibe la cedula
        if medico.verPaciente(cedula):#condicional parra mostrar el paciente
            infoPaciente=medico.verPaciente(cedula)
            nombre=(infoPaciente.__dict__.get('_Paciente__Nombre'))
            cedula=(infoPaciente.__dict__.get('_Paciente__Cedula'))
            if (infoPaciente.__dict__.get('_Paciente__Edad'))==1:
                edad = '15 años a 25 años'
            else:
                edad = 'Mayor de 25 años'
            if (infoPaciente.__dict__.get('_Paciente__Genero'))== 1:
                genero='Masculino'
            else:
                genero='Femenino'
            daltonismo=(infoPaciente.__dict__.get('_Paciente__Daltonismo'))
            correo=(infoPaciente.__dict__.get('_Paciente__Correo'))
            
           
            QMessageBox.about(self,'INFORMACION','''La informacion del usuario es: 
Nombre: {}
Cedula: {}
Edad: {}
Genero: {}
Diagnostico: {}
Correo: {}'''.format(nombre,cedula,edad,genero,daltonismo,correo))

                
class VerEstadisticas(QDialog):#Se crea la calse verEstadissticas
    def __init__(self):
        super(VerEstadisticas,self).__init__()
        loadUi('graficacion.ui',self)
        self.genero.clicked.connect(self.GraficarGenero)#conectar con el metodo graficargenero
        self.edad.clicked.connect(self.GraficarEdad)#conectar con el metodo graficarEdad
        
    def GraficarGenero(self):#Metodo que se realizara si dan click en el boton genero
        hombres, mujeres=medico.getGenerosDal()#recibe la cantidad de hombre y mujeres daltonicos
        self.figure=Figure()#creo la figura que msotrare
        self.Canvas=FigureCanvas(self.figure)#Pongo la figura en un lienzo
        self.geenero.addWidget(self.Canvas)#Agrego el lienzo a el espacio en el QT
        self.show()#Muestro la figura
        ax=self.figure.add_subplot(111)
        ax.clear()
        ax.grid(True)
        labels = 'Hombres', 'Mujeres'
        sizes = [hombres,mujeres]
        colors = ['gold', 'yellowgreen']
        explode = (0.1, 0)  # explode 1st slice
        ax.pie(sizes, explode=explode, labels=labels, colors=colors,
        autopct='%1.1f%%', shadow=True, startangle=140)##Creo la torta con los porcentajes

     
    def GraficarEdad(self):#Metodo que se realizara si dan click en el bton edad, hace lo mismo que el anterior metodo pero con la edad.
        menor, mayor=medico.getEdadDal()
        self.figure=Figure()
        self.Canvas=FigureCanvas(self.figure)
        self.edaad.addWidget(self.Canvas)
        self.show()
        ax=self.figure.add_subplot(111)
        ax.clear()
        ax.grid(True)
        labels = '15 años a 25 años', 'Mayores a 25 años'
        sizes = [menor,mayor]
        colors = ['gold', 'yellowgreen']
        explode = (0.1, 0)  # explode 1st slice
        ax.pie(sizes, explode=explode, labels=labels, colors=colors,
        autopct='%1.1f%%', shadow=True, startangle=140)

class verificacionCedula(QDialog):#se creoa la clase verificacionCedula
    def __init__(self):
        super(verificacionCedula,self).__init__()
        loadUi('cedulapretest.ui',self)
        self.ok.clicked.connect(self.on_clicked)#conexion con el metodo on?clciked
        
    def on_clicked(self):
        cedula=self.cedula.text()
        if medico.verificacionCedula(cedula):#Condicional que verifica que la cedula si este ingresada
            self.mostrarVentana=HacerTest(cedula)#Mostarra la clase HacerTest
            self.mostrarVentana.show()
            
        else:
            QMessageBox.about(self,'AVISO','La cedula no esta registrada.')#Mensaje si la ventana no esta registrada
            
class HacerTest(QDialog):#se crea la clase HacerTest
    def __init__(self, cedula):#recive una cedula de la ventana anterior
        super(HacerTest,self).__init__()#
        loadUi('ke.ui',self)
        self.__cedula = cedula#se guarda la cedula que recive de otra ventana
        self.enviar.clicked.connect(self.on_clicked)
        
    #Apartir de aca, los resultados seran, 1 para perosnas daltonicas,2 para perosnas que padecen seguera, 0 para las personas que no presentan nada    
    def Daltonismo1(self):
        if self.doce.isChecked():
            Daltonismo1 = 0 
        elif self.n1.isChecked():
            Daltonismo1 = 2
        else:
            Daltonismo1=None
        return Daltonismo1
    
    def Daltonismo2(self):        
        if self.tres.isChecked():
            Daltonismo2 = 1
        elif self.ocho.isChecked():
            Daltonismo2 = 0
        elif self.n2.isChecked():
            Daltonismo2 = 2
        else:
            Daltonismo2=None
        return Daltonismo2
    
    def Daltonismo3(self):        
        if self.seis.isChecked():
            Daltonismo3 = 1
        elif self.cinco.isChecked():
            Daltonismo3 = 0
        elif self.n3.isChecked():
            Daltonismo3 = 2
        else:
            Daltonismo3=None
        return Daltonismo3
    
    def Daltonismo4(self):        
        if self.setenta.isChecked():
            Daltonismo4 = 1
        elif self.veintinueve.isChecked():
            Daltonismo4 = 0
        elif self.n4.isChecked():
            Daltonismo4 = 2
        else:
            Daltonismo4=None
        return Daltonismo4
    
    def Daltonismo5(self):        
        if self.cincuentaysiete.isChecked():
            Daltonismo5 = 0
        elif self.treintaycinco.isChecked():
            Daltonismo5 = 1
        elif self.n5.isChecked():
            Daltonismo5 = 2
        else:
            Daltonismo5=None
        return Daltonismo5
    
    def Daltonismo6(self):        
        if self.dos.isChecked():
            Daltonismo6 = 1
        elif self.cincod.isChecked():
            Daltonismo6 = 0
        elif self.n6.isChecked():
            Daltonismo6 = 2
        else:
            Daltonismo6=None
        return Daltonismo6
        
    def on_clicked(self,):#conexion con el boton
        #se llaman los metodos anteriores para guardar las opciones elegidas 
        dal1=self.Daltonismo1()
        dal2=self.Daltonismo2()
        dal3=self.Daltonismo3()
        dal4=self.Daltonismo4()
        dal5=self.Daltonismo5()
        dal6=self.Daltonismo6()
        #se agregan todos los radiobotnes a un grupo para lueog limparlos
        self.grupo1 = QButtonGroup()
        self.grupo1.addButton(self.n1)
        self.grupo1.addButton(self.tres)
        self.grupo1.addButton(self.ocho)
        self.grupo1.addButton(self.n2)
        self.grupo1.addButton(self.seis)
        self.grupo1.addButton(self.cinco)
        self.grupo1.addButton(self.n3)
        self.grupo1.addButton(self.setenta)
        self.grupo1.addButton(self.veintinueve)
        self.grupo1.addButton(self.n4)
        self.grupo1.addButton(self.cincuentaysiete)
        self.grupo1.addButton(self.treintaycinco)
        self.grupo1.addButton(self.n5)
        self.grupo1.addButton(self.n6)
        self.grupo1.addButton(self.dos)
        self.grupo1.addButton(self.cincod)
        #en datos guardaremos la informacion que vamos a enviar por correo
        datos = '''Prueba 1: {}
Prueba 2: {}
Prueba 3: {}
Prueba 4: {}
Prueba 5: {}
Prueba 6: {}
Instrucciones para leer los resultados.

1.Si recibes un 1 en la mayoria de las pruebas, quiere decir que eres daltonico.
2.Si recibes un 2 en la mayoria de las pruebas, quiere decir que tienes ceguera total cromatica.
3.Si recibes un 0 en la mayoria de las pruebas, quiere decir que no padeces de daltonismo. '''.format(dal1,dal2,dal3,dal4,dal5,dal6)
        if dal1==None or dal2==None or dal3==None or dal4==None or dal5==None or dal6==None:
            QMessageBox.about(self,'AVISO','Faltan seleccionar datos obligatorios')#Mesnaje si no se ingresaron los datos obligatorios
        elif dal1==1 or dal2==1 or dal3==1 or dal4==1 or dal5==1 or dal6==1:#condicional para daltonicos
            if medico.verPaciente(self.__cedula):#condiconas que verifica la cedula y luego saca la infromacion del paciente
                infoPaciente=medico.verPaciente(self.__cedula)
                nombre=(infoPaciente.__dict__.get('_Paciente__Nombre'))
                cedula=(infoPaciente.__dict__.get('_Paciente__Cedula'))
                edad=(infoPaciente.__dict__.get('_Paciente__Edad'))
                correo=(infoPaciente.__dict__.get('_Paciente__Correo'))
                daltonismo=(infoPaciente.__dict__.get('_Paciente__Daltonismo'))
                genero=(infoPaciente.__dict__.get('_Paciente__Genero'))
                paciente=Paciente(nombre,cedula,edad,correo,daltonismo,genero)#Se crea el paciente con la informacion anterior
                medico.agregarDal(paciente)#Guarda el paciente en un diccionario aparte 
            QMessageBox.about(self,'AVISO','Los resultados fueron enviados a su correo')#Mesnaje para verificar que los datos hayan sido enviados
            file = open('datos.txt', 'w')#Guarda los datos en un archivo de texto
            file.writelines(datos)
            file.close()
            files = open('datos.txt', 'r')#se abre el archivo de texto para enviar por correo
            files = files.readlines()
            files = ''.join(datos)
            msg = EmailMessage()
            msg.set_content(datos)
            msg['Subject'] = 'RESULTADOS DALTONISMO'
            msg['From'] = "clases.python2018@gmail.com"
            nivelDaltonismo='Daltonico'#Como saco uno en alguno de las imagenes se dice que el paciente es daltonico
            medico.modificarDaltonismo(self.__cedula,nivelDaltonismo)
            medico.enviarCorreo(msg,self.__cedula)
          
        elif dal1==2 or dal2==2 or dal3==2 or dal4==2 or dal5==2 or dal6==2:#Condicional para personas con ceguera cromatica
            QMessageBox.about(self,'AVISO','Los resultados fueron enviados a su correo')
            file = open('datos.txt', 'w')#se guardan los datos en un archivo de texto
            file.writelines(datos)
            file.close()
            files = open('datos.txt', 'r')#se abre el archivo de texto para enviar por correo
            files = files.readlines()
            files = ''.join(datos)
            msg = EmailMessage()
            msg.set_content(datos)
            msg['Subject'] = 'RESULTADOS DALTONISMO'
            msg['From'] = "clases.python2018@gmail.com"
            nivelDaltonismo='Ceguera cromatica'#nivel segun resultados en la prueba
            medico.modificarDaltonismo(self.__cedula,nivelDaltonismo)
            medico.enviarCorreo(msg,self.__cedula)
        elif dal1==0 or dal2==0 or dal3==0 or dal4==0 or dal5==0 or dal6==0:#condicional para personas sanas
            QMessageBox.about(self,'AVISO','Los resultados fueron enviados a su correo')
            file = open('datos.txt', 'w')#se guardan los datos en un archivo de texto
            file.writelines(datos)
            file.close()
            files = open('datos.txt', 'r')#se abre el archivo de texto para enviar por correo
            files = files.readlines()
            files = ''.join(datos)
            msg = EmailMessage()
            msg.set_content(datos)
            msg['Subject'] = 'RESULTADOS DALTONISMO'
            msg['From'] = "clases.python2018@gmail.com"
            nivelDaltonismo='No presenta'
            medico.modificarDaltonismo(self.__cedula,nivelDaltonismo)
            medico.enviarCorreo(msg,self.__cedula)
    
class Paciente():#Se crea la clase paciente.
    def __init__(self,n,c,e,g,d,co):#EL constructor recibe en su argumento los atributos: Nombre, Cedula, Peso, Genero, Antecedentes.
        self.__Nombre=n #atributo que describe la variable que describen las cualidades de la clase.
        self.__Cedula=c
        self.__Edad=e
        self.__Genero=g
        self.__Daltonismo=d
        self.__Correo=co
    def getCedula(self): #Metodo que retorna la cedula del paciente.
        return self.__Cedula
    def getNombre(self):
        return self.__Nombre
    def getGenero(self):
        return self.__Genero
    def getCorreo(self):
        return self.__Correo
    def getEdad(self):
        return self.__Edad
    def getdaltonismo(self):
        return self.__Daltonismo
    def setDaltonismo(self,daltonico):#cambia el nivel de daltonismo de un paciente
        self.__Daltonismo=daltonico
    def setEdad(self,edad):
        self.__Edad=edad
        
    
class Medico(): #Se crea la clase medico.
    def __init__(self,n): #EL constructor recibe en su argumento el atributo: Nombre.
        self.__Nombre=n
        self.__PacientesQ={} #Se crea este diccionario para guardar la informacion del paciente. 
        self.__Usuariosdal={} #Se crea este diccionario para guardar la informacion de un paciente daltonico
    
    def agregarDal(self,paciente):
        if paciente.getCedula() in self.__Usuariosdal: #Si la cedula ya se encuentra en el diccionario, retorna falso y el paciente no se agrega en el. 
            return False
        else: #Si la cedula no esta en el diccionario, entonces se agrega el nuevo paciente en el y su clave es la cedula. 
            self.__Usuariosdal[paciente.getCedula()]=paciente
            return True
    
    def getGenerosDal(self): #Este metodo retorna la cantidad de hombres y mujeres que aparecen en el diccionario de pacientes. 
        cont = 0 #Se inicializa un contador en cero.
        for cedula in self.__Usuariosdal.keys(): #'cedula' toma las llaves del diccionario 'PacientesQ'.
            resultado = self.__Usuariosdal[cedula].getGenero() #A la variable resultado se le asigna el genero de cada paciente.
            if resultado==1: #La opcion '1' corresponde al genero masculino.
                cont+=1 #Si el resultado es 1 al contador se le suma 1. 
        hombres=cont #A la variable 'hombres' se le asigna el contador.
        mujeres=len(self.__Usuariosdal) - hombres #La cantidad de mujeres se determina con la resta entre la cantidad de pacienetes totales con la cantidad de hombres que ya se determino anteriormente. 
        return mujeres, hombres 
        
    def getEdadDal(self):
        cont = 0 #Se inicializa un contador en cero.
        for cedula in self.__Usuariosdal.keys(): #'cedula' toma las llaves del diccionario 'PacientesQ'.
            resultado = self.__Usuariosdal[cedula].getEdad() #A la variable resultado se le asigna el genero de cada paciente.
            if resultado==1: #La opcion '1' corresponde al genero masculino.
                cont+=1 #Si el resultado es 1 al contador se le suma 1. 
        menor=cont #A la variable 'hombres' se le asigna el contador.
        mayor=len(self.__Usuariosdal) - menor #La cantidad de mujeres se determina con la resta entre la cantidad de pacienetes totales con la cantidad de hombres que ya se determino anteriormente. 
        return menor, mayor
 
    def verificacionCedula(self,cedula):
        if cedula in self.__PacientesQ:#si la cedula esta en a lista de pacientes principal
            return True
        else:
            return False

    def verPaciente(self,cedula):
        if cedula in self.__PacientesQ: #condicional para verificar la cedula
            infoPaciente=self.__PacientesQ[cedula]#Guarda toda la informacion con esa cedula
            return infoPaciente
    
    def modificarDaltonismo(self,cedula,daltonico):
        if cedula in self.__PacientesQ:#condicional para verificar la cedula
            self.__PacientesQ[cedula].setDaltonismo(daltonico)#cambiara el nivel de daltonismo con ayuda del emtodo setDaltonismo
            
        
    def agregarPaciente(self,paciente): #Con este metodo se agrega la informacion completa de un paciente al diccionario 'PacientesQ'
        if paciente.getCedula() in self.__PacientesQ: #Si la cedula ya se encuentra en el diccionario, retorna falso y el paciente no se agrega en el. 
            return False
        else: #Si la cedula no esta en el diccionario, entonces se agrega el nuevo paciente en el y su clave es la cedula. 
            self.__PacientesQ[paciente.getCedula()]=paciente
            return True 
    
    def enviarCorreo(self,msg,cedula):
        if cedula in self.__PacientesQ:
            correo=self.__PacientesQ[cedula].getCorreo()
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login("clases.python2018@gmail.com", "informatica01*")
            text = msg.as_string()
            server.sendmail("clases.python2018@gmail.com", correo, text)
            server.quit()
        
    

    
nombreMedico = 'Daniel'
medico=Medico(nombreMedico)

app = QApplication(sys.argv)
widget = prueba_Daltonismo()
widget.show()
app.exec_()







































