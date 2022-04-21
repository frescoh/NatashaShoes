import Controladores.clsConexion as conector

class clsCVenta:
        def __init__(self):
                 self.bd= conector.clsConexion()
        
        #idVenta,vendedor.nombre,vendedor.apellido, cliente.nombre, cliente.apellido, fecha, importe, medioDePago.nombreMedioDePago
        def getData(self):
                query = "SELECT "\
                                +"idVenta AS ID, "\
                                +"vendedor.nombre AS 'Nombre del vendedor' , "\
                                +"vendedor.apellido AS 'Apellido del vendedor' , "\
                                +"cliente.nombre AS 'Nombre del cliente' , "\
                                +"cliente.apellido AS 'Apellido del cliente' , "\
                                +"fecha AS Fecha, "\
                                +"importe AS Importe, "\
                                +"mediodepago.nombreMedioDePago AS 'Medio de pago' "\
                        +"FROM venta "\
                                +"INNER JOIN mediodepago ON venta.idMedioDePago = mediodepago.idMedioDePago "\
                                +"INNER JOIN usuario AS vendedor ON venta.idVendedor = vendedor.idUser "\
                                +"INNER JOIN usuario AS cliente ON venta.idCliente = cliente.idUser "\
                        +"ORDER BY idVenta; "
                result = self.bd.run_query(query)
                if (len(result)==0):
                        return None
                else:
                        return result

        
        # retona id del ingreso
        def insert(self,idVendedor,idCliente, fecha,importe,idMedioDePago):
            query = "INSERT INTO venta (idVendedor,idCliente,fecha,importe,idMedioDePago) VALUES ('%d','%d','%s','%s','%d');"%(idVendedor, idCliente, fecha,importe,idMedioDePago)          
            self.bd.run_query(query)
            query = "SELECT @@identity AS id"
            result = self.bd.run_query(query)
            if len(result)==0:
                    return None
            else:
                    return result
        def updateTotal(self,idVenta,importe):
                query = "UPDATE `venta` SET `importe`= `importe`-'%s'  WHERE idProducto='%d';" %(importe,idVenta)
                self.bd.run_query(query) 
        
        