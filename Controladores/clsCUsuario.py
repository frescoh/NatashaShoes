import Controladores.clsConexion as conector

class clsCUsuario:
        def __init__(self):
                 self.bd= conector.clsConexion()
    
        def     getData(self,idUser):
                query = "SELECT "\
                                +"usuario.nombre AS Nombre, "\
                                +"tipocuenta.idTCta AS 'ID Tipo', "\
                                +"usuario.user as nick "\
                        +"FROM usuario "\
                            +"INNER JOIN tipocuenta ON usuario.idTCta = tipocuenta.idTCta "\
                        +"WHERE idUser = '%d';" %(idUser)
                result = self.bd.run_query(query)
                if (len(result)==0):
                        return None
                else:
                        return result
        
        def getDatabyDNI(self, dni):
                query = "SELECT "\
                                +"usuario.idUser AS ID, "\
                                +"usuario.nombre AS Nombre, "\
                                +"usuario.apellido AS Apellido "\
                        +"FROM usuario "\
                                +"WHERE dni = '%d';" %(dni)
                result = self.bd.run_query(query)
                if (len(result)==0):
                        return None
                else:
                        return result