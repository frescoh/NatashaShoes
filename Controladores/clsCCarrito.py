import Controladores.clsConexion as conector
#import clsConexion as conector

class clsCCarrito:

        def __init__(self):
            self.bd= conector.clsConexion()
        
        def getData(self):
            query = "SELECT * FROM carrito;"
            result = self.bd.run_query(query)
            if len(result)==0:
                return None
            else:
                return result
            


        def getCarrito(self,idUsuario):
        # idproducto, codigo, nombreTipo, idMarca, Modelo, color, PrecioVenta, Cantidad
            query ="SELECT "\
                    +"producto.idProducto AS 'ID Producto', "\
                    +"producto.codProducto AS Codigo, "\
                    +"tipo.nombreTipo AS Tipo , "\
                    +"marca.nombreMarca AS Marca, "\
                    +"producto.modelo AS Modelo, "\
                    +"producto.color AS Color, "\
                    +"producto.talle as Talle, "\
                    +"producto.precioVenta as Precio, "\
                    +"carrito.cantidad as Cantidad "\
                +"FROM carrito "\
                    +"INNER JOIN usuario ON carrito.idUsuario = usuario.idUser "\
                    +"INNER JOIN producto ON carrito.idProducto = producto.idProducto "\
                    +"INNER JOIN marca ON producto.idMarca = marca.idMarca "\
                    +"INNER JOIN tipo ON producto.idTipo = tipo.idTipo "\
                +"WHERE carrito.idUsuario='%d';" %(idUsuario)
            result = self.bd.run_query(query)
            if len(result)==0:
                return None
            else:
                return result
        
        def insert(self,idUsuario,idProducto, cantidad):
            query = "INSERT INTO carrito "\
                +"(idUsuario,idProducto, cantidad) \
                VALUES('%d','%d','%d');"\
                %(idUsuario,idProducto, cantidad)     
            self.bd.run_query(query) 
        
        #Se usara para evaluar si un producto ya esta en el carrito - Si result != None -> Update else insert
        def cantidadByIdAndProducto(self, idUsuario, idProducto):   
            query= "SELECT cantidad FROM carrito WHERE idUsuario = '%d' AND  idProducto = '%d';" %(idUsuario, idProducto)
            result = self.bd.run_query(query)
            if len(result) ==0:
                return None
            else:
                return result
        
        def reemplazar(self, idUsuario, idProducto, cantidad):
            query = "UPDATE carrito SET cantidad = '%d' WHERE idUsuario = '%d' and idProducto = '%d';"\
                %(cantidad,idUsuario, idProducto)
            self.bd.run_query(query)

        def update(self, idUsuario, idProducto, cantidad):
            query = "UPDATE carrito SET cantidad = cantidad + '%d' WHERE idUsuario = '%d' and idProducto = '%d';"\
                %(cantidad,idUsuario, idProducto)
            self.bd.run_query(query)
        
        def deleteProducto(self, idUsuario,idProducto):
                query = "DELETE FROM carrito WHERE idProducto= '%d' AND idUsuario ='%d';" %(idProducto,idUsuario)
                self.bd.run_query(query)
        
        def deleteCarrito(self, idUsuario):
                query = "DELETE FROM carrito WHERE  idUsuario ='%d';" %(idUsuario)
                self.bd.run_query(query)