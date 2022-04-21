from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QTableWidgetItem
import sys

import datetime
from datetime import date, timedelta
import random
import clsMsjAlert as Mje
import clsC_Usuarios as CrudUsuarios
import clsSendMail as EnviarMail
from PyQt5.QtWidgets import *

class clsRegistroCta(QtWidgets.QMainWindow):
    def __init__(self,fila=None,tabla=None):
       super(clsRegistroCta, self).__init__()
       uic.loadUi('ui/registroCta.ui',self)
       self.fchActual=datetime.date.today()
       self.bd=CrudUsuarios.clsC_Usuarios()
       self.listTCta=self.bd.getTiposCta()
       self.fila=fila
       self.tbl=tabla

       self.setupUi()



    
    def setupUi(self):
        
        if self.fila!=None:
            self.setWindowTitle("Datos del usuario")
            self.idUs=self.tbl.tblData.item(self.fila, 0).text()
            self.datosUs=self.bd.getDatos(self.idUs)
            self.correo=self.tbl.tblData.item(self.fila, 6).text()
            self.cargarForm(self.datosUs)
            self.passSection.hide()
            self.btnResPass.clicked.connect(self.resetearPass)
            self.btnAceptar.clicked.connect(self.updateDatos)
            #self.btnResPass.clicked.connect(lambda:self.resetearPass())
            
        else:
            self.btnAceptar.clicked.connect(self.cargarDatos)
            self.dateNac.setDate(self.fchActual)
            self.btnResPass.hide()

        self.cboTCta.addItems(self.getTiposCta())
        self.chkPass.stateChanged.connect(lambda:self.verPass(1))
        self.chkPass2.stateChanged.connect(lambda:self.verPass(2))
        self.btnCancelar.clicked.connect(self.cerrar)
        
        


    def cargarForm(self,tupla):
        self.textDni.setText(str(tupla[0][1]))
        self.textNombre.setText(str(tupla[0][2]))
        self.textApellido.setText(str(tupla[0][3]))
        self.dateNac.setDate(tupla[0][4])
        self.textDireccion.setText(str(tupla[0][5]))
        self.textMail.setText(str(tupla[0][6]))
        self.textTel.setText(str(tupla[0][7]))
        self.textUser.setText(str(tupla[0][9]))
        self.textPass.setText(str(tupla[0][10]))
        self.textLastPass.setText(str(tupla[0][11]))
        '''
        self.textPass.setText(str(tupla[]))
        '''
        




    def cargarDatos(self):
        dni=self.textDni.toPlainText()
        nom=self.textNombre.toPlainText()
        ape=self.textApellido.toPlainText()
        temp_var = self.dateNac.date() 
        fchNac = temp_var.toPyDate()
        print(temp_var)
        print(fchNac)
        direc=self.textDireccion.toPlainText()
        mail=self.textMail.toPlainText()
        tel=self.textTel.toPlainText()
        user=self.textUser.toPlainText()
        tCta=self.cboTCta.currentText()
        idTCta=self.getIdTCta(tCta)

        cta=self.bd.buscaCta(user)
        print(cta)
        if cta==None:
            pass1=self.textPass.text()
            pass2=self.textLastPass.text()
            if pass1!=pass2:
                self.mje=Mje.clsMsjAlert("Las contraseñas no son iguales.\nPor favor controle que ambas contraseñas sean la misma.")
                self.mje.show()
            else:
                fchActual=self.fchActual
                print(fchActual)
                data=[int(dni),nom,ape,fchNac,direc,mail,tel,fchActual,user,pass1,idTCta]
                self.bd.insert(data)
                self.mail=EnviarMail.clsSendMail(pass1,nom,mail,user)
                self.mje=Mje.clsMsjAlert("La cuenta ha sido creada con éxito.")
                self.mje.show()
                self.cerrar()
        else:
            self.mje=Mje.clsMsjAlert("El nombre de usuario ya está en uso.\nPor favor elija otro nombre de usuario.")
            self.mje.show()


            
    def verPass(self,item):
        if item==1:
            chk=self.chkPass
            txtItem=self.textPass
        else:
            if item==2:
                chk=self.chkPass2
                txtItem=self.textLastPass
        if chk.isChecked():
            txtItem.setEchoMode(QLineEdit.Normal)
        else:
            txtItem.setEchoMode(QLineEdit.Password)
           


    def resetearPass(self):     #pass de 8 digitos
        idUs=self.tbl.tblData.item(self.fila, 0).text()
        nombre=self.tbl.tblData.item(self.fila, 2).text()
        password=""
        #Fecha y hora UTC-00 +1hora, seria la fecha y hora en que caduce la nueva clave
        fchHora=datetime.datetime.utcnow()+timedelta(hours=1)
        for x in range(0,8):
            password= password + str(random.randint(0, 9))
        self.bd.setPass(password,idUs,fchHora)
        self.mail=EnviarMail.clsSendMail(password,nombre,self.correo)
        self.mje=Mje.clsMsjAlert("La contraseña ha sido reestablecida.\nSe ha enviado un correo con la nueva contraseña al correo del usuario.")
        self.mje.show()
        


    def updateDatos(self):
        print(self.datosUs)
        datos=["","","","","","","",""]
        flag=0
        #               [  0     1     2     3     4       5      6  ]
        #FORMATO: datos=["dni","nom","ape","fch","dom","correo","tel"]
        dni=self.textDni.toPlainText()
        nom=self.textNombre.toPlainText()
        ape=self.textApellido.toPlainText()
        temp_var = self.dateNac.date() 
        fchNac = temp_var.toPyDate()
        dom=self.textDireccion.toPlainText()
        correo=self.textMail.toPlainText()
        tel=self.textTel.toPlainText()

        if dni=="" or nom=="" or ape=="" or dom=="" or correo=="" or tel=="":
            self.mje=Mje.clsMsjAlert("Controle que ningún campo quede vacio.")
            self.mje.show()
        else:
            if dni!=str(self.datosUs[0][1]):
                flag=1
                datos[0]=dni
            
            if nom!=str(self.datosUs[0][2]):
                flag=1
                datos[1]=nom
        
            if ape!=str(self.datosUs[0][3]):
                flag=1
                datos[2]=ape

            if fchNac!=str(self.datosUs[0][4]):
                flag=1
                datos[3]=fchNac
    
            if dom!=str(self.datosUs[0][5]):
                flag=1
                datos[4]=dom
            
            if correo!=str(self.datosUs[0][6]):
                flag=1
                datos[5]=correo
            
            if tel!=str(self.datosUs[0][7]):
                flag=1
                datos[6]=tel
            #me fijo la bandera para saber si hubo algun cambio
            if flag!=0:
                self.bd.setData(self.idUs,datos)
            self.close()



    def getTiposCta(self):
        tipos=[]
        for ind in range(0,len(self.listTCta)):
            tipos.append(self.listTCta[ind][1])
        return tipos        
    


    def getIdTCta(self,tipo):
        for ind in range(0,len(self.listTCta)):
            if self.listTCta[ind][1]==tipo:
                return self.listTCta[ind][0]      
            
            

    def cerrar(self):
        self.close()





def main():
	app = QtWidgets.QApplication(sys.argv)	
	
	form = clsRegistroCta()
	form.show()
	app.exec_()

if __name__ == '__main__':
	main()