import Controladores.clsConexion as conector
#import clsConexion as conector

class clsCMediosDePago:
        def __init__(self):
                 self.bd= conector.clsConexion()
    
        def getData(self):
                query = "SELECT * FROM mediodepago ORDER BY mediodepago.idMedioDePago;"
                result = self.bd.run_query(query)
                if (len(result)==0):
                        return None
                else:
                        return result