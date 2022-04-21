import Controladores.clsConexion as conector

class clsCPais:
        def __init__(self):
                 self.bd= conector.clsConexion()
    
        def getData(self):
                query = "SELECT * from pais ORDER BY nombrePais;"
                result = self.bd.run_query(query)
                if (len(result)==0):
                        return None
                else:
                        return result
        
        def getIdByNombre(self,nombre):
                query= "select idPais from pais where nombrePais= '"+nombre+"';"
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
        
        def insert(self, pais):
                query = "INSERT INTO pais (nombrePais) VALUES ('%s');"%(pais)          
                self.bd.run_query(query)