import sqlite3
from utils import generar_id
from pathlib import Path
import time
from os import system,name


ruta_usuario = Path("sql/GestorGeneral.db")
if ruta_usuario.exists():
    print(f"Ruta OK...")
    time.sleep(2)
    system("clear")
else:
    print("No existe la ruta")
rutalog = Path("logs/log_usuarios_id.txt")


def validar_plataforma():
	"""
	funcion para formatear el sistema de comandos de la funcion system
	para que funcione en windows o linux repectivamente
	"""
	sistema = []
	if name == "posix":
		print("Sistema Linux")
		sistema.append("clear")
	else:
		print("Sistema Windows")
		sistema.append("cls")
	return "".join(sistema)


class Usuario:
    """Clase para definir la estructura de cada usuario"""
    def __init__(self, nombre, apellido, edad, user_id):
        self.nombre = nombre
        self.apellido = apellido
        self.edad = edad
        self.user_id = user_id

    def __str__(self):
        print(f"{self.nombre}{self.apellido}{self.edad}{self.user_id}")

    def ingresar_usuario_DB(self):
        try:
            print("Cargando base de datos...")
            with sqlite3.connect(ruta_usuario, timeout=20,check_same_thread=False) as conn:
                cur = conn.cursor()
                cur.execute("CREATE TABLE IF NOT EXISTS Usuario(user_id,Nombre,Apellido,Edad)")
                cur.execute("INSERT INTO Usuario (user_id,Nombre,Apellido,Edad) VALUES (?,?,?,?)", (self.user_id, self.nombre, self.apellido, self.edad))
                with open (rutalog,"a") as log:
                    log.writelines(f"UserID {self.user_id} | UserName {self.nombre} | UserLastN {self.apellido} | UserAge {self.edad}")
                conn.commit()
        except sqlite3.Error as error:
            print(f"Ha ocurrido un error '{error}'")
        except sqlite3.SQLITE_LOCKED as L:
            print(f"La base de datos se protegio {L}")
# Declarar variables para poder colocar rangos de edad.
#  Getter
@property
def nombre(self):
    return self._nombre
# el setter no debe de regresar nada.
@nombre.setter
def nombre(self, nombre):
    if nombre == "":
        raise ValueError("Debes ingresar un nombre")
    else:
        self._nombre = nombre

@property
def apellido(self):
    return self._apellido

@apellido.setter
def apellido(self, apellido):
    if apellido == "":
        raise ValueError("Debes ingresar un apellido")
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

def ingresar_usuario(userid,nombre, apellido, edad):
    genericuser = Usuario(nombre, apellido, edad, userid)
    if isinstance(genericuser, Usuario):
        genericuser.ingresar_usuario_DB()
        print("Usuario creado con exito.")
        try:
            with open(ruta_usuario, "a") as user_log:
                user_log.writelines(f"Nombre: {nombre} | Apellido: {apellido} | Edad: {edad} | ID: {userid}\n")
        except FileNotFoundError:
            print("Asegurate de que la ruta o el archivo existan.")
    # Regresa una instancia de la clase Usuario
    return genericuser

def buscar_usuario():
    ...

def listar_usuarios():
    ...

#  Usar map() para mostrar títulos en mayúscula

#  Usar filter() para buscar por año
