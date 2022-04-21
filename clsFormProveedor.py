import PyQt5
from PyQt5 import QtCore, QtWidgets, uic
from PyQt5.QtCore import QDateTime, Qt
from PyQt5.QtWidgets import QMessageBox, QInputDialog, QLineEdit, QTableWidgetItem
import Controladores.clsCProveedor as conectorProveedor
import Controladores.clsCPais as conectorPais
import clsFormProducto as formProducto
import sys

class clsFormProveedor(QtWidgets.QMainWindow):
    def __init__(self, ob= None,t=None, fila = None): 
        # called from clsFormProducto.nuevoProveedor() y clsTable.dcGrilla y desde la grilla de gestion de proveedores
        # Grilla envia clsTable envia id Proveedor y clsFormProducto envia el formulario completo
        # Para resolver esto se podra llamar a la funcion con dos  argumentos (idProveedor o form) y tipoDellamada
        # Valor de ib según el tipo de llamada: 
        # 'cm' = consult - Mercaderia (recibe a clsTable como argumento) desde clsTable
        # 'cp' = consult - Proveedores (Consulta, recibe la grilla Proveedores) desde clsTableProveedores. Actualiza los datos
        # 'nf' = new - form (recibe clsFormProducto) desde clsFormProducto
        # 'ng' = new - grid (recibe grilla para actualizar) desde clsTableProveedores. Inserta al final de la grilla
        

        super(clsFormProveedor, self).__init__()
        uic.loadUi('ui files/proveedor.ui',self)
        self.__obj = ob
        self.__idLLam = t
        self.__row = fila
        self.__idProveedor = None
        self.objProveedor = conectorProveedor.clsCProveedor()
        self.objPais = conectorPais.clsCPais()
        self.setupUiComponents()
        if self.__obj  != None:
            self.loadValues()
        
    def setupUiComponents(self):
        
        #Inicializacion
        #self.lblTitulo.setText("Nuevo Proveedor")
        self.setWindowTitle("Ingreso de proveedor nuevo")
        self.tedObservaciones.setText("Ingrese un maximo de 200 caracters")
        self.cboPais.addItems(self.getList(self.objPais.getData()))
        self.datFechaAlta.setCalendarPopup(True)
        self.datFechaAlta.setDateTime(QDateTime.currentDateTime())
        self.datFechaAlta.setEnabled(False)
        
        
        #Eventos botones
        self.btnGuardar.clicked.connect(self.guardar)
        self.btnSalir.clicked.connect(self.cerrar)
        self.btnEditar.clicked.connect(self.habilitar)

        #Eventos QTextEdit obsercaciones
        #self.tedObservaciones.duoubleClicked.connect(self.controlCaracteres)
        self.tedObservaciones.cursorPositionChanged.connect(self.limpiarCuadro)
        self.tedObservaciones.textChanged.connect(self.controlCaracteres)
        
    def limpiarCuadro(self):
        if self.tedObservaciones.toPlainText() == 'Ingrese un maximo de 200 caracters':
            self.tedObservaciones.setText('')

    def controlCaracteres(self):
        numCaracteres = len( self.tedObservaciones.toPlainText())
        if numCaracteres <=200:
            self.lblContadorCaracteres.setText(str(numCaracteres)+"/200")
        else:
            self.tedObservaciones.setText(self.tedObservaciones.toPlainText()[:200])

    def guardar(self):
        razonSocial = self.ledRazonSocial.text()
        idPais = self.getIndice(self.cboPais.currentText())
        direccion = self.ledDireccion.text()
        telefono = self.ledTelefono.text()
        email = self.ledEmail.text()
        fechaAlta = self.datFechaAlta.dateTime()
        if self.tedObservaciones.toPlainText() == 'Ingrese un maximo de 200 caracters':
            observacion = ''
        else:
            observacion = self.tedObservaciones.toPlainText()
        

        if self.__idLLam.lower() == 'cm':
            self.guardarCM(razonSocial, idPais, direccion, telefono, email, observacion)
        elif self.__idLLam.lower() == 'cp':
            self.guardarCP(razonSocial, idPais, direccion, telefono, email, observacion)
        elif self.__idLLam.lower() == 'nf':
            self.guardarNF(razonSocial, idPais, direccion, telefono, email, fechaAlta, observacion)
        elif self.__idLLam.lower() == 'ng':
            self.guardarNG(razonSocial, idPais, direccion, telefono, email, fechaAlta, observacion)
            
    def guardarCM(self,razonSocial, idPais, direccion, telefono, email, observacion):
        try:
            self.objProveedor.update(self.__idProveedor, razonSocial, idPais, direccion, telefono, email, observacion)
            print("Insert exitoso")
            QMessageBox.about(self, "Perfecto!", "Los datos fueron actualizados correctamente.")
            if self.__obj.tblMercaderia.item(self.__row,4).text() != razonSocial:
                cell = QTableWidgetItem(razonSocial)
                cell.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)  # make cell not editable
                anterior = self.__obj.tblMercaderia.item(self.__row,4).text()
                for i in range(self.__obj.tblMercaderia.rowCount()):
                    if self.__obj.tblMercaderia.item(i,4).text()==anterior:
                        self.__obj.tblMercaderia.setItem(i,4,cell)
                        # nuevo cell para insertar en la siguiente celda
                        cell = QTableWidgetItem(razonSocial)
                        cell.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)  # make cell not editable
                for elem in self.__obj.tabla:
                    if elem[4] == anterior:
                        print(elem)
                        elem[4] = razonSocial      
        except Exception as e:
            print('Error en gardarCM ' + str(e))
            QMessageBox.about(self, "Error!", "No se pudo guardar la informacion debido a un error inesperado.")
            
    def guardarCP(self,razonSocial, idPais, direccion, telefono, email, observacion):
        try:
            self.objProveedor.update(self.__idProveedor, razonSocial, idPais, direccion, telefono, email, observacion)
        except Exception as e:
                print('Error en gardarCP ' + str(e))

    def guardarNF(self,razonSocial, idPais, direccion, telefono, email, fechaAlta, observacion):
        try:
            self.objProveedor.insert(razonSocial, idPais, direccion, telefono, email, fechaAlta, observacion)
            self.__obj.cboProveedor.clear()
            self.__obj.cboProveedor.addItems(self.getList(self.objProveedor.getRazonSocial()))
            self.__obj.loadCombo(self.__obj.cboProveedor,razonSocial)
        except Exception as e:
                print('Error en GuardarFN ' + str(e))

    def guardarNG(self,razonSocial, idPais, direccion, telefono, email, fechaAlta, observacion):
        try:
            self.objProveedor.insert(razonSocial, idPais, direccion, telefono, email, fechaAlta, observacion)
        except Exception as e:
                print('Error en GardarNG ' + str(e))

    def cerrar(self):
        self.close()

    def inhab(self):
        self.ledRazonSocial.setEnabled(False)
        self.ledDireccion.setEnabled(False)
        self.ledTelefono.setEnabled(False)
        self.ledEmail.setEnabled(False)
        self.tedObservaciones.setEnabled(False)
        self.cboPais.setEnabled(False)
        self.datFechaAlta.setEnabled(False)
    
    def habilitar(self):
        self.ledRazonSocial.setEnabled(True)
        self.ledDireccion.setEnabled(True)
        self.ledTelefono.setEnabled(True)
        self.ledEmail.setEnabled(True)
        self.tedObservaciones.setEnabled(True)
        self.cboPais.setEnabled(True)
    
    def loadCombo(self,combo, valor):
        i= 0
        while i< combo.count() and valor!= self.getValor(combo.currentText()):
            print(f"i= {i}, valor = {valor}, texto en celda = {self.getValor(combo.currentText())}")
            i+=1
            combo.setCurrentIndex(i)
    
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
           
    def loadValues(self):
        if self.__idLLam.lower() == 'cm':
            self.lblTitulo.setText("Consulta Proveedor")
            self.setWindowTitle("Consulta de un proveedor existente")
            self.inhab()
            try:
                self.__idProveedor = self.objProveedor.getIdByRS(self.__obj.tblMercaderia.item(self.__row,4).text())[0][0]
            except Exception as e:
                print('Error en loadValues ' + str(e))
        
        elif self.__idLLam.lower() == 'ng' or self.__idLLam.lower() =='nf':
            self.lblTitulo.setText("Nuevo proveedor")
            self.setWindowTitle("Ingresar nuevo proveedor")
            self.btnEditar.setVisible(False)

        elif self.__idLLam.lower() == 'cp':
            self.lblTitulo.setText("Consulta Proveedor")
            self.setWindowTitle("Consulta de un proveedor existente")
            self.inhab()
            # self.__idProveedor = int(grilla.item(self.__row,0).text())
        
        try:
            result = self.objProveedor.getProveedor( self.__idProveedor)[0]
            self.ledRazonSocial.setText(result[1])
            self.loadCombo(self.cboPais,result[2])
            self.ledDireccion.setText(result[3])
            self.ledTelefono.setText(result[4])
            self.ledEmail.setText(result[5])
            self.datFechaAlta.setDate(result[6])
            self.tedObservaciones.setText(result[7])
        except Exception as e:
                print('Error en la carga del formulario ' + str(e)) 

    def getList(self,result):
        comboList=[]
        for elem in result:
            comboList.append(str(elem[1]) + ":" + str(elem[0]))
        comboList.append('Agregar')
        return comboList

def main():
    app = QtWidgets.QApplication(sys.argv)
    form = clsFormProveedor()
    form.show()
    app.exec_()

if __name__ == '__main__':
    main()

