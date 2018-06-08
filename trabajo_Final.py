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
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

class prueba_Daltonismo(QDialog):
    def __init__(self):
        super(prueba_Daltonismo,self).__init__()
        loadUi('menu_principal.ui',self)
        self.ingresar_paciente=IngresarPaciente()
        self.ingresar.clicked.connect(self.Boton1)
        self.hacertest=verificacionCedula()
        self.test.clicked.connect(self.Boton2)
        self.verInfoPaciente=verInfoPaciente()
        self.ver.clicked.connect(self.boton3)
        
    def Boton1(self):
        self.ingresar_paciente.show()
    def Boton2(self):
        self.hacertest.show()
    def boton3(self):
        self.verInfoPaciente.show()
 
class IngresarPaciente(QDialog):
    def __init__(self):
        super(IngresarPaciente,self).__init__()
        loadUi('ingresar_p.ui',self)
        self.ingresar_pa.clicked.connect(self.on_clicked)
        self.cedula.setValidator(QtGui.QDoubleValidator())
        self.edad.setValidator(QtGui.QDoubleValidator())
        self.grupo1 = QButtonGroup()
        self.grupo1.addButton(self.femenino)
        self.grupo1.addButton(self.masculino)
    
    def generoP(self):        
        if self.masculino.isChecked():
            genero = 1
        elif self.femenino.isChecked():
            genero= 2
        else:
            genero=None
        return genero
        
    def on_clicked(self):
        nombre=self.nombre_paciente.text()
        cedula=self.cedula.text()
        edad=self.edad.text()
        genero=self.generoP()
        dalt='Falta por ingresar'
        correo=self.correo.text()
        if cedula=='' or genero==None:#Ciclo para comprobar que se ingresen los datos obligatorios, aun no funciona no se porque, sin el guarda el paciente 
            QMessageBox.about(self,'AVISO','Faltaron seleccionar datos obligatorios, intentelo nuevamente.')
        else:
            paciente=Paciente(nombre,cedula,edad,genero,dalt,correo)
            if medico.agregarPaciente(paciente):
                self.grupo1.setExclusive(False)
                self.femenino.setChecked(False)
                self.masculino.setChecked(False)
                self.grupo1.setExclusive(True)
                QMessageBox.about(self,'Aviso','El paciente fue agregado con exito')
            else:
                QMessageBox.about(self,'Aviso','El paciente ya existe')
        self.nombre_paciente.setText('')
        self.cedula.setText('')
        self.edad.setText('')
        
class verInfoPaciente(QDialog):
    def __init__(self):
        super(verInfoPaciente,self).__init__()
        loadUi('verPacienteCedula.ui',self)
        self.okay.clicked.connect(self.on_clicked)
        
    def on_clicked(self):
        cedula=self.cedula.text()
        if medico.verPaciente(cedula):
            infoPaciente=medico.verPaciente(cedula)
            QMessageBox.about(self,'AVISO','La informacion del paciente es: {}'.format(infoPaciente.__dict__))
        
class verificacionCedula(QDialog):
    def __init__(self):
        super(verificacionCedula,self).__init__()
        loadUi('cedulapretest.ui',self)
        
        self.ok.clicked.connect(self.on_clicked)
        
    def on_clicked(self):
        cedula=self.cedula.text()
        if medico.verificacionCedula(cedula):
            self.mostrarVentana=HacerTest(cedula)
            self.mostrarVentana.show()
            
        else:
            QMessageBox.about(self,'AVISO','La cedula no esta registrada.')
            
class HacerTest(QDialog):
    def __init__(self, cedula):
        super(HacerTest,self).__init__()
        loadUi('Prueba_Daltonismo.ui',self)
        self.__cedula = cedula
        self.enviar.clicked.connect(self.on_clicked)
        
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
        
    def on_clicked(self,):
        dal1=self.Daltonismo1()
        dal2=self.Daltonismo2()
        dal3=self.Daltonismo3()
        dal4=self.Daltonismo4()
        dal5=self.Daltonismo5()
        dal6=self.Daltonismo6()
