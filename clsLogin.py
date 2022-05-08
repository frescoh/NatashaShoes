from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QTableWidgetItem
import Controladores.clsC_Usuarios as CrudUsuarios
import clsRegistroCta as RegistroCta
import clsMsjAlert as Mje
import datetime

import sys

import clsTable as principal

class clsLogin(QtWidgets.QMainWindow):
    
    def __init__(self):
        super(clsLogin, self).__init__()
        uic.loadUi('ui files/login.ui',self)
        self.bd=CrudUsuarios.clsC_Usuarios()
        self.setupUi()
        
    def setupUi(self):
        self.btnIngresar.clicked.connect(self.ingreso)
        self.btnCancelar.clicked.connect(self.cerrar)
        
    def ingreso(self):
        usuario=self.textUser.toPlainText()
        contrasenia=self.textPass.text()
        cta=self.bd.getCta(usuario)
        print(cta)
        if cta!=None and cta[0][3]==None:
            #Fecha y hora UTC-00
            if self.controlaFechaHora(cta[0][2]):
                if contrasenia==cta[0][1]:
                    print("Login correcto.")
                    self.btnIngresar.setVisible(False)
                    self.p = principal.clsTable(self.bd.getId(cta[0][0])[0][0])
                    self.p.show()

                    self.hide()
                else:
                    self.mje=Mje.clsMsjAlert("Contraseña incorrecta.")
                    self.mje.show()
            else:
                self.mje=Mje.clsMsjAlert("La cuenta ha sido bloqueada.\nSolicite a un administrador que restablezca su contraseña.")
                self.mje.show()
        else:
            self.mje=Mje.clsMsjAlert("La cuenta ingresada no existe.")
            self.mje.show()



    def controlaFechaHora(self,fchHora):
        """Que  """
        #Fecha y hora UTC-00
        if fchHora!=None:
            ahora=datetime.datetime.utcnow()
            if ahora.date()<=fchHora.date() and ahora.time()<=fchHora.time():
                return True
            else:
                return False
        return True



    def cerrar(self):
        self.close()


def main():
	app = QtWidgets.QApplication(sys.argv)	
	form = clsLogin()
	form.show()
	app.exec_()

if __name__ == '__main__':
	main()