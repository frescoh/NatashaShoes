from os import X_OK
from PyQt5 import QtWidgets, uic


import sys
import clsC_Usuarios as CrudUsuarios
import clsMsjAlert as Mje
import clsSendMail as EnviarMail

class clsCambioPass(QtWidgets.QMainWindow):

    def __init__(self,user):
        super(clsCambioPass, self).__init__()
        uic.loadUi('ui/changePass.ui',self)
        self.user=user
        self.bd=CrudUsuarios.clsC_Usuarios()
        self.idUser=self.bd.getId(user)[0][0]
        self.datos=self.bd.getDatos(self.idUser)

        self.setupUi()
        
    def setupUi(self):
        self.chkPassAct.stateChanged.connect(lambda:self.verPass(1))
        self.chkNewPass.stateChanged.connect(lambda:self.verPass(2))
        self.chkNewPass2.stateChanged.connect(lambda:self.verPass(3))
        self.btnAceptar.clicked.connect(self.setPass)
        self.btnCancelar.clicked.connect(self.cerrar)

    def setPass(self):
        oldP=self.oldPass.text()
        if self.datos[0][10]==oldP:
            newP1=self.newPass.text()
            newP2=self.newPass2.text()
            if newP1==newP2:
                self.bd.setPass(newP1,self.idUser)
                self.mail=EnviarMail.clsSendMail(newP1,self.datos[0][2],self.datos[0][6],None,True)
                self.mje=Mje.clsMsjAlert("Se ha cambiado la contraseña.\nSe ha enviado un mail a su correo notificando este cambio.")
                self.mje.show()
                self.cerrar()
            else:
                self.mje=Mje.clsMsjAlert("La nueva contraseña no coincide.\nControle que la nueva contraseña sea la misma en ambos campos.")
                self.mje.show()
        else:
            self.mje=Mje.clsMsjAlert("La contraseña actual es incorrecta.")
            self.mje.show()
        
    def verPass(self,item):
        if item==1:
            chk=self.chkPassAct
            txtItem=self.oldPass
        elif item==2:
            chk=self.chkNewPass
            txtItem=self.newPass
        else:
            chk=self.chkNewPass2
            txtItem=self.newPass2
        if chk.isChecked():
            txtItem.setEchoMode(QtWidgets.QLineEdit.Normal)
        else:
            txtItem.setEchoMode(QtWidgets.QLineEdit.Password)
        

    def cerrar(self):
        self.close()


def main():
	app = QtWidgets.QApplication(sys.argv)	
	
	window = clsCambioPass()
	window.show()
	app.exec_()

if __name__ == '__main__':
	main()