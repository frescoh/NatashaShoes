from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import QMessageBox, QLineEdit, QTableWidgetItem,QInputDialog
from PyQt5.QtGui import QIcon
import sys

import Controladores.clsCProductoHasVenta as conectorPHV

class clsDetalleDeVenta(QtWidgets.QMainWindow):
    def __init__(self, idVenta=None):
        super(clsDetalleDeVenta,self).__init__()
        self.__row = -1
        self.__idVenta = idVenta
        self.objPHV = conectorPHV.clsCProductoHasVenta()
        uic.loadUi('ui files/detalleDeVenta.ui',self)
        self.setupUiComponents()

  

    def setupUiComponents(self):
        self.setWindowTitle("Detalle de ventas")
        self.loadTable()
        self.btnAceptar.clicked.connect(self.close)
    

    def loadTable(self):
        try:
                    # idVenta, vendedor.nombre, vendedor.apellido, comprador.nombre, comprador.apellido,
                    # productoID, tipo.nombre, marca.nombre, producto.modelo, producto.color, producto.talle
                    # cantidad, precio 'agregar precio total por producto' 
            #['ID Venta','Vendedor', 'Cliente', 'ID Producto', 'Tipo', 'Marca', 'Modelo', 'Color', 'Talle', 'Cantidad', 'Precio', 'Subtotal' ]
            result = self.objPHV.getData(self.__idVenta)  #idVenta,vendedor.nombre,vendedor.apellido, cliente.nombre, cliente.apellido, fecha, importe, medioDePago.nombreMedioDePago
            print("Result: ",result)
            print("Result loadTable registro de venta exitoso")
            self.tblDetalle.setRowCount(0)
            self.tblDetalle.setColumnCount(12)
            #['ID Venta','Vendedor', 'Cliente', 'ID Producto', 'Tipo', 'Marca', 'Modelo', 'Color', 'Talle', 'Cantidad', 'Precio', 'Subtotal' ]
            self.tblDetalle.setHorizontalHeaderLabels(['ID Venta','Vendedor', 'Cliente', 'ID Producto', 'Tipo', 'Marca', 'Modelo', 'Color', 'Talle', 'Cantidad', 'Precio', 'Subtotal' ])
                
            while self.tblDetalle.rowCount():
                self.tblDetalle.removeRow(0)
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
                elem.append(fila[11]*fila[12])
                row = self.tblDetalle.rowCount()
                self.tblDetalle.setRowCount(row + 1)
                for i in range(len(elem)):
                    cell = QTableWidgetItem(str(elem[i]))
                    cell.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)  # make cell not editable
                    self.tblDetalle.setItem(row,i,cell)
            self.tblDetalle.resizeColumnsToContents()
            self.tblDetalle.resizeRowsToContents()
            
        except Exception as e:
                print('Error en loadTable ' + str(e))
        


def main():
    app = QtWidgets.QApplication(sys.argv)
    form = clsDetalleDeVenta()
    form.show()
    app.exec_()

if __name__ == '__main__':
    main()