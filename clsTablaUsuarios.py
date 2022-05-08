from os import close
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import QApplication, QLineEdit
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtGui import QIcon
import sys

import Controladores.clsC_Usuarios as CrudUsuarios
import clsRegistroCta as loadForm
import datetime


class clsTablaUsuarios(QtWidgets.QMainWindow):
    """ 
    Administra la vista de la tabla de usuarios"""
    def __init__(self,parent=None):
        super(clsTablaUsuarios, self).__init__(parent)
        uic.loadUi('ui files/listado.ui', self)
        action = self.ledBuscar.addAction(QIcon("ui files/search.png"), QLineEdit.LeadingPosition)
        self.bd = CrudUsuarios.clsC_Usuarios()
        self.table= self.bd.getTablaSP()
        self.setupUiComponents()


    def setupUiComponents(self):
        """ 
        Inicializa los componentes"""
        self.loadTable()
        self.tblData.resizeColumnsToContents()
        self.tblData.resizeRowsToContents()
        self.btnSalir.clicked.connect(self.cerrar)
        self.btnAgregar.clicked.connect(self.agregarUsuario)
        self.tblData.doubleClicked.connect(self.loadForm)
        self.btnActualizar.clicked.connect(self.refresh)
        self.btnEliminar.clicked.connect(self.eliminaUno)
        self.cbAdmin.stateChanged.connect(self.filtrar)
        self.cbVendedor.stateChanged.connect(self.filtrar)
        self.cbCliente.stateChanged.connect(self.filtrar)

        self.cbCliente.setChecked(True)
        self.cbAdmin.setChecked(True)
        self.cbVendedor.setChecked(True)

    def filtrar(self):
        """ 
        Se activa cada vez que haya una modificacion en los checkboxes, permite filtrar por tipo de usuario"""
        usuarios= []
        if self.cbAdmin.isChecked():
            usuarios.append(0)
        if self.cbVendedor.isChecked():
            usuarios.append(1)
        if self.cbCliente.isChecked():
            usuarios.append(12)
        self.table= self.bd.getTabla(usuarios)
        self.loadTable()

    def loadTable(self):
        """ 
        Carga la tabla de usuarios con los registros que encuentre en la variable table"""
        rowI = 0
        if type(self.table)==tuple:
            for row in self.table:
                self.tblData.setHorizontalHeaderLabels(["ID","DNI", "Nombre", "Apellido", "Fecha de Nacimiento","Dirección", "E-mail", "Telefono", "Fecha de alta","Fecha de Baja", "Usuario", "Tipo de cuenta"])
                self.tblData.setRowCount(rowI+1)                
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
        else:
            self.tblData.setHorizontalHeaderLabels(["ID","DNI", "Nombre", "Apellido", "Fecha de Nacimiento","Dirección", "E-mail", "Telefono", "Fecha de alta","Fecha de Baja", "Usuario", "Tipo de cuenta"])
            self.tblData.setRowCount(0)
    
            

    def refresh(self):
        """ 
        Carga nuevamente la tabla desde DB teniendo en cuenta el estado actual de los checkboxes
        """
        self.table= self.bd.getTablaSP()
        self.filtrar()

    def eliminaUno(self):
        """ 
        Delete sobre un registro"""
        #Completar para hacer eliminacion logica

        fila=self.tblData.selectedIndexes()[0].row()
        idFila=self.tblData.item(fila,0).text()
        fch=datetime.date.today()
        self.bd.inhabilitarUser(idFila,fch)
        cell = QTableWidgetItem(str(fch))
        self.tblData.setItem(fila, 9, cell)
        #self.tblData.removeRow(fila)


    def agregarUsuario(self):
        """ 
        Crea un usuario nuevo"""
        self.w=loadForm.clsRegistroCta()
        self.w.show()
    
    def loadForm(self,index):
        """ 
        Vista que permite la carga de un usuario nuevo
        """
        row = index.row()
        self.w=loadForm.clsRegistroCta(row,self)
        self.w.show()

    def cerrar(self):
        self.close()




def main():
	app = QApplication(sys.argv)
	
	objeto = clsTablaUsuarios()
	objeto.show()
	app.exec_()

if __name__ == '__main__':
	main()