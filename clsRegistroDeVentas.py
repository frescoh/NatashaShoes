from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import QMessageBox, QLineEdit, QTableWidgetItem,QInputDialog
from PyQt5.QtGui import QIcon
import sys

import Controladores.clsCVenta as conectorVenta
import clsDetalleDeVenta as detalle

class clsRegistroDeVentas(QtWidgets.QMainWindow):
    def __init__(self):
        super(clsRegistroDeVentas,self).__init__()
        self.__row = -1
        self.objVenta = conectorVenta.clsCVenta()
        uic.loadUi('ui files/regVentas.ui',self)
        self.setupUiComponents()

    

    def setupUiComponents(self):
        self.setWindowTitle("Registro de Ventas")
        self.loadTable()
        self.btnDetalle.setEnabled(False)
        self.btnSalir.clicked.connect(self.close)
        self.btnDetalle.clicked.connect(self.verDetalle)
        self.tblVentas.doubleClicked.connect(self.verDetalleDC)
        self.tblVentas.cellClicked.connect(self.posicion)
        self.tblVentas.doubleClicked.connect(self.verDetalle)
    
    def posicion(self,row, colum):
        self.__row = row
        self.btnDetalle.setEnabled(True)
    
    
    def verDetalle(self):
        print("id venta= ",int(self.tblVentas.item(self.__row,0).text()))
        self.dv = detalle.clsDetalleDeVenta(int(self.tblVentas.item(self.__row,0).text()))
        self.dv.show()

    @QtCore.pyqtSlot(QtCore.QModelIndex)
    def verDetalleDC(self,index):
        self.verDetalle()

    

    def loadTable(self):
        try:
            result = self.objVenta.getData()  #idVenta,vendedor.nombre,vendedor.apellido, cliente.nombre, cliente.apellido, fecha, importe, medioDePago.nombreMedioDePago
            print("Result loadTable registro de venta exitoso")
            self.tblVentas.setRowCount(0)
            self.tblVentas.setColumnCount(6)
            #'id','Vendedor', 'cliente', 'Fecha', 'Importe', 'Medio de pago'
            self.tblVentas.setHorizontalHeaderLabels(['id','Vendedor', 'cliente', 'Fecha', 'Importe', 'Medio de pago'])
                
            while self.tblVentas.rowCount():
                self.tblVentas.removeRow(0)
            for fila  in result:
                elem = []
                for i in range(len(fila)):
                    if i not in [1,2,3,4]:
                        elem.append(fila[i])
                    else:
                        if i == 2:
                            elem.append(fila[1]+' '+fila[2])
                        elif i == 3:
                            elem.append(fila[3]+' '+fila[4])
                row = self.tblVentas.rowCount()
                self.tblVentas.setRowCount(row + 1)
                for i in range(len(elem)):
                    cell = QTableWidgetItem(str(elem[i]))
                    cell.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)  # make cell not editable
                    self.tblVentas.setItem(row,i,cell)
            self.tblVentas.resizeColumnsToContents()
            self.tblVentas.resizeRowsToContents()
        except Exception as e:
                print('Error en la carga de la grilla ' + str(e))
    

    def closeEvent(self, event):
        resultado =  QMessageBox.question(self,"Salir...","¿Confirma que desea salir de la aplicacion?", #(self, titulo, mensaje, botones
		QMessageBox.Yes|QMessageBox.No)
        if resultado == QMessageBox.Yes: event.accept()
        else: event.ignore()


def main():
    app = QtWidgets.QApplication(sys.argv)
    form = clsRegistroDeVentas()
    form.show()
    app.exec_()

if __name__ == '__main__':
	main()