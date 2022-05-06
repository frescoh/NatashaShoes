import smtplib
import email.message


class clsSendMail:
    def __init__(self,password,nombre,correo,user=None,flag=None):
        self.flag=flag
        if user==None:
            email_content = """
            <html lang="es">
            <head>
            <meta http-equiv="Content-Type" content="text/html; charset="UTF-8"">
            
            <title>Notificacion</title>
            <style type="text/css">
                body{
                    font-size: 17px;
                }
                .pass{
                    font-size: 20px;
                    font-weight: bold;
                }
                .container{
                    text-align: center;
                }
                h1{
                    text-align: left;
                    padding-left: 5%;
                }
            </style>
            </head>
            """
            if self.flag==None:
                email_content= email_content+f"""
                    <body>
                        <h1>Hola {nombre}</h1>
                        <div class="container">
                            
                            <p>Su nueva clave es:</p> 
                            <p class="pass">{password}</p>
                            <p>Tiene 1 hora para poder ingresar con esta clave y cambiarla, de lo contrario debera pedir a un administrador que vuelva a reestablecerla.<br>
                            Si no ha sido usted la persona que ha pedido un reestablecimiento de clave, comuniquese con un administrador lo antes posible.
                            </p>
                        
                        </div>
                        
                    </body>
                    </html>
                    """
            else:
                email_content= email_content+f"""
                    <body>
                        <h1>Hola {nombre}</h1>
                        <div class="container">
                            
                            <p>Su nueva clave es:</p> 
                            <p class="pass">{password}</p>
                            <p>Este mail es solo para notificarle el cambio de clave.
                            <br>
                            Si ha sido usted quien ha realizado este cambio puede descartar este mail, de lo contrario comuniquese con un administrador lo antes posible.
                            </p>
                        
                        </div>
                        
                    </body>
                    </html>
                    """

                    
            msg = email.message.Message()
            msg['Subject'] = 'Cambio de clave'
        else:
            email_content = """
            <html lang="es">
            <head>
            <meta http-equiv="Content-Type" content="text/html; charset="UTF-8"">
            
            <title>Notificacion</title>
            <style type="text/css">
                .body{
                    font-size: 17px;
                }
                .pass, .user{
                    font-size: 17px;
                    font-weight: bold;
                }
                .container{
                    text-align: center;
                }
                h1{
                    text-align: left;
                    padding-left: 5%;
                }
            </style>
            </head>
            """+f"""

            <body>
                <h1>Bienvenido/a {nombre}</h1>
                <div class="container">
                    
                    <p>Tus datos han sido registrados correctamente en nuestro sistema.</p> 
                    <p>Ya puedes ingresar con tu cuenta.</p>
                    <div class="data">
                        <p>Usuario: <span class="user">{user}</p>
                        <p>Clave: <span class="pass">{password}</p>
                    </div> 
                
                </div>
                            
            </body>
            </html>



            """
            msg = email.message.Message()
            msg['Subject'] = 'Registro de cuenta'
    
        

        


        msg['From'] = Credencial.mail
        msg['To'] = correo
        password = Credencial.passMail
        msg.add_header('Content-Type', 'text/html')
        msg.set_payload(email_content)

        s = smtplib.SMTP('smtp.gmail.com: 587')
        s.starttls()

        # Login Credentials for sending the mail
        s.login(msg['From'], password)

        s.sendmail(msg['From'], [msg['To']], msg.as_string())
        s.quit()
