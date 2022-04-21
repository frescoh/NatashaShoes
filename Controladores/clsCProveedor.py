import Controladores.clsConexion as conector
#import clsConexion as conector

class clsCProveedor:
        def __init__(self):
                self.bd= conector.clsConexion()
        
        def getData(self):
                query = "SELECT * from proveedor;"
                result = self.bd.run_query(query)
                if (len(result)==0):
                        return None
                else:
                        return result
        
        def getRazonSocial(self):
                query = "SELECT idProveedor, razonSocial FROM proveedor ORDER BY razonSocial;"
                result = self.bd.run_query(query)
                if len(result)==0:
                        return None
                else:
                        return result

        def getProveedor(self, id):
                query= "SELECT "\
                                +"proveedor.idProveedor, proveedor.razonSocial, pais.nombrePais, proveedor.direccion, proveedor.telefono, "\
                                +"proveedor.email,proveedor.fechaAltaProveedor, proveedor.observacion "\
                        +"FROM proveedor INNER JOIN pais ON proveedor.idPais = pais.idPais "\
                        +"WHERE proveedor.idProveedor= '%d';"%(id)
                result = self.bd.run_query(query)
                if len(result)==0:
                        return None
                else:
                        return result
                
        def insert(self,razonSocial, idPais, direccion, telefono, email, fechaAlta, observaciones):
                query= "INSERT INTO proveedor "\
                                +"(razonSocial, idPais, direccion, telefono, email, fechaAltaProveedor, observacion) "\
                                +"VALUES('%s','%d','%s','%s','%s','%s','%s'); "\
                                %(razonSocial, idPais, direccion, telefono, email, fechaAlta, observaciones)
                self.bd.run_query(query)
        
        def update(self,id,razonSocial, idPais, direccion, telefono, email, observaciones):
                query= "UPDATE proveedor SET razonSocial = '%s', idPais= '%d', direccion= '%s', telefono= '%s', email= '%s',  observacion= '%s' WHERE idProveedor = '%d';"\
                        %(razonSocial, idPais, direccion, telefono, email, observaciones,id)
                self.bd.run_query(query)

                """     id              %d
                        razonSocial     %s
                        idPais          %d
                        direccion       %s
                        telefono        %s
                        email           %s
                        fechaAlta       %s
                        observaciones   %s
                """

        def getIdByRS(self,razonSocial):
                query= "SELECT idProveedor FROM proveedor WHERE razonSocial= '%s';"%(razonSocial)
                result = self.bd.run_query(query)
                if (len(result)==0):
                        return None
                else:
                        return result
    
    #Devuelve el ultimo ID insertado en la DB 
    #Usar inmediatamente despues de un INSERT. En otro contexto no funciona  
        def ultimateID(self): 
            query = "SELECT @@identity AS id"
            result = self.bd.run_query(query)
            if len(result)==0:
                    return None
            else:
                    return result


""" coso = clsCProveedor()
print(coso.getProveedor(1)) """