#        cedula=self.cedula.text()
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
            QMessageBox.about(self,'AVISO','Faltan seleccionar datos obligatorios')
        elif dal1==1 or dal2==1 or dal3==1 or dal4==1 or dal5==1 or dal6==1:
            QMessageBox.about(self,'AVISO','Los mensajes fueron enviados a su correo')
            file = open('datos.txt', 'w')
            file.writelines(datos)
            file.close()
            files = open('datos.txt', 'r')
            files = files.readlines()
            files = ''.join(datos)
            msg = '''
From: clases.python2018@gmail.com
Subject: Resultados de la prueba de daltonismo'...
{} '''.format(files)
            nivelDaltonismo='Daltonico'
            medico.modificarDaltonismo(self.__cedula,nivelDaltonismo)
            medico.enviarCorreo(msg,self.__cedula)
        elif dal1==2 or dal2==2 or dal3==2 or dal4==2 or dal5==2 or dal6==2:
            QMessageBox.about(self,'AVISO','Los mensajes fueron enviados a su correo')
            file = open('datos.txt', 'w')
            file.writelines(datos)
            file.close()
            files = open('datos.txt', 'r')
            files = files.readlines()
            files = ''.join(datos)
            msg = '''
From: clases.python2018@gmail.com
Subject: Resultados de la prueba de daltonismo'...
{} '''.format(files)
            nivelDaltonismo='Ceguera cromatica'
            medico.modificarDaltonismo(self.__cedula,nivelDaltonismo)
            medico.enviarCorreo(msg,self.__cedula)
        elif dal1==0 or dal2==0 or dal3==0 or dal4==0 or dal5==0 or dal6==0:
            QMessageBox.about(self,'AVISO','Los mensajes fueron enviados a su correo')
            file = open('datos.txt', 'w')
            file.writelines(datos)
            file.close()
            files = open('datos.txt', 'r')
            files = files.readlines()
            files = ''.join(datos)
            msg = '''
From: clases.python2018@gmail.com
Subject: Resultados de la prueba de daltonismo'...
{} '''.format(files)
            nivelDaltonismo='No presenta'
            medico.modificarDaltonismo(self.__cedula,nivelDaltonismo)
            medico.enviarCorreo(msg,self.__cedula)

class Paciente():#Se crea la clase paciente.
    def __init__(self,n,c,e,g,d,co):#EL constructor recibe en su argumento los atributos: Nombre, Cedula, Peso, Genero, Antecedentes.
        self.__Nombre=n #atributo que describe la variable que describen las cualidades de la clase.
        self.__Cedula=c
        self.__Edad=e
        self.__Genero=g
        self.__daltonismo=d
        self.__Correo=co
    def getCedula(self): #Metodo que retorna la cedula del paciente.
        return self.__Cedula
    def getNombre(self):
        return self.__Nombre
    def getGenero(self):
        return self.__Genero
    def getCorreo(self):
        return self.__Correo
    def setDaltonismo(self,daltonico):
        self.__daltonismo=daltonico
        
    
class Medico(): #Se crea la clase medico.
    def __init__(self,n): #EL constructor recibe en su argumento el atributo: Nombre.
        self.__Nombre=n
        self.__PacientesQ={} #Se crea este diccionario para guardar la informacion del paciente. 

    def verificacionCedula(self,cedula):
        if cedula in self.__PacientesQ:
            return True
        else:
            return False
        
    def verPaciente(self,cedula):
        if cedula in self.__PacientesQ:
            infoPaciente=self.__PacientesQ[cedula]
            return infoPaciente
            
    def agregarPaciente(self,paciente): #Con este metodo se agrega la informacion completa de un paciente al diccionario 'PacientesQ'
        if paciente.getCedula() in self.__PacientesQ: #Si la cedula ya se encuentra en el diccionario, retorna falso y el paciente no se agrega en el. 
            return False
        else: #Si la cedula no esta en el diccionario, entonces se agrega el nuevo paciente en el y su clave es la cedula. 
            self.__PacientesQ[paciente.getCedula()]=paciente
            return True

    def getGeneros(self): #Este metodo retorna la cantidad de hombres y mujeres que aparecen en el diccionario de pacientes. 
        cont = 0 #Se inicializa un contador en cero.
        for cedula in self.__PacientesQ.keys(): #'cedula' toma las llaves del diccionario 'PacientesQ'.
            resultado = self.__PacientesQ[cedula].getGenero() #A la variable resultado se le asigna el genero de cada paciente.
            if resultado==1: #La opcion '1' corresponde al genero masculino.
                cont+=1 #Si el resultado es 1 al contador se le suma 1. 
        hombres=cont #A la variable 'hombres' se le asigna el contador.
        mujeres=len(self.__PacientesQ) - hombres #La cantidad de mujeres se determina con la resta entre la cantidad de pacienetes totales con la cantidad de hombres que ya se determino anteriormente. 
        return mujeres, hombres
    
    def modificarDaltonismo(self,cedula,daltonico):
        if cedula in self.__PacientesQ:
            self.__PacientesQ[cedula].setDaltonismo(daltonico)
            
    def enviarCorreo(self,msg,cedula):
        if cedula in self.__PacientesQ:
            correo=self.__PacientesQ[cedula].getCorreo()
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login("clases.python2018@gmail.com", "informatica01*") #correo y contraseña
            server.sendmail("clases.python2018@gmail.com", correo, msg)
            server.quit()
        
    
nombreMedico = 'Daniel'
medico=Medico(nombreMedico)

app = QApplication(sys.argv)
widget = prueba_Daltonismo()
widget.show()
sys.exit(app.exec_())







































