import MySQLdb
import Controladores.Credenciales as c

class clsConexion: 
        def __init__(self, DB_HOST=c.host, DB_USER=c.user, DB_PASS=c.passw, DB_NAME=c.db):   
                self.datos = [DB_HOST, DB_USER, DB_PASS, DB_NAME]
                self.conn = MySQLdb.connect(*self.datos)
                self.conn.autocommit(True)
                MySQLdb.connect(*self.datos)
                self.cursor = self.conn.cursor()

        def run_query(self,query=''):
                self.cursor.execute(query)
                if query.upper().startswith('SELECT'):
                        data = self.cursor.fetchall()
                
                else:
                        self.conn.commit()
                        data=None
                return data

        def close(self):
                self.cursor.close()
                self.conn.close()
