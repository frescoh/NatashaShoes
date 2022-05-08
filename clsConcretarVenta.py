from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import QMessageBox, QLineEdit, QTableWidgetItem,QInputDialog
from PyQt5.QtGui import QIcon
import sys
from datetime import datetime 

import clsTable

import Controladores.clsCMediosDePago as conectorMP
import Controladores.clsCCarrito as conectorCarrito
import Controladores.clsCVenta as conectorVenta
import Controladores.clsCProducto as conectorProducto
import Controladores.clsCProductoHasVenta as conectorPHV
import Controladores.clsCUsuario as conectorUsuario


class clsConcretarVenta(QtWidgets.QMainWindow):
    def __init__(self, claseTable=None):
        super(clsConcretarVenta,self).__init__()
        self.clsTabla = claseTable
        self.importe = 'sin datos'
        self.__idCliente= None
        self.__faltantes = ''
        self.__vendido = False
        self.objMedioDePago = conectorMP.clsCMediosDePago()
        self.objCarrito = conectorCarrito.clsCCarrito()
        self.objVenta = conectorVenta.clsCVenta()
        self.objProducto = conectorProducto.clsCProducto()
        self.objPHV = conectorPHV.clsCProductoHasVenta()
        self.objUsuario = conectorUsuario.clsCUsuario()


        uic.loadUi('ui files/concretaVenta.ui',self)
        self.setupUiComponents()
        
    


    def reservar(self):
        j = 1
        result = self.objCarrito.getCarrito(self.clsTabla.getIdUser())
        for fila in result:
            idProducto = fila[0]
            cantidad= fila[8]
            disponible = self.objProducto.getStock(idProducto)[0][0]
            if disponible >=cantidad:
                self.objProducto.updateVenta(idProducto, cantidad)
            else: 
                self.objProducto.updateVenta(idProducto, disponible)
                self.objCarrito.reemplazar(self.clsTabla.getIdUser(),idProducto,disponible)
                self.__faltantes = self.__faltantes + str(j)+" - Producto ID= "+ str(idProducto) +\
                " Pedidos= "+str(cantidad)+" disponible= "+str(disponible)+". Se asignaron todas la unidades disponibles a esta compra.\n\n"
                j+=1
        if self.__faltantes != '':
            self.tedObservaciones.setText(self.__faltantes)




    def setupUiComponents(self):
        self.setWindowTitle("Concretar venta")
        if self.clsTabla.getIdRol() == 12:
            self.ledDNI.setVisible(False)
            self.lblDNI.setVisible(False)
            self.btnConsultarDNI.setVisible(False)
            self.btnNuevoCliente.setVisible(False)
            self.resize(471,585)

        self. btnFinalizar.setVisible(False)
        self.cboMedioDePago.addItems(self.getList(self.objMedioDePago.getData()))

        self.btnFinalizar.clicked.connect(self.cargarVenta)
        self.btnConsultarDNI.clicked.connect(self.consultarUsuario)
        self.reservar()
        self.clsTabla.loadCarrito(self.tblCarrito)
        self.clsTabla.loadCarrito(self.clsTabla.tblCarrito)
        self.importe= self.clsTabla.lblTotal.text()
        self.lblTotal.setText(str(self.importe))
        
    
    def consultarUsuario(self):
        try:
            result= self.objUsuario.getDatabyDNI(int(self.ledDNI.text()))
            if result!= None:
                self.ledDNI.setText(result[0][1]+" "+result[0][2])
                self.__idCliente = result[0][0]
                self.btnFinalizar.setVisible(True)
        except Exception as e:
                print('Error en ConsultarUsuario ' + str(e))
        
    
    def closeEvent(self, event):
        if self.__vendido:
            event.accept()
        else:
            resultado =  QMessageBox.question(self,"Salir...","¿Confirma que desea salir de la aplicacion?", #(self, titulo, mensaje, botones
            QMessageBox.Yes|QMessageBox.No)
            if resultado == QMessageBox.Yes: 
                self.devolverProductos()
                event.accept()
            else: 
                event.ignore()
            

    def devolverProductos(self):
        for i in range(self.tblCarrito.rowCount()-1):
            idProducto = int(self.tblCarrito.item(i,0).text().split('/')[0])
            cantidad= int(self.tblCarrito.item(i,2).text())
            self.objProducto.updateVenta(idProducto, -cantidad)


    def cargarVenta(self):
       # try:
        if self.clsTabla.getIdRol() == 12:
            id= self.objVenta.insert(0 ,self.clsTabla.getIdUser(), datetime.now(),float(self.tblCarrito.item(self.tblCarrito.rowCount()-1,3).text()),self.getIndice(self.cboMedioDePago.currentText()))[0][0]    
        else:
            id= self.objVenta.insert(self.clsTabla.getIdUser() , self.__idCliente, datetime.now(),float(self.tblCarrito.item(self.tblCarrito.rowCount()-1,3).text()),self.getIndice(self.cboMedioDePago.currentText()))[0][0]
        id= int(id)
        #self.objVenta.insert(idVendedor, idComprador, fecha, importe, idMedioDePago)
        for i in range(self.tblCarrito.rowCount()-1):
            idProducto = int(self.tblCarrito.item(i,0).text().split('/')[0])
            precio = float(self.objProducto.getPrecio(idProducto)[0][0])
            cantidad= int(self.tblCarrito.item(i,2).text())
            self.objPHV.insert(id, idProducto, cantidad,precio)
        self.clsTabla.limpiarCarrito()
        self.clsTabla.loadTable()
        QMessageBox.warning(self, 'Felicidades!', 'La venta fue cargada con exito')
        self.__vendido = True
        self.close()
        #except Exception as e:
        #       print('Error en cargarVenta ' + str(e))
        
            




    def loadCombo(self,combo, valor):
        i= 0
        while i< combo.count()-1 and valor!= self.getValor(combo.currentText()):
            i+=1
            combo.setCurrentIndex(i)
    
    
    def getList(self, result):     
        comboList=[]
        if result != None:
            for elem in result:
                comboList.append(str(elem[1]) + ":" + str(elem[0])) 
        return comboList
    


    def getIndice(self,elem):
            value = -1

            if (elem!=''):
                aux = elem.split(':')
                value = int(aux[1])

            return value
    
    def getValor(self,elem):
        value = -1
        if (elem!=''):
            aux = elem.split(':')
            value = aux[0]

        return value








def main():
    app = QtWidgets.QApplication(sys.argv)
    form = clsConcretarVenta()    
    form.show()
    app.exec_()

if __name__ == '__main__':
	main()