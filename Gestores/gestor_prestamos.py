from datetime import datetime
import sqlite3
from pathlib import Path
from os import system
from time import sleep

hoy = datetime.now().strftime("%d-%m-%Y")

ruta_db = Path("sql/GestorGeneral.db")

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
					cur.execute("SELECT User_id, Nombre FROM Usuario WHERE Nombre like ? and Apellido like ?", (f"%{nom}%", f"%{ape}%"))
					user_actual = cur.fetchone()  # traer un solo resultado
					if user_actual:
						return "usuario existente"
				except sqlite3.Error as error:
					print('Hubo un error =>', error)
	except sqlite3.DatabaseError as e:
		print(f" Ha ocurrido un error => {e}")
		
	except ValueError:
		print("Asegurate de escribir bien la opcion")
	return None

def verificarEstadoPrestamo(libro_id):
	try:
		with sqlite3.connect(ruta_db) as con:
			cur = con.cursor()
			cur.execute("SELECT prestado FROM Prestamo WHERE Libro_id = ?",(libro_id,))
			estado = cur.fetchone()
			print("DEBUG estado:", estado, "->", type(estado)) # nos ayuda a saber que regresa una consulta
			if estado == None:
				print("no hubo ningun resultado")
				return False
			else:
				#  compresion de logica de true y false
				estadoLimpio = estado[0]
				return estadoLimpio == 1
	except sqlite3.Error as e:
		print(f"Ha ocurrido un error {e}")
	

def prestar_libro(busqueda,libro,*args):
	"""
	Funcion que recibe el libro y los datos del usuario para realizar el prestamo del libro solicitado
	"""
	tipo = busqueda
	libroLimpio = libro.strip(" ")
	(nombre, apellido) = args
	"""
	Esta funcion recibe la solicitud ya depues de las verificaciones
    anteriores.
    """
	re = ' '
	try:
		with sqlite3.connect(ruta_db) as con:
			cur = con.cursor()
			#  recuperar id del libro mediante el titulo del libro
			"""Con este case nos evitamos crear codigo inceseario
			para las opciones, asi segun el parametro solamente
			cambiamos el valor de columna y asi"""
			match tipo:
				case 1:
					columna = "Autor"
				case 2:
					columna = "Titulo"
				case 3:
					columna = "Genero"
				case 4:
					columna = "ISBN"
				case _:
					raise ValueError("Tipo de busqueda invalido")

			cur.execute(f"SELECT Libro_ID FROM Libro where Libro.{columna} LIKE ? ", (libroLimpio,))
			lid = cur.fetchone()
			cur.execute("SELECT User_id FROM Usuario WHERE Nombre LIKE ? and Apellido LIKE ? ",(f"%{nombre}%", f"%{apellido}%"))
			usid = cur.fetchone()
			print("DEBUG Libro_ID:", lid, "->", type(lid)) # nos ayuda a saber que regresa una consulta
			print("DEBUG User_ID:", usid, "->", type(usid)) # nos ayuda a saber que regresa una consulta

			# Limpiamos la tupla que nos regreso la consulta (n,)
			libroid = lid[0]
			userid = usid[0]

			
			print(f"Datos limpios => {libroid}, {userid}")
			sleep(2)
			system("clear")

			while True:
				if verificarEstadoPrestamo(libroid):
					print("El Libro seleccionado se encuentra en prestamo en este momento.\n¿deseas solicitar algun otro?")
					break
				else:
					#  Creamos la tabla en caso de no existir, lo cual puede suceder pero lo optimo seria que existiera para mantener congruencia con los prestamos
					print("Realizando prestamo...")
					sleep(2)
					system("clear")
					cur.execute("""
					CREATE TABLE IF NOT EXISTS Prestamo (
					Libro_ID INTEGER,
					Usuario_id INTEGER,
					FechaPrestamo TEXT,
					prestado BOOLEAN)""")
					cur.execute("CREATE IF NOT EXISTS INSERT INTO Prestamo (Libro_ID,Usuario_id,FechaPrestamo,prestado) VALUES (?,?,?,?)", (libroid, userid, hoy, True))
					con.commit()
					print("El prestamo se realizo correctamente. tienes 3 meses.")
					try:
						with open('logs/log_prestamos.txt') as log:
							log.writelines(f"Libro ID: {libroid}| User: {userid} id | FechaP: {hoy}| Prestado: {1}\n")
						print("Prestamo guardado en log")
					except FileNotFoundError:
						print("Asegurate de que el archivo exista o la ruta es te bien escrita")
					else:
						system("clear")
						print(f"Usuario o Libro no encontrados {lid} {usid}")                                                                             
	except sqlite3.Error as e:
		print("hay un puto pinche error {}".format(e))
	except ValueError as f:
		print("hay un error {}".format(f))
	
def devolver_libro():
	"""Funcion cambia el estado del libro"""
def ver_prestamos():
	"""
	Funcion que devuelve el estado de los
	libros, si estan disponibles para ser
	prestados o aun hay que esperar
	"""
