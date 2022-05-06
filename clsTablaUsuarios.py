from os import close
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QTableWidgetItem
import sys

import Controladores.clsC_Usuarios as CrudUsuarios
import clsRegistroCta as loadForm
import datetime


class clsTablaUsuarios(QtWidgets.QMainWindow):
    def __init__(self,parent=None):
        super(clsTablaUsuarios, self).__init__(parent)
        uic.loadUi('ui files/listado.ui', self)
        self.bd = CrudUsuarios.clsC_Usuarios()
        self.table= self.bd.getTablaSP()
        self.setupUiComponents()


    def setupUiComponents(self):
        self.loadTable()
        self.tblData.resizeColumnsToContents()
        self.tblData.resizeRowsToContents()
        self.btnSalir.clicked.connect(self.cerrar)
        self.btnAgregar.clicked.connect(self.agregarUsuario)
        self.tblData.doubleClicked.connect(self.loadForm)
        self.btnActualizar.clicked.connect(self.refresh)
        self.btnEliminar.clicked.connect(self.eliminaUno)

    def loadTable(self):
        rowI = 0
        for row in self.table:
            self.tblData.setRowCount(rowI+1)
            self.tblData.setHorizontalHeaderLabels(["ID","DNI", "Nombre", "Apellido", "Fecha de Nacimiento",
                                                   "Dirección", "E-mail", "Telefono", "Fecha de alta","Fecha de Baja", "Usuario", "Tipo de cuenta"])
            if rowI == 0:
                columns = len(row)
                self.tblData.setColumnCount(columns)

            columns = len(row)
            for columnJ in range(columns):
                if row[columnJ]==None:
                    myValue = "-"
                else:
                    myValue = row[columnJ]
                cell = QTableWidgetItem(str(myValue))

                self.tblData.setItem(rowI, columnJ, cell)

            rowI = rowI + 1

    def refresh(self):
        self.table=self.bd.getTablaSP()
        self.loadTable()

    def eliminaUno(self):
        fila=self.tblData.selectedIndexes()[0].row()
        idFila=self.tblData.item(fila,0).text()
        fch=datetime.date.today()
        self.bd.inhabilitarUser(idFila,fch)
        cell = QTableWidgetItem(str(fch))
        self.tblData.setItem(fila, 9, cell)
        #self.tblData.removeRow(fila)


    def agregarUsuario(self):
        self.w=loadForm.clsRegistroCta()
        self.w.show()
    
    def loadForm(self,index):
        row = index.row()
        self.w=loadForm.clsRegistroCta(row,self)
        self.w.show()

    def cerrar(self):
        self.close()

    def getDato(self,f,c):
        return self.tblData.item(f, c).text()




def main():
	app = QApplication(sys.argv)
	
	objeto = clsTablaUsuarios()
	objeto.show()
	app.exec_()

if __name__ == '__main__':
	main()