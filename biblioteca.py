# Module Imports
from typing import Collection
import mariadb
import smtplib
import sys
import getpass
import csv
from email.mime.text import MIMEText
import random
import string


def validacionUsuario():
    perfil=0
    intentos=0
    while(intentos < 5):
        #se pide un usuario y contraseña para entrar en la aplicacion
        userid = input("Escribe tu UserID: ")
        contra = getpass.getpass('Password: ')     
        #la funcion password del sql de mariadb encripta una cadena para que no se almacenen en claro las contraseñas
        sql="SELECT rol,nombre FROM usuarios WHERE userid='" + userid + "' AND  PASSWORD('"+ contra + "')=contraseña ;"
        # se ejecuta la accion en la base de datos   
        cur.execute(sql)
        # print(f"{cur.rowcount}")    
        if cur.rowcount == 0:
            rol = -1
            intentos += 1
            print(f"UserId/Pass erroneo. #intentos: {intentos}/5" )
            if intentos == 5:
                sys.exit("Numero de intentos superados - EXIT") 
        else:   
            (rol,nombre)=cur.fetchone()
            print("\n")         
            return (rol,nombre)

def autorizacionUsuario(tipo,modulo):
    sql="select " + modulo +" from roles where idRol="+ str(tipo) +";"
    # print(f"{sql}")
    cur.execute(sql)    
    (autorizado,)=cur.fetchone()
    # print(f"autorizado : {autorizado}")
    return autorizado

def pedirNumero():
    correcto=False
    num=0
    while(not correcto):
        try:
            num = int(input("Elige una opción: "))
            correcto=True
        except ValueError:
            print('Error, introduce un numero entero')
    return num

def agregarLibro(tipo):
    autorizado = autorizacionUsuario(tipo,'agregarLibro')
    if autorizado=='S':     
        # se pide el nombre del libro que se va añadir y se guarda en una variable
        libroAgregar = input("Nombre un libro: ")
        fechaEstandar="0000-00-00"
        #insert information 
        try: 
            libroAgregar = "INSERT INTO libros (nombreLibro,prestado,fecha) VALUES ('"+ libroAgregar + "',0,'"+fechaEstandar+"');"
            cur.execute(libroAgregar) 
        except mariadb.Error as e: 
            print(f"Error: {e}")
        conn.commit() 
    else:
        print('\nRol no autorizado\n')
        
def buscarLibro(tipo):
    autorizado = autorizacionUsuario(tipo,'buscarLibro')
    if autorizado=='S': 
        libroDeseado=input("Libro a buscar: ")
        # buscar informacion
        sql="select libros.nombreLibro, usuarios.nombre, libros.fecha from libros inner join usuarios on libros.prestado=usuarios.id WHERE libros.nombreLibro='"+libroDeseado+ "'"
        cur.execute(sql)
        for (nombreLibro,nombre,fecha) in cur:
            print(f"{nombreLibro},{nombre},{fecha}")
    else:
        print('\nRol no autorizado\n')
        
def eliminarLibro(tipo):
    autorizado = autorizacionUsuario(tipo,'eliminarLibro')
    if autorizado=='S':    
        libroBuscado=input("Libro a eliminar: ")
        # eliminar informacion
        sql="delete from libros where nombreLibro='"+libroBuscado+"'"
        #print(sql)
        cur.execute(sql)
        conn.commit()
    else:
        print('\nRol no autorizado\n')
        
def añadirCliente(tipo): 
    autorizado = autorizacionUsuario(tipo,'añadirCliente')
    if autorizado=='S':
        usuarioAgregar = input("Nombre nuevo cliente: ")
        correoCliente = input("Correo del cliente: ")
        #insert information 
        usuarioAgregar="INSERT INTO biblioteca.usuarios (nombre,rol,correo) VALUES ('"+ usuarioAgregar + "',3,'"+ correoCliente + "');"
        #print(usuarioAgregar)
        try: 
            #cur.execute("INSERT INTO biblioteca.usuarios (nombre) VALUES (?)", (usuarioAgregar))
            cur.execute(usuarioAgregar)
            print(f"{cur.rowcount} details inserted")
            conn.commit()
        except mariadb.Error as e: 
            print(f"Error: {e}")
    else:
        print('\nRol no autorizado\n')
        
