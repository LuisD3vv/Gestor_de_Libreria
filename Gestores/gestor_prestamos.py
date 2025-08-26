from datetime import datetime
import sqlite3


hoy = datetime.now()

ruta_db = "/home/lissandro/Escritorio/Gestor de Librerias/extra/GestorGeneral.db"

def validadar_metodo(*args):
	# Si esperas que el argumento sea 1, args llega como tupla, por eso se compara con args[0][1] etc
	#  Buscar usuario por ID
	try:
		with sqlite3.connect(ruta_db) as conn: # conectar con la base de datos
			if args[0] == 1:
				table_id = args[1]
				try:
					cur = conn.cursor() # utilizar los comandos
					cur.execute("SELECT nombre, apellido FROM Usuario WHERE User_id = ?", (table_id,)) # ejecutar una consulta
					user_actual = cur.fetchone()  # traer un solo resultado
					if user_actual:
						return "usuario existente"
					else:
						return "id inexistente"
				except sqlite3.Error as error:
					print('Hubo un error =>', error)
			elif args[0] == 2:
				nom = args[1].strip(" ")
				ape = args[2].strip(" ")
				try:
					cur = conn.cursor()
					# Para poder trabajar con algunos caracteres como los %% de sql, es necesario formatear el string con cadenas literales
					cur.execute("SELECT User_id, Nombre FROM Usuario WHERE (Nombre like ?) and (Apellido like ?)", (f"%{nom}%", f"%{ape}%"))
					user_actual = cur.fetchone()  # traer un solo resultado
					if user_actual:
						return "usuario existente"
				except sqlite3.Error as error:
					print('Hubo un error =>', error)
	except sqlite3.DatabaseError as e:
		print(f"Ha ocurrido un error => {e}")
		
	except ValueError:
		print("Asegurate de escribir bien la opcion")
	
	return None
		
	#  Buscar por nombre y apellido
	


def prestar_libro(libro,metodo):
	...
	


def devolver_libro():
	"""Funcion cambia el estado del libro"""


def ver_prestamos():
	"""
	Funcion que devuelve el estado de los
	libros, si estan disponibles para ser
	prestados o aun hay que esperar
	"""



