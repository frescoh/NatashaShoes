import Controladores.clsConexion as conector
#import clsConexion as conector

class clsCProducto:
        def __init__(self):
                 self.bd= conector.clsConexion()
    
        def getData(self):
                query = "SELECT " \
                                +"producto.idProducto as ID, " \
                                +"producto.codProducto as Codigo, " \
                                +"tipo.nombreTipo as Tipo, "\
                                +"marca.nombreMarca as Marca, " \
                                +"proveedor.razonSocial as Proveedor, "\
                                +"pais.nombrePais as Origen, "\
                                +"producto.modelo as Modelo, "\
                                +"producto.color as Color, " \
                                +"producto.talle as Talle, " \
                                +"producto.stock as Unidades, "\
                                +"producto.precioVenta as Precio "\
                        +"FROM producto "\
                                +"INNER JOIN tipo ON producto.idTipo = tipo.idTipo "\
                                +"INNER JOIN marca ON producto.idMarca= marca.idMarca "\
                                +"INNER JOIN proveedor ON producto.idProveedor = proveedor.idProveedor "\
                                +"INNER JOIN pais ON producto.idPais = pais.idPais "\
                        +"ORDER BY producto.idProducto;"
                result = self.bd.run_query(query)
                if (len(result)==0):
                        return None
                else:
                        return result

        def getStock(self, idProducto):
                query = "SELECT "\
                                +"stock "\
                        +"FROM producto "\
                        +"WHERE idProducto= '%d'" %(idProducto)
                result = self.bd.run_query(query)
                if (len(result)==0):
                        return None
                else:
                        return result


        def getTipoyMarca(self, idProducto):
                query = "SELECT tipo.nombreTipo, marca.nombreMarca FROM producto INNER JOIN tipo ON producto.idTipo = tipo.idTipo INNER JOIN marca ON producto.idMarca = marca.idMarca WHERE idProducto = '%d';" %(idProducto)
                result = self.bd.run_query(query)
                if len(result)==0:
                        return None
                else: 
                        return result


        def getDataAdmin(self):
                query = "SELECT "\
                                +"producto.idProducto as ID, "\
                                +"producto.codProducto as Codigo, "\
                                +"tipo.nombreTipo as Tipo, "\
                                +"marca.nombreMarca as Marca, "\
                                +"proveedor.razonSocial as Proveedor, "\
                                +"pais.nombrePais as Origen, "\
                                +"producto.modelo as Modelo, "\
                                +"producto.color as Color, "\
                                +"producto.talle as Talle, "\
                                +"producto.stock as Unidades, "\
                                +"producto.precioCompra as 'Precio de Compra', "\
                                +"producto.precioVenta as 'Precio de Venta' "\
                        +"FROM producto  "\
                                +"INNER JOIN tipo ON producto.idTipo = tipo.idTipo  "\
                                +"INNER JOIN marca ON producto.idMarca= marca.idMarca "\
                                +"INNER JOIN proveedor ON producto.idProveedor = proveedor.idProveedor "\
                                +"INNER JOIN pais ON producto.idPais = pais.idPais "\
                        +"ORDER BY producto.idProducto;"
                result = self.bd.run_query(query)

                if (len(result)==0):
                        return None
                else:
                        return result
                

        def getDescripcion(self, idProducto):
                query = "SELECT "\
                                +"producto.idProducto AS Producto, "\
                                +"producto.codProducto AS Codigo, "\
                                +"tipo.nombreTipo AS Tipo, "\
                                +"marca.idMarca AS marca, "\
                                +"producto.modelo AS Modelo, "\
                                +"producto.color AS Color, "\
                                +"producto.talle AS Talle "\
                        +"FROM producto "\
                                +"INNER JOIN tipo ON producto.idTipo = tipo.idTipo "\
                                +"INNER JOIN marca ON producto.idMarca = marca.idMarca "\
                        +"WHERE producto.idProducto = '%d';" %(idProducto)
                result = self.bd.run_query(query)
                if (len(result)==0):
                        return None
                else:
                        return result

        def getModelos(self):
                query = "SELECT idProducto, modelo FROM producto ORDER BY modelo;"
                result = self.bd.run_query(query)

                if (len(result)==0):
                        return None
                else:
                        return result
        
        def getIdByCodigo(self,codigo):
                query= "select idProducto from producto where codProducto= '"+codigo+"';"
                result = self.bd.run_query(query)
                if (len(result)==0):
                        return None
                else:
                        return result

        def insert(self,codigo, idTipo, idMarca, idProveedor, idPais,modelo, color,talle,unidades, precioCompra, precioVenta):
                query = "INSERT INTO producto "\
                        +"(codProducto, idTipo, idMarca, idProveedor, idPais, modelo, color, talle, stock, precioCompra, precioVenta )"\
			+"VALUES('%s','%d','%d','%d','%d','%s',	'%s','%d','%d','%s', '%s');"\
                        %(codigo, idTipo, idMarca, idProveedor, idPais,modelo, color,talle,unidades, precioCompra, precioVenta)          
                self.bd.run_query(query)
                        
        
        #Devuelve el ultimo ID insertado en la DB 
        #Usar inmediatamente despues de un INSERT. En otro contexto no funciona  
        def ultimateID(self): 
                query = "SELECT @@identity AS id"
                result = self.bd.run_query(query)
                if len(result)==0:
                        return None
                else:
                        return result
        

        
        def delete(self, ID):
                query = "DELETE FROM producto WHERE idProducto= " + str(ID) + ";"
                self.bd.run_query(query)
        
        def getCantidadByCod(self,codigo):
                query = "SELECT stock FROM producto where codProducto= '%s';" %(codigo)
                result = self.bd.run_query(query)
                if len(result)==0:
                        return None
                else:
                        return result

        def getPrecio(self,idProducto):
                query = "SELECT precioVenta FROM producto where idProducto= '%s';" %(idProducto)
                result = self.bd.run_query(query)
                if len(result)==0:
                        return None
                else:
                        return result


        def updateVenta(self,id,cantidad):
                query = "UPDATE `producto` SET `stock`= `stock`- '%d'  WHERE idProducto='%d';" %(cantidad,id)
                self.bd.run_query(query) 

        def update(self,id,codProducto, idTipo, idMarca, idProveedor, idPais, modelo, color, talle, stock, precioCompra, precioVenta):
                query = "UPDATE producto SET codProducto= '%s', idTipo ='%d',  idMarca = '%d', idProveedor = '%d',idPais= '%d', modelo = '%s',color= '%s', talle= '%d',stock= '%d', precioCompra= '%s', precioVenta= '%s' WHERE idProducto= '%d';" \
                %(codProducto, idTipo, idMarca, idProveedor, idPais, modelo, color, talle, stock, precioCompra, precioVenta,id)
                self.bd.run_query(query)

        

