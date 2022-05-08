import Controladores.clsConexion as Conexion
import datetime

class clsC_Usuarios():
    def __init__(self):
        self.bdControl=Conexion.clsConexion()

    def getTabla(self):
        query=f"SELECT * FROM `usuario`"
        result = self.bdControl.run_query(query)
        if (len(result)==0):
            return None
        else:
            return result

    def getTablaSP(self):
        query=f"SELECT "\
            +"`idUser`,`dni`,`nombre`,`apellido`,`fchNac`,`direccion`,`mail`,`numTel`,`fchAlta`,`fchBaja`,`user`, tipocuenta.descripcion "\
            +"FROM "\
                +"`usuario` "\
            +"INNER JOIN tipocuenta ON usuario.idTCta=tipocuenta.idTCta;"
        result = self.bdControl.run_query(query)
        if (len(result)==0):
            return None
        else:
            return result
    
    def getTabla(self,ids):
        """ Hernan
        Consulta que recibe como parametro un array de IDs de Tipo de cuenta y devuelve los registros de usuarios que correponden a esos tipos"""
        query=f"SELECT "\
                +"`idUser`,`dni`,`nombre`,`apellido`,`fchNac`,`direccion`,`mail`,`numTel`,`fchAlta`,`fchBaja`,`user`, tipocuenta.descripcion "\
            +"FROM `usuario` "\
            +"INNER JOIN tipocuenta ON usuario.idTCta=tipocuenta.idTCta "\
            +"WHERE tipocuenta.idTCta=9999"
        if len(ids) >0:
            for i in range(len(ids)):
                query = query +f" OR tipocuenta.idTCta = {ids[i]}"
        query = query+";"

        result = self.bdControl.run_query(query)
        if (len(result)==0):
            return None
        else:
            return result


    def getDatos(self,idUs):
        query=f"SELECT * FROM `usuario` WHERE usuario.idUser='{idUs}'"
        result = self.bdControl.run_query(query)
        if (len(result)==0):
            return None
        else:
            return result

    def getCta(self,us):
        query=f"SELECT usuario.user, usuario.password, usuario.fchHora, usuario.fchBaja FROM `usuario` WHERE usuario.user='{us}'"
        result = self.bdControl.run_query(query)
        if (len(result)==0):
            return None
        else:
            return result


    #   %s=String o Num Real       %d=Num Entero
    def insert(self, data):
        #     [ 0   1   2     3    4    5   6     7     8    9     10  ]
        #data=[dni,nom,ape,fchNac,dir,mail,tel,fchAlta,user,pass,idTcta]
        query = "INSERT INTO usuario (dni,nombre,apellido,fchNac,direccion,mail,numTel,fchAlta,user,password,idTCta) VALUES ('%d','%s','%s','%s','%s','%s','%s','%s','%s','%s','%d');"%(data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8],data[9],data[10])
        self.bdControl.run_query(query)


    def setPass(self,password,idUser,fchHora=None):
        if fchHora!=None:
            query = f"UPDATE usuario SET usuario.password='{password}', usuario.fchHora='{fchHora}'  WHERE usuario.idUser={idUser}"
        else:
            query = f"UPDATE usuario SET usuario.password='{password}', usuario.fchHora=NULL  WHERE usuario.idUser={idUser}"
        self.bdControl.run_query(query)


    def setData(self, idUser,lista):
        #      [  0     1     2    3    4      5       6  ]
        #lista=["dni","nom","ape",fch,"dom","correo","tel"]
        campos=""
        if lista[0]!="":
            if campos!="":
                campos=campos+","
            campos=campos+f"usuario.dni='{lista[0]}'"
        if lista[1]!="":
            if campos!="":
                campos=campos+","
            campos=campos+f"usuario.nombre='{lista[1]}'"
        if lista[2]!="":
            if campos!="":
                campos=campos+","
            campos=campos+f"usuario.apellido='{lista[2]}'"
        if lista[3]!="":
            if campos!="":
                campos=campos+","
            campos=campos+f"usuario.fchNac='{lista[3]}'"
        if lista[4]!="":
            if campos!="":
                campos=campos+","
            campos=campos+f"usuario.direccion='{lista[4]}'"
        if lista[5]!="":
            if campos!="":
                campos=campos+","
            campos=campos+f"usuario.mail='{lista[5]}'"
        if lista[6]!="":
            if campos!="":
                campos=campos+","
            campos=campos+f"usuario.numTel='{lista[6]}'"
        
        query = f"UPDATE usuario SET {campos}  WHERE usuario.idUser={idUser}"
        self.bdControl.run_query(query)


    def inhabilitarUser(self,idUs,fch):
        query = f"UPDATE usuario SET usuario.fchBaja='{fch}' WHERE usuario.idUser={idUs}"
        self.bdControl.run_query(query)
        


    def buscaCta(self,us):
        query=f"SELECT usuario.user,usuario.password FROM `usuario` WHERE usuario.user='{us}'"
        result = self.bdControl.run_query(query)
        if (len(result)==0):
            return None
        else:
            return result


    def getTiposCta(self):
        query=f"SELECT * FROM `tipocuenta`"
        result = self.bdControl.run_query(query)
        if (len(result)==0):
            return None
        else:
            return result

    def getId(self,user):
        query=f"SELECT usuario.idUser FROM `usuario` WHERE usuario.user='{user}'"
        result = self.bdControl.run_query(query)
        if (len(result)==0):
            return None
        else:
            return result
