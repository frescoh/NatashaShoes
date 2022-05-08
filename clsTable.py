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
        self.tabla = []

        #Carrito
        self.__rowCarrito = -1

        uic.loadUi('ui files/winVenta.ui',self)
        self.setupUiComponents()
        #self.setupVistaUser(self.__tipo)

    
   
    

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
        items = self.cboCondicion.addItems(['en','<','=','>'])
        

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
        self.menuUsuarioCambiarPass.triggered.connect(self.changePass)
        self.menuAdministrarVentas.triggered.connect(self.verVentas)
        self.menuAdministrarUsuarios.triggered.connect(self.verUsuarios)
        self.menuAdministrarProveedores.triggered.connect(self.verProveedores)

        
        # Line edit
        self.ledBusqueda.textChanged.connect(self.filterBy)

        action = self.ledBusqueda.addAction(QIcon("ui files/search.png"), QLineEdit.LeadingPosition)     
        
        

        if self.__idRolUsuario  == 0 : # 0 - Admin | 1 - Vendedor | 12 - Cliente 
            """ 
            Habilita las opciones administrativas solo para los administradores"""
            self.frameAdmin.setVisible(True)
            self.menuBar.setVisible(True)
        
        if self.__idRolUsuario == 12:
            self.btnVender.setText("Comprar")

        self.loadTable()
        self.loadCarrito(self.tblCarrito)

    def verProveedores(self):
        """Muestra la lista de proveedores del negocio"""
        pass



    def getIdRol(self):
        """
        Devuelve el ID del rol de usuario almacenado en la tabla tipocuenta
        Con esto podemos saber el rol del usuario según el numero de id"""
        return self.__idRolUsuario
    
    def getIdUser(self):
        """Devuelve el ID  del usuario. Con esta informacion podemos saber que usuario es el que se leggeó"""
        return self.__idUser

    def verVentas(self):
        """Muestra una tabla con todas las ventas realizadas desde el sistema"""
        self.v= ventas.clsRegistroDeVentas()
        self.v.show()

    def verUsuarios(self):
        """Muestra una tabla con todos los usuarios registrados en el sistema"""
        self.u = formUsuarios.clsTablaUsuarios()
        self.u.show()

    def changePass(self):
        """
        Permite cambiar la contraseña del usuario actual
        Envía un mail al correo registrado para el usuario, informando que se raalizó la accion
        """
        self.c = cambio.clsCambioPass(self.__nickUsuario)
        self.c.show()

    def loadCarrito(self,carrito):      
        """
        Carga el carrito con los productos que se vayan seleecionando para la venta"""  
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
        """
        Elimina un producto del carrito y lo devuelve a la tabla de productos"""
        try:
            idProducto = int(self.tblCarrito.item(self.__rowCarrito,0).text().split('/')[0])
            self.objCarrito.deleteProducto(self.__idUser,idProducto)
            self.loadCarrito(self.tblCarrito)
        except Exception as e:
                print('Error en quitarProducto ' + str(e))



    def definirTipoUSer(self): # 0 - admin  1 - Vendedor 
        """
        Hace una lectura de la tabla usuario y carga los datos del usuarui actual en variables locales
        nombreUsurio: Nombre real del usuario
        idRolUsuario: Define el rol dentro del sistema, puede ser administrador, vendedor o cliente
        nickUsuario: Además del nombre real, el usuario puede tener un nick que se almacena en el campo user de su registro
        """
        try:
            result = self.objUsuario.getData(self.__idUser)
            if result != None:
                self.__nombreUsuario= result[0][0]
                self.__idRolUsuario = result[0][1]
                self.__nickUsuario = result[0][2]
        except Exception as e:
                print('Error en la definirTipoUser ' + str(e))
                
    def selectCell(self,row,column):
        """
        Define las acciones que se realizan cuando se hace click sobre una celda de la tabla"""
        self.__row = row
        self.__column = column
        self.btnCargarEnCarrito.setEnabled(True)
        self.btnVender.setEnabled(True)
        self.btnModificar.setEnabled(True)
        self.btnEliminarFila.setEnabled(True)
        self.lblColumna.setText(self.tblMercaderia.horizontalHeaderItem(column).text())

    
    def marcarFila(self,row,column):
        """
        Habilita el boton de eliminar fila, para poder eliminar un producto del carrito"""
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
        """
        Carga la tabla con todos los productos de la tienda"""
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
        """
        Elimina un producto de la tabla de productos"""
        i= o
        while i <len(self.tabla) and tabla[i][0]!= idProducto:
            i+=1
        if self.tabla[i][0]==idProducto:
            self.tabla.pop(i)


    def delete(self):
        """
        Responde al click del boton eliminar fila de la tabla de productos"""
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
        """ 
        Ordena la tabla de productos segun la columna que se haya seleccionado para realizar la accion"""
        for i in range(len(self.tabla)-1):
            for j in range(i+1,len(self.tabla)):
                if self.tabla[i][self.__column] > self.tabla[j][self.__column]:
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

  
    """
    def buscarTabla(self, indice):
        #Metodo aparentemente deprecado
        i = 0
        while i < len(self.tabla) and int(self.__tabla[i][0])!=indice:
            i+=1
        if int(self.__tabla[i][0])==indice:
            return i
        else: 
            return -1
    """

    def vender(self):
        """ 
        Metodo del carrito que lleva a una vista donde se concretará la venta"""
        if self.tblCarrito.rowCount()==0:
            self.cargarCarro()
        self.cv = formVenta.clsConcretarVenta(self)
        self.cv.show()

    def setupCarritoVacio(self):
        """ 
        Cuando el carrito está vacio, este metodo configura botones y etiquetas para mantener la coherencia"""
        self.btnEliminar.setEnabled(False)
        self.btnLimpiarCarrito.setEnabled(False)
        if self.__row==-1:
            self.btnVender.setEnabled(False)
        self.lblTotal.setText('$0.00')

    
    def setupCarritoOcupado(self):
        """ Cuando el carrito no esta vacio, este metodo habilita las vistas para mantener la coherencia
        """
        self.btnLimpiarCarrito.setEnabled(True)
        self.btnVender.setEnabled(True)


    def limpiarCarrito(self):
        """ 
        Elimina el carrito de un usuario"""
        try:
            self.objCarrito.deleteCarrito(self.__idUser)
            self.loadCarrito(self.tblCarrito)
        except Exception as e:
                print('Error en la limpieza ' + str(e))


    @QtCore.pyqtSlot(QtCore.QModelIndex)
    def dcGrilla(self, index):
        """ 
        Realiza distintas acciones para el doble click en la tabla de productos, según el rol del usuario y según la columna clickeada
        Admin: 
        doble click en columnna:
            Proveedores: Muestra informacion del proveedor
            otra: Pide cantidad de productos para cargarlo en le carrito 

        Vendedor/Cliente: Pide cantidad de productos para cargarlo en le carrito 
        """
        if self.__idRolUsuario== 0:
            if self.__column==4:
                self.p= formProveedor.clsFormProveedor(self,'cm',self.__row)
                self.p.show()
            else:
                self.cargarCarro()
        else:
            self.cargarCarro()
        

    def update(self):
        """" 
        Abre ventana con informacion del producto seleccionado con la posibilidad de modificarla"""
        self.w = formProducto.clsFormProducto(self.tblMercaderia,self.tabla,self.__row)
        self.w.show()

    def insert(self):
        """ 
        Permite cargar un producto en la taba, mediante una venta de producto vacia
        """
        self.w = formProducto.clsFormProducto(self.tblMercaderia,self.tabla)
        self.w.show()
        
            
    def getCantidad(self):
        """ 
        InputDialog que pide cantidad
        El usuario debe ingresar un valor mayor o igual  1
        devuelve 0 si el usuario cancela 
        """
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
        """ 
        Carga la tabla carrito con un registro nuevo
        Si el producto ya existia en el carrito, suma la nueva cantidad"""
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
        """ 
        Ordena la vista segun la columna seleccionada por el usuario y el texto ingresado en el cuadro de busqueda"""
        #Vacío la tabla
        while self.tblMercaderia.rowCount()>0:
            self.tblMercaderia.removeRow(0)
        rowI=0
        reader = self.tabla
        for row in reader:
            columns = len(row)
            if str(self.ledBusqueda.text()).lower() in str(row[self.__column]).lower():
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