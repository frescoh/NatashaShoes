from PyQt5 import QtWidgets, uic

import sys

class clsMsjAlert(QtWidgets.QMainWindow):

	def __init__(self,mje):
		super(clsMsjAlert, self).__init__()
		self.mje=mje
		uic.loadUi('ui files/msj.ui',self)


		self.setupUi()


	def setupUi(self):
		self.label.setText(self.mje)
		self.btnAceptar.clicked.connect(self.cerrar)


	def cerrar(self):
		self.close()


def main():
	app = QtWidgets.QApplication(sys.argv)	
	
	form = clsMsjAlert()
	form.show()
	app.exec_()

if __name__ == '__main__':
	main()