def buscarUsuario(tipo):
    autorizado = autorizacionUsuario(tipo,'buscarUsuario')
    if autorizado=='S':
        usuarioDeseado=input("Usuario a buscar: ")
        # buscar informacion
        sql="SELECT usuarios.nombre, roles.nombreRol, usuarios.correo FROM usuarios INNER JOIN roles ON usuarios.rol=roles.idRol WHERE usuarios.nombre='"+usuarioDeseado+"'"
        cur.execute(sql)
        #print(sql)
        for (nombre,rol,correo) in cur:
            print(f"{nombre},{rol},{correo}")
    else:
        print('\nRol no autorizado\n')

def añadirBibliotecario(tipo):

    autorizado = autorizacionUsuario(tipo,'añadirBibliotecario')
    if autorizado=='S':
        nuevoUsuario = input("Nombre nuevo bibliotecario: ")
        correoBiblioteca = input("Correo del bibliotecario: ")
        rP=string.ascii_lowercase
        length = 5
        temp=random.sample(rP,length)
        randomPassword="".join(temp)
        print("tu contraseña es: "+randomPassword)
        #insert information 
        usuarioAgregar="INSERT INTO biblioteca.usuarios (nombre,rol,correo,userID) VALUES ('"+ nuevoUsuario + "',2,'"+ correoBiblioteca + "','"+correoBiblioteca+"');"
        #se usa el mail para el user y contraseña se crea automaticamente
        contraseñaNueva="update usuarios set contraseña=(password('"+randomPassword+"')) where nombre='"+nuevoUsuario+"';"
        
        try: 
            # print(contraseñaNueva)
            cur.execute(usuarioAgregar)
            cur.execute(contraseñaNueva)
            print(f"{cur.rowcount} details inserted")
            conn.commit()
        except mariadb.Error as e: 
            print(f"Error: {e}")
    else:
        print('\nRol no autorizado\n')

def despedirBibliotecario(tipo):
    autorizado = autorizacionUsuario(tipo,'despedirBibliotecario')
    if autorizado=='S':    
        bibliotecario=input("Persona que va a ser despedida: ")
        # eliminar informacion
        sql="delete from usuarios where nombre='"+bibliotecario+"'"
        #print(sql)
        cur.execute(sql)
        conn.commit()
    else:
        print('\nRol no autorizado\n')

def prestarLibro(tipo):
    autorizado = autorizacionUsuario(tipo,'prestarLibro')
    if autorizado=='S':
        libroDeseado=input("Libro prestado: ")
        from datetime import date
        today=date.today()
        usuarioDeseado=input("Cliente que se lleva el libro: ")
        # buscar informacion       
        sql="select id from usuarios where nombre='" + usuarioDeseado + "'"
        cur.execute(sql)
        (idCliente,)=cur.fetchone()
        #cambiar informacion
        sql="UPDATE libros SET prestado="+str(idCliente)+", fecha='"+str(today)+"' WHERE nombreLibro='"+libroDeseado+"'"
        #print(sql)
        cur.execute(sql)
        conn.commit()     
    else:
        print('\nRol no autorizado\n')
        
def devolucionLibro(tipo):
    autorizado = autorizacionUsuario(tipo,'devolucionLibro')
    if autorizado=='S':
        fechaEstandar="0000-00-00" 
        libroDevuelto=input("Libro devuelto: ")
        #cambiar informacion
        sql="UPDATE libros SET prestado=0, fecha='"+fechaEstandar+"' WHERE nombreLibro='"+libroDevuelto+"'"
        #print(sql)
        cur.execute(sql)
        conn.commit()   
    else:
        print('\nRol no autorizado\n')    

def enviarEmail(tipo):
    autorizado = autorizacionUsuario(tipo,'enviarEmail')
    if autorizado=='S':
        usuarioDeseado=input("Usuario al que se le desea enviar el correo: ")
        # buscar informacion 
        sql="select correo from usuarios where nombre='" + usuarioDeseado + "'"
        cur.execute(sql)
        # guardar informacion en una variable para su uso posterior
        (correoUsado,)=cur.fetchone()
        #print(sql)
        print("Se ha enviado el correo a: "+correoUsado)
        gmail_user = 'uemcorreobiblioteca@gmail.com'
        gmail_password = 'Enviarcorreopython'
        sent_from = gmail_user
        to = correoUsado
        # subject = 'UEM correo proyecto Bibioteca'
        # body = "Hola \nESte correo se envia para que devuelva el libro\n\n"
        # email_text = """From: %s
        # To: %s
        # MIME-version: 1.0
        # content-type: text/html
        # Subject: %s
        # %s
        # """ % (sent_from, ", ".join(to), subject, body)
        #mensaje el cual se va a enviar en el correo, es un mensaje fijo
        msg = MIMEText('Hola,\nEste es un mensaje automatico de la biblioteca UEM\n Por favor devuelva el libro\n')

        msg['Subject'] = 'Mensaje de biblioteca UEM'
        msg['From'] = gmail_user
        msg['To'] = to
        try:
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.ehlo()
            server.login(gmail_user, gmail_password)
            # server.sendmail(sent_from, to, email_text)
            server.sendmail(sent_from, to, msg.as_string())
            server.close()
            print("Email sent!") 
        except:
            print('Something went wrong...')
    else:
        print('\nRol no autorizado\n')

