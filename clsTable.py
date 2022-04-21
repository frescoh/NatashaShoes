from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import QMessageBox, QLineEdit, QTableWidgetItem,QInputDialog
from PyQt5.QtGui import QIcon

import sys
import Controladores.clsCProducto as conector
import Controladores.clsCProveedor as conectorProveedor
import Controladores.clsCCarrito as conectorCarrito
import Controladores.clsCUsuario as conectorUsuario

import clsFormProducto as formProducto 
import clsFormProveedor as formProveedor
import clsConcretarVenta as formVenta
import clsRegistroDeVentas as ventas
import clsTablaUsuarios as formUsuarios
import clsCambioPass as cambio

class clsTable(QtWidgets.QMainWindow):
    def __init__(self,idUser= None):  
        super(clsTable,self).__init__()      
        self.__idUser = idUser                   
        self.__idRolUsuario = None     # 0 - Admin | 1 - Vendedor | 12 - Cliente 
        
        self.__nombreUsuario = ''
        self.__nickUsuario= ''
        
        self.objProducto= conector.clsCProducto() 
        self.objProveedor = conectorProveedor.clsCProveedor()
        self.objCarrito = conectorCarrito.clsCCarrito()
        self.objUsuario = conectorUsuario.clsCUsuario()
        
        #Tabla Mercaderia
        self.__row = -1
        self.__column = -1
        self.__numColumns =[] # ['1',...,'n']
        self.tabla = []

        #Carrito
        self.__rowCarrito = -1

        uic.loadUi('ui files/winVenta.ui',self)
        self.setupUiComponents()
        #self.setupVistaUser(self.__tipo)

    
    def verUsuarios(self):
        pass

    def cambiarPass(self):
        pass

    def getIdRol(self):
        return self.__idRolUsuario
    
    def getIdUser(self):
        return self.__idUser
    

    def setupUiComponents(self):
        self.definirTipoUSer()
        self.setWindowTitle("Natasha indumentarias System_User:"+self.__nombreUsuario)
        
        self.btnCargarEnCarrito.setEnabled(False)
        self.btnVender.setEnabled(False)
        self.frameAdmin.setVisible(False)
        self.menuBar.setVisible(False)
        self.tblCarrito.setAlternatingRowColors(True)
        self.tblMercaderia.setAlternatingRowColors(True)
        self.btnEliminar.setEnabled(False)
        self.btnModificar.setEnabled(False)
        self.btnEliminarFila.setEnabled(False)

        

        # Acciones Botones
        self.btnOrdenar.clicked.connect(self.ordenar)
        self.btnVender.clicked.connect(self.vender)
        self.btnLimpiarCarrito.clicked.connect(self.limpiarCarrito)
        self.btnEliminarFila.clicked.connect(self.delete)
        self.btnModificar.clicked.connect(self.update)
        self.btnAgregar.clicked.connect(self.insert)
        self.btnCargarEnCarrito.clicked.connect(self.cargarCarro)
        self.btnActualizar.clicked.connect(self.loadTable)
        self.btnCerrar.clicked.connect(self.close)
        self.btnEliminar.clicked.connect(self.quitarProducto)

        # Acciones Grilla
        self.tblMercaderia.resizeColumnsToContents()
        self.tblMercaderia.cellClicked.connect(self.selectCell)
        self.tblMercaderia.doubleClicked.connect(self.dcGrilla)
        self.tblCarrito.cellClicked.connect(self.marcarFila)

        #Menu
        self.menuVentas.triggered.connect(self.verVentas)
        self.menuUsuarios.triggered.connect(self.verUsuarios)
        self.menuCambiarPass.triggered.connect(self.changePass)

        
        # Line edit
        self.ledBusqueda.textChanged.connect(self.filterBy)

        action = self.ledBusqueda.addAction(QIcon("ui files/search.png"), QLineEdit.LeadingPosition)     
        
        

        if self.__idRolUsuario  == 0 : # 0 - Admin | 1 - Vendedor | 12 - Cliente 
            self.frameAdmin.setVisible(True)
            self.menuBar.setVisible(True)
        
        if self.__idRolUsuario == 12:
            self.btnVender.setText("Comprar")

        self.loadTable()
        self.loadCarrito(self.tblCarrito)
        items = self.cboColumna.addItems(self.__numColumns)
        self.sbFila.setMaximum(self.tblMercaderia.rowCount())
        self.sbFila.setMinimum(1)
    
    

    def verVentas(self):
        self.v= ventas.clsRegistroDeVentas()
        self.v.show()
    
    def verUsuarios(self):
        self.u = formUsuarios.clsTablaUsuarios()
        self.u.show()

    def changePass(self):
        self.c = cambio.clsCambioPass(self.__nickUsuario)
        self.c.show()

    def loadCarrito(self,carrito):        
        try:
            result= self.objCarrito.getCarrito(self.__idUser) 
            while carrito.rowCount():
                    self.tblCarrito.removeRow(0) 
            if result!=None:
                carrito.setRowCount(0)
                carrito.setColumnCount(4)
                carrito.setHorizontalHeaderLabels(["Producto","Precio", "Cantidad","Subtotal"])
                total = 0
                row = 0
                
                for compra in result: #"Producto","Precio", "Cantidad","Subtotal"
                    carrito.setRowCount(row+1)
                    fila = [] # producto(idproducto, codigo, nombreTipo, idMarca, Modelo, color,talle) PrecioVenta, Cantidad 
                    producto = '' 
                    for i in range(len(compra)-3):
                        producto = producto + str(compra[i]) +"/"
                    producto = producto + str(compra[6])
                    fila.append(producto)
                    fila.append(compra[7])
                    fila.append(compra[8])
                    for i in range(len(fila)):
                        cell = QTableWidgetItem(str(fila[i]))
                        cell.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)  # make cell not editable
                        if i!=0:
                            cell.setTextAlignment(QtCore.Qt.AlignRight) #Alineo a la derecha
                        carrito.setItem(row,i,cell)  
                    # Calcula el subtotal y lo agrega a la tabla en la ultima celda de la fila
                    subtotal = compra[7]*compra[8]
                    total += subtotal
                    cell = QTableWidgetItem(str(subtotal))
                    cell.setTextAlignment(QtCore.Qt.AlignRight) #Alineo a la derecha
                    cell.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)  # make cell not editable
                    carrito.setItem(row,len(fila),cell)
                    row+=1
                carrito.setRowCount(row+1)
                carrito.setSpan(row,0,1,3) #setSpan (fila, columna, el número de filas que se fusionarán, el número de columnas que se fusionarán)
                
                cell = QTableWidgetItem("Suma Total: ")
                cell.setTextAlignment(QtCore.Qt.AlignRight) #Alineo a la derecha
                cell.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)  # make cell not editable
                carrito.setItem(row,0,cell)

                cell = QTableWidgetItem(str(total))
                cell.setTextAlignment(QtCore.Qt.AlignRight) #Alineo a la derecha
                cell.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)  # make cell not editable
                carrito.setItem(row,3,cell)
                #carrito.item(row,3).setBackground(QtGui.QColor(248,000,000))
                
                carrito.resizeColumnsToContents()
                carrito.resizeRowsToContents()
                self.setupCarritoOcupado()
                
                self.lblTotal.setText('$ '+str(total))
                
            else:
                self.setupCarritoVacio() 
        except Exception as e:
                print('Error en la loadcarrito ' + str(e))



    def quitarProducto(self):
        try:
            idProducto = int(self.tblCarrito.item(self.__rowCarrito,0).text().split('/')[0])
            self.objCarrito.deleteProducto(self.__idUser,idProducto)
            self.loadCarrito(self.tblCarrito)
        except Exception as e:
                print('Error en quitarProducto ' + str(e))



    def definirTipoUSer(self): # 0 - admin  1 - Vendedor 
        try:
            result = self.objUsuario.getData(self.__idUser)
            if result != None:
                self.__nombreUsuario= result[0][0]
                self.__idRolUsuario = result[0][1]
                self.__nickUsuario = result[0][2]
        except Exception as e:
                print('Error en la definirTipoUser ' + str(e))






    def selectCell(self,row,column):
        self.__row = row
        self.__column = column
        self.sbFila.setValue(row+1)
        self.cboColumna.setCurrentText(str(column+1))
        self.btnCargarEnCarrito.setEnabled(True)
        self.btnVender.setEnabled(True)
        self.btnModificar.setEnabled(True)
        self.btnEliminarFila.setEnabled(True)

    
    def marcarFila(self,row,column):
        if row != self.tblCarrito.rowCount()-1:
            self.__rowCarrito= row
            self.btnEliminar.setEnabled(True)
            self.btnEliminar.setText("Eliminar \nFila "+str(row+1))
            codigo = self.tblCarrito.item(self.__rowCarrito,0).text().split('/')[1]
            total = int(self.objProducto.getCantidadByCod(codigo)[0][0])
            reservado = int(self.tblCarrito.item(self.__rowCarrito,2).text())
            self.lblDisponible.setText(str(total-reservado))
        else:
            self.btnEliminar.setEnabled(False)
            self.btnEliminar.setText("Eliminar \nFila")
        



    def loadTable(self):
        try:
            if self.__idRolUsuario == 0:
                result = self.objProducto.getDataAdmin()
                print("Result exitoso")
                self.tblMercaderia.setRowCount(0)
                self.tblMercaderia.setColumnCount(12)
                self.tblMercaderia.setHorizontalHeaderLabels(["ID", "Codigo", "Tipo", "Marca","Proveedor","Origen", "Modelo", "Color", "Talle","Unidades", "Precio de Compra", "Precio de Venta"])
                
            else:
                result = self.objProducto.getData()
                self.tblMercaderia.setRowCount(0)
                self.tblMercaderia.setColumnCount(11)
                self.tblMercaderia.setHorizontalHeaderLabels(["ID", "Codigo", "Tipo", "Marca","Proveedor","Origen", "Modelo", "Color", "Talle","Unidades", "Precio"])
            self.__numColumns = [str(i) for i in range(1,self.tblMercaderia.columnCount()+1)]
            self.tabla=[]
            while self.tblMercaderia.rowCount():
                self.tblMercaderia.removeRow(0)
            for elem in result:
                self.tabla.append(list(elem))
                row = self.tblMercaderia.rowCount()
                self.tblMercaderia.setRowCount(row + 1)
                for i in range(len(elem)):
                    
                    cell = QTableWidgetItem(str(elem[i]))
                    cell.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)  # make cell not editable
                    if i>7:
                        cell.setTextAlignment(QtCore.Qt.AlignRight) #Alineo a la derecha
                    self.tblMercaderia.setItem(row,i,cell)
                    if elem[9]==0:
                        self.tblMercaderia.item(row,i).setBackground(QtGui.QColor(231,37,18))
            self.tblMercaderia.resizeColumnsToContents()
            self.tblMercaderia.resizeRowsToContents()
        except Exception as e:
                print('Error en meter datos en la grilla ' + str(e))
    
    def closeEvent(self, event):
        resultado =  QMessageBox.question(self,"Salir...","¿Confirma que desea salir de la aplicacion?", #(self, titulo, mensaje, botones
		QMessageBox.Yes|QMessageBox.No)
        if resultado == QMessageBox.Yes: event.accept()
        else: event.ignore()
    
    def eliminarDeTabla(self, idProducto):
        i= o
        while i <len(self.tabla) and tabla[i][0]!= idProducto:
            i+=1
        if self.tabla[i][0]==idProducto:
            self.tabla.pop(i)


    def delete(self):
        if self.__row>-1 and self.__column>-1:
            ID = int(self.tblMercaderia.item(self.__row, 0).text())
            try:
                self.objProducto.delete(ID)
                print ("Exito. Eliminacion correcta de iris ID= " + str(ID))
                self.tblMercaderia.removeRow(self.__row)
                eliminarDeTabla(idProducto)
            except Exception as e:
                print('Error en la eliminacion ' + str(e))
        else:
            print ("Error. No seleccionó fila")
    
    def ordenar(self):
        col = int(self.cboColumna.currentText())-1
        for i in range(len(self.tabla)-1):
            for j in range(i+1,len(self.tabla)):
                if self.tabla[i][col] > self.tabla[j][col]:
                    self.tabla[i], self.tabla[j] = self.tabla[j],self.tabla[i]
        rowI=0
        for row in self.tabla:
            self.tblMercaderia.setRowCount(rowI+1)
            columns = len(row)
            for i in range(columns):
                cell = QTableWidgetItem(str(row[i]))
                cell.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)  # make cell not editable
                self.tblMercaderia.setItem(rowI,i,cell)
            rowI += 1
        self.tblMercaderia.resizeColumnsToContents()
        self.tblMercaderia.resizeRowsToContents()

    def buscarTabla(self, indice):
        i = 0
        while i < len(self.tabla) and int(self.__tabla[i][0])!=indice:
            i+=1
        if int(self.__tabla[i][0])==indice:
            return i
        else: 
            return -1


    def vender(self):
        if self.tblCarrito.rowCount()==0:
            self.cargarCarro()
        self.cv = formVenta.clsConcretarVenta(self)
        self.cv.show()

    def setupCarritoVacio(self):
        self.btnEliminar.setEnabled(False)
        self.btnLimpiarCarrito.setEnabled(False)
        if self.__row==-1:
            self.btnVender.setEnabled(False)
        self.lblTotal.setText('$0.00')

    
    def setupCarritoOcupado(self):
        self.btnLimpiarCarrito.setEnabled(True)
        self.btnVender.setEnabled(True)


    def limpiarCarrito(self):
        try:
            self.objCarrito.deleteCarrito(self.__idUser)
            self.loadCarrito(self.tblCarrito)
        except Exception as e:
                print('Error en la limpieza ' + str(e))


    @QtCore.pyqtSlot(QtCore.QModelIndex)
    def dcGrilla(self, index):
        if self.__idRolUsuario== 0:
            if self.__column==4:
                self.p= formProveedor.clsFormProveedor(self,'cm',self.__row)
                self.p.show()
            else:
                self.cargarCarro()
        else:
            self.cargarCarro()
        

    def update(self):
        self.w = formProducto.clsFormProducto(self.tblMercaderia,self.tabla,self.__row)
        self.w.show()

    def insert(self):
        self.w = formProducto.clsFormProducto(self.tblMercaderia,self.tabla)
        self.w.show()
        
            
    def getCantidad(self):
        try:
            cantidad ,ok = QInputDialog().getText(self, "Venta",
                                        "Cantidad: ", QLineEdit.Normal,)
            if not ok: 
                return 0
            cantidad = int(cantidad)
            if cantidad <1:
                return self.getCantidad()
            else:
                return cantidad
        except:
            return self.getCantidad()

    def cargarCarro(self):
        try:
            idProducto  = int(self.tblMercaderia.item(self.__row,0).text())
            cantidad =  self.getCantidad()  #0 si cancela
            if cantidad: # Compruebo si no canceló
                yaCargado = self.objCarrito.cantidadByIdAndProducto(self.__idUser, idProducto)
                disponible = int(self.tblMercaderia.item(self.__row,9).text())
                if yaCargado!= None: # El pruducto ya estaba en el carrito
                    yaCargado = int(yaCargado[0][0]) 
                    while cantidad and cantidad + yaCargado > disponible:  # Compruebo tener stock suficiente para cubrir el pedido
                        QMessageBox.warning(self, 'Error ', 'Solo disponemos de '+str(disponible)+" productos de ID "+self.tblMercaderia.item(self.__row,0).text()+" para vender y usted ingresó "+str(cantidad+yaCargado)+". Vuelva a intentarlo")
                        cantidad =  self.getCantidad()  #0 si cancela
                    if cantidad: # Nuevamente compruebo si no canceló
                        self.objCarrito.update(self.__idUser, idProducto, cantidad)
                else: # El producto se está ingresando por primera vez al carrito
                    while cantidad and cantidad > disponible: 
                        QMessageBox.warning(self, 'Error ', 'Solo disponemos de '+str(disponible)+" productos de iD "+self.tblMercaderia.item(self.__row,0).text()+" para vender y usted ingresó "+str(cantidad)+". Vuelva a intentarlo")
                        cantidad =  self.getCantidad()  #0 si cancela
                    if cantidad: 
                        self.objCarrito.insert(self.__idUser, idProducto, cantidad)
                self.loadCarrito(self.tblCarrito)
        except Exception as e:
                print('Error en la carga del carro ' + str(e))

    def filterBy(self):
        columna = int(self.cboColumna.currentText())-1
        #Vacío la tabla
        while self.tblMercaderia.rowCount()>0:
            self.tblMercaderia.removeRow(0)
        rowI=0
        reader = self.tabla
        for row in reader:
            columns = len(row)
            if str(self.ledBusqueda.text()).lower() in str(row[columna]).lower():
                self.tblMercaderia.setRowCount(rowI+1)
                for i in range(columns):
                        cell = QTableWidgetItem(str(row[i]))
                        cell.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)  # make cell not editable
                        self.tblMercaderia.setItem(rowI,i,cell)
                rowI += 1
        self.tblMercaderia.resizeColumnsToContents()
        self.tblMercaderia.resizeRowsToContents()



def main():
    app = QtWidgets.QApplication(sys.argv)
    form = clsTable()
    form.show()
    app.exec_()

if __name__ == '__main__':
	main()