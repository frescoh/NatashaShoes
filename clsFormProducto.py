import PyQt5
from PyQt5 import QtCore, QtWidgets, uic
from PyQt5.QtWidgets import QMessageBox, QInputDialog, QLineEdit, QTableWidgetItem

import sys
import Controladores.clsCProducto as conectorProducto
import Controladores.clsCTipo as conectorTipo
import Controladores.clsCMarca as conectorMarca
import Controladores.clsCProveedor as conectorProveedor
import Controladores.clsCPais as conectorOrigen
import clsFormProveedor as formProveedor
# https://www.pythonguis.com/tutorials/pyqt-dialogs/
# Hacer modal
class clsFormProducto(QtWidgets.QMainWindow):
    def __init__(self,ObjTabla=None,vecTabla=None,row=None):
        super(clsFormProducto, self).__init__()
        uic.loadUi('ui files/form.ui',self)
        self.__table= ObjTabla
        self.__nRow= row
        self.__vecTabla = vecTabla
        
        self.objProducto = conectorProducto.clsCProducto()
        self.objTipo = conectorTipo.clsCTipo()
        self.objMarca = conectorMarca.clsCMarca()
        self.objProveedor = conectorProveedor.clsCProveedor()
        self.objOrigen = conectorOrigen.clsCPais()

        self.original=''
        


        self.setupUiComponents()

        

        if self.__table !=None and self.__nRow!=None and self.__vecTabla!=None:
            self.loadValues()
            
        
    def loadCombo(self,combo, valor):
        i= 0
        while i< combo.count()-1 and valor!= self.getValor(combo.currentText()):
            i+=1
            combo.setCurrentIndex(i)

    def loadValues(self):
        """ index = self.cboTipo.findText(self.__table.item(self.__nRow,2).text(), QtCore.Qt.MatchFixedString)
        if index >= 0:
         self.cboTipo.setCurrentIndex(index) """
        self.original = self.__table.item(self.__nRow,1).text() + self.__table.item(self.__nRow,2).text() +self.__table.item(self.__nRow,3).text()+\
            self.__table.item(self.__nRow,4).text() + self.__table.item(self.__nRow,5).text() + self.__table.item(self.__nRow,6).text() + \
            self.__table.item(self.__nRow,7).text() + self.__table.item(self.__nRow,8).text() + self.__table.item(self.__nRow,9).text() + \
            self.__table.item(self.__nRow,10).text() + self.__table.item(self.__nRow,11).text()
        
        self.ledCodigo.setText(self.__table.item(self.__nRow,1).text())
        self.loadCombo(self.cboTipo, self.__table.item(self.__nRow,2).text())
        self.loadCombo(self.cboMarca,self.__table.item(self.__nRow,3).text())
        self.loadCombo(self.cboProveedor,self.__table.item(self.__nRow,4).text())
        self.loadCombo(self.cboOrigen,self.__table.item(self.__nRow,5).text())
        self.ledModelo.setText(self.__table.item(self.__nRow,6).text())
        self.ledColor.setText(self.__table.item(self.__nRow,7).text())
        self.ledTalle.setText(self.__table.item(self.__nRow,8).text())
        self.ledUnidades.setText(self.__table.item(self.__nRow,9).text())
        self.ledPrecioCompra.setText(self.__table.item(self.__nRow,10).text())
        self.ledPrecioVenta.setText(self.__table.item(self.__nRow,11).text())
        
    def setupUiComponents(self):
        if self.__nRow == None:
            self.setWindowTitle("Nuevo producto")
        else: 
            self.setWindowTitle("Modifica producto")

        #Carga de los ComboBox
        self.cboTipo.addItems(self.getList(self.objTipo.getData()))
        self.cboMarca.addItems(self.getList(self.objMarca.getData()))
        self.cboProveedor.addItems(self.getList(self.objProveedor.getRazonSocial()))
        self.cboOrigen.addItems(self.getList(self.objOrigen.getData()))

        self.btnGuardar.setEnabled(False)
        
        #Eventos para Botones
        self.btnGuardar.clicked.connect(self.guardar)
        self.btnSalir.clicked.connect(self.salir)

        #Evento para QLine Edit
        self.ledCodigo.editingFinished.connect(self.validarCodigo)
        self.ledTalle.editingFinished.connect(self.validarTalle)
        self.ledUnidades.editingFinished.connect(self.validarUnidades)
        self.ledPrecioCompra.editingFinished.connect(self.validarPrecioCompra)
        self.ledPrecioVenta.editingFinished.connect(self.validarPrecioVenta)
        self.ledModelo.editingFinished.connect(self.evalGuardar)
        self.ledColor.editingFinished.connect(self.capColor)


        #Agrega elementos desde evento de ComboBox
        self.cboTipo.currentIndexChanged.connect(self.nuevoTipo)
        self.cboMarca.currentIndexChanged.connect(self.nuevaMarca)
        self.cboProveedor.currentIndexChanged.connect(self.nuevoProveedor)
        self.cboOrigen.currentIndexChanged.connect(self.nuevoPais)
        
    def capColor(self):
        self.ledColor.setText(self.ledColor.text().capitalize())
        self.evalGuardar()

    def nuevoTipo(self):
        if self.cboTipo.currentText().lower()=='agregar':
            nombreTipo, ok = QInputDialog().getText(self, "Nuevo tipo",
                                     "Ingrese el nuevo tipo", QLineEdit.Normal,)
            if ok and nombreTipo:
                id = self.objTipo.getIdByNombre(nombreTipo)
                if id!=None: 
                    QMessageBox.warning(self, 'Error ', 'El tipo ingresado ya existe. Por favor ingrese otro o seleccione el existente')
                    self.cboTipo.setCurrentIndex(0)
                else:
                    self.objTipo.insert(nombreTipo.capitalize())
                    self.cboTipo.clear()
                    self.cboTipo.addItems(self.getList(self.objTipo.getData()))
                    self.loadCombo(self.cboTipo,nombreTipo.capitalize())
            else: 
                self.cboTipo.setCurrentIndex(0)
        self.evalGuardar()
    
    
                   
    def inhabAll(self):
        self.ledCodigo.setEnabled(False)
        self.ledModelo.setEnabled(False)
        self.ledColor.setEnabled(False)
        self.ledTalle.setEnabled(False)
        self.ledUnidades.setEnabled(False)
        self.ledPrecioCompra.setEnabled(False)
        self.ledPrecioVenta.setEnabled(False)

        self.cboTipo.setEnabled(False)
        self.cboMarca.setEnabled(False)
        self.cboProveedor.setEnabled(False)
        self.cboOrigen.setEnabled(False)
    
    def habAll(self):
        self.ledCodigo.setEnabled(True)
        self.ledModelo.setEnabled(True)
        self.ledColor.setEnabled(True)
        self.ledTalle.setEnabled(True)
        self.ledUnidades.setEnabled(True)
        self.ledPrecioCompra.setEnabled(True)
        self.ledPrecioVenta.setEnabled(True)

        self.cboTipo.setEnabled(True)
        self.cboMarca.setEnabled(True)
        self.cboProveedor.setEnabled(True)
        self.cboOrigen.setEnabled(True)
        
    def evalGuardar(self):
        if(self.ledCodigo.text() != '' and self.ledModelo.text() != '' and self.ledColor.text() != '' and \
        self.ledTalle.text() != '' and self.ledUnidades.text() != '' and self.ledPrecioCompra.text() != '' and\
        self.ledPrecioVenta.text() != '' and \
        self.ledCodigo.isEnabled() and self.ledModelo.isEnabled() and self.ledColor.isEnabled() and \
        self.ledTalle.isEnabled() and self.ledUnidades.isEnabled() and self.ledPrecioCompra.isEnabled() and\
        self.ledPrecioVenta.isEnabled()):
            self.btnGuardar.setEnabled(True)
        else:
            self.btnGuardar.setEnabled(False)

    def nuevaMarca(self):
        if self.cboMarca.currentText().lower()=='agregar':
            nombreMarca, ok = QInputDialog().getText(self, "Nueva marca",
                                     "Ingrese la nueva marca: ", QLineEdit.Normal,)
            if ok and nombreMarca:
                id = self.objMarca.getIdByNombre(nombreMarca)
                if id!=None: 
                    QMessageBox.warning(self, 'Error ', 'La marca ingresada ya existe. Por favor ingrese otra o seleccione la  existente')
                    self.cboMarca.setCurrentIndex(0)
                else:
                    self.objMarca.insert(nombreMarca.capitalize())
                    self.cboMarca.clear()
                    self.cboMarca.addItems(self.getList(self.objMarca.getData()))
                    self.loadCombo(self.cboMarca,nombreMarca.capitalize())
            else: 
                self.cboMarca.setCurrentIndex(0)
                    
        self.evalGuardar()
    
    def validarTalle(self):
        talle = self.ledTalle.text()
        try:
            talle = int(talle)
            if talle <1: 
                QMessageBox.warning(self, 'Error ', 'El talle no puede ser un valor nulo o negativo')
                self.inhabAll()
                self.ledTalle.setEnabled(True)
            else:
                self.habAll()
                self.evalGuardar()
        except Exception as e:
            print('Error en validarTalle ' + str(e))
            self.inhabAll()
            self.ledTalle.setEnabled(True)
    
    def validarUnidades(self):
        unidades = self.ledUnidades.text()
        try:
            unidades = int(unidades)
            if unidades <1: 
                QMessageBox.warning(self, 'Error ', 'El valor no puede ser un valor nulo o negativo')
                self.inhabAll()
                self.ledUnidades.setEnabled(True)
            else: 
                self.habAll()
                self.evalGuardar()
        except Exception as e:
            print('Error en ValidarUnidades ' + str(e)) 
            QMessageBox.warning(self, 'Error ', 'El valor ingresado no es entero')
            self.inhabAll()
            self.ledUnidades.setEnabled(True)
    
    def validarPrecio(self,ledPrecio):
        val = ledPrecio.text()
        if val!='':
            try:
                val = float(val)
                if val <1: 
                    QMessageBox.warning(self, 'Error ', 'El valor no puede ser un valor nulo o negativo')
                    self.inhabAll()
                    ledPrecio.setEnabled(True)
                else:
                    self.habAll()
                    self.evalGuardar()
            except Exception as e:
                print('Error en validarPrecio ' + str(e)) 
                QMessageBox.warning(self, 'Error ', 'El valor ingresado no es numerico')
                self.inhabAll()
                ledPrecio.setEnabled(True)
    
    def validarPrecioCompra(self):
            self.validarPrecio(self.ledPrecioCompra)
        
    def validarPrecioVenta(self):
        self.validarPrecio(self.ledPrecioVenta)

    def nuevoProveedor(self):
        if self.cboProveedor.currentText().lower() == 'agregar':
            self.p = formProveedor.clsFormProveedor(self,'nf')
            self.p.show()
        self.evalGuardar()
    
    def nuevoPais(self):
        if self.cboOrigen.currentText().lower()=='agregar':
            nombrePais, ok = QInputDialog().getText(self, "Nuevo pais",
                                     "Ingrese el nuevo pais: ", QLineEdit.Normal,)
            if ok and nombrePais:
                id = self.objOrigen.getIdByNombre(nombrePais)
                if id!=None: 
                    QMessageBox.warning(self, 'Error ', 'El nombre del pais ingresado ya existe. Por favor ingrese otro o seleccione el existente')
                    self.cboOrigen.setCurrentIndex(0)
                else:
                    self.objOrigen.insert(nombrePais.capitalize())
                    self.cboOrigen.clear()
                    self.cboOrigen.addItems(self.getList(self.objOrigen.getData()))
                    self.loadCombo(self.cboOrigen,nombrePais.capitalize())
            else: 
                self.cboOrigen.setCurrentIndex(0)
        self.evalGuardar()

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


    def getList(self, result):     
        comboList=[]
        for elem in result:
            comboList.append(str(elem[1]) + ":" + str(elem[0]))    
        comboList.append('Agregar')    
        return comboList

    def validarCodigo(self):
        id = self.objProducto.getIdByCodigo(self.ledCodigo.text())
        if self.__nRow==None:
            if id!=None:
                QMessageBox.warning(self, 'Error ', 'El codigo ingresado ya está en uso. Por favor ingrese otro') 
                self.inhabAll()
                self.ledCodigo.setEnabled(True)
            else:
                self.habAll()
                self.evalGuardar()
        else:
            if id!=None:
                if id[0][0] !=int(self.__table.item(self.__nRow,0).text()):
                    QMessageBox.warning(self, 'Error ', 'El codigo ingresado pertenece a otro producto. Por favor ingrese otro o mantenga el anterior:') 
                    self.inhabAll()
                    self.ledCodigo.setEnabled(True)
            else:
                self.habAll()
        self.evalGuardar()

    def limpiar(self):
        self.ledCodigo.setText('')
        self.ledModelo.setText('')
        self.ledColor.setText('')
        self.ledTalle.setText('')
        self.ledUnidades.setText('')
        self.ledPrecioCompra.setText('')
        self.ledPrecioVenta.setText('')
        self.btnGuardar.setEnabled(False)

    def guardar(self):
        self.codigo = self.ledCodigo.text()
        self.idTipo = self.getIndice(self.cboTipo.currentText())
        self.idMarca = self.getIndice(self.cboMarca.currentText())
        self.idProveedor = self.getIndice(self.cboProveedor.currentText())
        self.idPais= self.getIndice(self.cboOrigen.currentText())
        self.modelo = self.ledModelo.text()
        self.color = self.ledColor.text()
        self.talle = int(self.ledTalle.text())
        self.unidades = int(self.ledUnidades.text())
        self.precioCompra = self.ledPrecioCompra.text()
        self.precioVenta = self.ledPrecioVenta.text()        
        
        if self.__nRow==None:            
            try:
                self.objProducto.insert(self.codigo, self.idTipo, self.idMarca, self.idProveedor, \
                self.idPais,self.modelo, self.color,self.talle,self.unidades, self.precioCompra, self.precioVenta)
                self.id = int(self.objProducto.ultimateID()[0][0])
                filaNueva = [self.id,self.ledCodigo.text(),self.getValor(self.cboTipo.currentText()),self.getValor(self.cboMarca.currentText()) ,\
                    self.getValor(self.cboProveedor.currentText()),self.getValor(self.cboOrigen.currentText()),self.modelo,self.color,\
                    int(self.talle),int(self.unidades),float(self.precioCompra), float(self.precioVenta)]
                row = self.__table.rowCount()
                row += 1
                self.__table.setRowCount(row)

                for i in range(len(filaNueva)):
                    cell = QTableWidgetItem(str(filaNueva[i]))
                    cell.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)  # make cell not editable
                    if i>7:
                        cell.setTextAlignment(QtCore.Qt.AlignRight) #Alineo a la derecha
                    self.__table.setItem(row-1,i,cell)
                self.__table.resizeColumnsToContents()
                self.__table.resizeRowsToContents()
                self.__vecTabla.append(filaNueva)
                QMessageBox.about(self, "Perfecto!", "Los datos fueron guardados exitosamente")
                self.limpiar()
            except Exception as e:
                print('Error en insertar fila nueva ' + str(e))
        else:
            cadena  =  self.ledCodigo.text()+self.getValor(self.cboTipo.currentText())+self.getValor(self.cboMarca.currentText()) +\
            self.getValor(self.cboProveedor.currentText())+self.getValor(self.cboOrigen.currentText())+self.modelo+self.color+\
            str(self.talle)+str(self.unidades)+ self.precioCompra+self.precioVenta
            self.id= int(self.__table.item(self.__nRow,0).text())
            fila = [self.id,self.ledCodigo.text(),self.getValor(self.cboTipo.currentText()),self.getValor(self.cboMarca.currentText()) ,\
                self.getValor(self.cboProveedor.currentText()),self.getValor(self.cboOrigen.currentText()),self.modelo,self.color,int(self.talle),\
                    int(self.unidades),float(self.precioCompra), float(self.precioVenta)]
            if cadena != self.original:
                self.objProducto.update(self.id, self.codigo, self.idTipo, self.idMarca, self.idProveedor, self.idPais, self.modelo, self.color,\
                     self.talle, self.unidades, self.precioCompra, self.precioVenta)
                self.orderVec()

                pos = self.busq(int(self.id))
                if pos>=0:
                    self.__vecTabla[pos]= fila
                for i in range(len(fila)):
                    cell = QTableWidgetItem(str(fila[i]))
                    cell.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)  # make cell not editable
                    if i>7:
                        cell.setTextAlignment(QtCore.Qt.AlignRight) #Alineo a la derecha
                    self.__table.setItem(self.__nRow,i,cell)
                    self.__table.resizeColumnsToContents()
                    self.__table.resizeRowsToContents()
                QMessageBox.about(self, "Perfecto!", "Los datos fueron actualizados exitosamente")
                self.close()
            else: 
                print("Las cadenas son iguales")
                QMessageBox.about(self, "Nada!", "No hay cambios que guardar.")
                

    def busq(self,id):
        ini= 0
        fin = len(self.__vecTabla)-1
        med = (ini+fin)//2
        while self.__vecTabla[med][0] != id and ini<fin:
            if self.__vecTabla[med][0]<id:
                ini = med+1
            else:
                fin = med-1
            med = (ini+fin)//2
        if self.__vecTabla[med][0] ==id:
            return med
        else: 
            return -1

    def orderVec(self):
        for i in range(len(self.__vecTabla)-1):
            for j in range(i+1,len(self.__vecTabla)):
                if self.__vecTabla[i][0] > self.__vecTabla[j][0]:
                    self.__vecTabla[i], self.__vecTabla[j] = self.__vecTabla[j],self.__vecTabla[i]

    def salir(self):
        self.close()


def main():
    app = QtWidgets.QApplication(sys.argv)
    
    form = clsFormProducto()
    form.show()
    app.exec_()

if __name__ == '__main__':
    main()