def ficheroCSV(tipo):
    autorizado = autorizacionUsuario(tipo,'ficheroCSV')
    if autorizado=='S':
        f = open("registroLibros.csv", "w")
        f.write("Nombre,Cliente,Fecha\n")
        listaLibros="SELECT libros.nombreLibro, usuarios.nombre, libros.fecha FROM libros INNER JOIN usuarios ON libros.prestado=usuarios.id"
        cur.execute(listaLibros) 
        for (nombreLibro,prestado,fecha) in cur:
            infoCSV=(f"{nombreLibro},{prestado},{fecha}\n")
            # print(infoCSV)
            f.write(infoCSV)
        f.close()
    else:
        print('\nRol no autorizado\n')       

#Aqui empieza el programa principal
if __name__ == '__main__': 

    #se fijan variables para estar permanente en el menú de inicio     
    salir = False
    opcion = -1
    # El siguiente bloque es para establecer la conexión con la base de datos (bd)
    try:
        conn = mariadb.connect(user="root",password="fundacion",host="localhost",port=3306,database="biblioteca")
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)
    cur = conn.cursor(buffered=True)
    
    #La funcion validacionUsuario pide login y contraseña y la valida contra 
    #el password encriptado almacenado en la bd y si coinciden devuelve el rol
    (rol,nombre) = validacionUsuario()
    # print(f"El rol del usuario es: {rol}")
    #bloque de presentación del menú
    while not salir: 
        print(f"=================\nBIENVENIDO {nombre}\n=================")
        print ("1. Agregar Libro")
        print ("2. Buscar Libro")
        print ("3. Eliminar Libro")
        print ("4. Añadir Cliente")
        print ("5. Buscar Usuario")
        print ("6. Contratar bibliotecario")
        print ("7. Despedir bibliotecario")
        print ("8. Prestar Libros") 
        print ("9. Devolucion Libros") 
        print ("10. Enviar correo") 
        print ("11. Ficheros de libros") 
        print ("0. Salir")
        print ("\n")
        opcion = pedirNumero()
        #bloque de selección de funcion con base en selección de usuairo
        if opcion == 1:
            print ("====================\nAgregar Libro\n====================")
            agregarLibro(rol)
        elif opcion == 2:
            print ("====================\nBuscar Libro\n====================")
            buscarLibro(rol)
        elif opcion == 3:
            print("====================\nEliminar Libro\n====================")
            eliminarLibro(rol)
        elif opcion == 4:
            print("====================\nAñadir Cliente\n====================")
            añadirCliente(rol)
        elif opcion == 5:
            print("====================\nBuscar Usuario\n====================")
            buscarUsuario(rol)
        elif opcion == 6:
            print("====================\nAñadir Bibliotecario\n====================")
            # (rol,nombre) = validacionUsuario(), cambio de usuario, cerrar sesion      
            añadirBibliotecario(rol)
        elif opcion == 7:
            print("====================\nDespedir Bibliotecario\n====================")
            despedirBibliotecario(rol)
        elif opcion == 8:
            print("====================\nPrestar Libros\n====================")           
            prestarLibro(rol)   
        elif opcion == 9:
            print("====================\nDevolucion Libros\n====================")
            devolucionLibro(rol)
        elif opcion == 10:
            print("====================\nEnviar correo\n====================")
            enviarEmail(rol)
        elif opcion == 11:
            print("====================\nFichero libros\n====================")
            ficheroCSV(rol)
        elif opcion == 0:
            salir = True
        else:
            print ("Introduce un numero entre 1 y 8")
    #bloque de finalización del programa, aquí se cierran conexiones
    conn.close
    print("fin de programa")

    