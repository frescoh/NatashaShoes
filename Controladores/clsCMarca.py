import Controladores.clsConexion as conector

class clsCMarca:
        def __init__(self):
                 self.bd= conector.clsConexion()
    
        def getData(self):
                query = "SELECT * from marca ORDER By nombreMarca;"
                result = self.bd.run_query(query)
                if (len(result)==0):
                        return None
                else:
                        return result
        
        def getIdByNombre(self,nombre):
                        query= "select idMarca from marca where nombreMarca= '"+nombre+"';"
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
        
        def insert(self, marca):
                query = "INSERT INTO marca (nombreMarca) VALUES ('%s');"%(marca)          
                self.bd.run_query(query)