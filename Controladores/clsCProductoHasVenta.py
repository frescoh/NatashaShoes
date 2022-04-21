import Controladores.clsConexion as conector
#import clsConexion as conector

class clsCProductoHasVenta:
        def __init__(self):
            self.bd= conector.clsConexion()


        def getData(self,idVenta):  # idVenta, vendedor.nombre, vendedor.apellido, comprador.nombre, comprador.apellido,
                                    # productoID, tipo.nombre, marca.nombre, producto.modelo, producto.color, producto.talle
                                    # cantidad, precio 'agregar precio total por producto' 
            query = "SELECT "\
                        +"producto_has_venta.idVenta AS idVenta, "\
                        +"vendedor.nombre AS NombreVendedor, "\
                        +"vendedor.apellido AS ApellidoVendedor, "\
                        +"comprador.nombre AS Nombrecomprador, "\
                        +"comprador.apellido AS Apellidocomprador, "\
                        +"producto.idProducto AS IDProducto, "\
                        +"tipo.nombreTipo AS Tipo, "\
                        +"marca.nombreMarca AS Marca, "\
                        +"producto.modelo AS Modelo, "\
                        +"producto.color AS Color, "\
                        +"producto.talle AS Talle, "\
                        +"producto_has_venta.cantidad AS Cantidad, "\
                        +"producto_has_venta.precioUnidad AS Precio  "\
                    +"FROM producto_has_venta "\
                        +"INNER JOIN venta ON producto_has_venta.idVenta = venta.idVenta "\
                        +"INNER JOIN usuario AS comprador ON venta.idCliente = comprador.idUser "\
                        +"INNER JOIN usuario AS vendedor ON venta.idVendedor = vendedor.idUser "\
                        +"INNER JOIN producto ON producto_has_venta.idProducto = producto.idProducto "\
                        +"INNER JOIN tipo ON producto.idTipo = tipo.idTipo "\
                        +"INNER JOIN marca on producto.idMarca = marca.idMarca "\
                    +"WHERE producto_has_venta.idVenta = '%d' ;" %(idVenta)
            result = self.bd.run_query(query)
            if len(result)==0:
                return None
            else:
                return result
        
        def insert(self, idVenta, idProducto, cantidad,precio):
            query = "INSERT INTO producto_has_venta (idVenta,idProducto,cantidad,precioUnidad) VALUES ('%d','%d','%d','%s');"%(idVenta,idProducto,cantidad,precio)          
            self.bd.run_query(query)