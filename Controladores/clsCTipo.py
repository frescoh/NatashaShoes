import Controladores.clsConexion as conector

class clsCTipo:
        def __init__(self):
                 self.bd= conector.clsConexion()
    
        def getData(self):
                query = "SELECT * from tipo ORDER BY nombreTipo;"
                result = self.bd.run_query(query)
                if (len(result)==0):
                        return None
                else:
                        return result

        def getNombreTipo(self, idTipo):
                query = "select nombreTipo from tipo WHERE idTipo = '%d';" %(idTipo)
                result = self.bd.run_query(query)
                if len(result) == 0:
                        return None
                else:
                        return result

        def getIdByNombre(self,nombre):
                query= "select idTipo from tipo where nombreTipo= '"+nombre+"';"
                print(query)
                result = self.bd.run_query(query)
                if (len(result)==0):
                        return None
                else:
                        return result
        
        def insert(self, tipo):
                query = "INSERT INTO tipo (nombreTipo) VALUES ('%s');"%(tipo)          
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
        
