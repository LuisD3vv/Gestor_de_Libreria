import sqlite3
from utils import generar_id
from pathlib import Path

ruta_usuario = Path("/home/lissandro/Python_Repox/Gestor de Libreria/Usuarios/log_usuarios_id.txt")
if ruta_usuario.exists():
    print("La ruta si existe")
else:
    print("No existe la ruta")
class Usuario:
    """Clase para definir la estructura de cada usuario"""
    def __init__(self, nombre, apellido, edad, user_id):
        self.nombre = nombre
        self.apellido = apellido
        self.edad = edad
        self.user_id = user_id

    def mostrar_info_usuario(self):
        ...

    #  def __del__(self, nombre_eliminar):

    def conocer_id(self, nombre_user, apellido_user):
        ...

    def ingresar_usuario_DB(self):
       """
        Funcion para manejar el ingreso de usuarios a una base de datos
        utilizando el with para no tener que cerrar manualment
        que eso normalmente cuausa errores si la apertura no
        funciona
       """
       try:
         with sqlite3.connect("/home/lissandro/Python_Repox/Gestor de Libreria/Usuarios/Usuarios.db") as conn:
            cur = conn.cursor()
            cur.execute("CREATE TABLE IF NOT EXISTS Usuariodb(nombre,apellido,edad,user_id)")
            cur.execute("INSERT INTO Usuariodb(nombre,apellido,edad,user_id) VALUES (?,?,?,?)", (self.nombre, self.apellido, self.edad, self.user_id))
            conn.commit()
       except sqlite3.Error as error:
            print("Ha ocurrido un error =>", error)
# Declarar variables para poder colocar rangos de edad.
#  Getter
@property
def nombre(self):
    return self._nombre
# el setter no debe de regresar nada.
@nombre.setter
def nombre(self, nombre):
    if nombre == "":
        raise ValueError("debes ingresar un nombre")
    else:
        self._nombre = nombre

@property
def apellido(self):
    return self._apellido

@apellido.setter
def apellido(self, apellido):
    if apellido == "":
        raise ValueError("debes ingresar un apellido")
    else:
        self._apellido = apellido

@property
def edad(self):
    return self._edad

@edad.setter
def edad(self, edad):
    if edad <= 0:
        raise ValueError("La edad debe ser mayor a 0")
    else:
            self._edad = edad


def ingresar_usuario(nombre, apellido, edad):
    userid = generar_id()
    genericuser = Usuario(nombre, apellido, edad, userid)
    if isinstance(genericuser, Usuario):
        genericuser.ingresar_usuario_DB()
        print("Usuario creado con exito")
        try:
            with open(ruta_usuario, "a") as user_log:
                user_log.writelines(f"Nombre: {nombre} | Apellido: {apellido} | Edad: {edad} | ID: {userid}\n")
        except FileNotFoundError:
            print("Asegurate de que la ruta o el archivo existan.")

def buscar_usuario():
    ...


def listar_usuarios():
    ...

#  Usar map() para mostrar títulos en mayúscula

#  Usar filter() para buscar por año
