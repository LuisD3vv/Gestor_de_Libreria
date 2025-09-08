from datetime import datetime
import sqlite3
from pathlib import Path
from os import system

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
	print(libro_id)
	try:
		with sqlite3.connect(ruta_db) as con:
			cur = con.cursor()
			cur.execute("select prestado from Prestamo where Libro_id = ?",(libro_id,))
			estado = cur.fetchone()
			print("DEBUG estado:", estado, "->", type(estado)) # nos ayuda a saber que regresa una consulta
			if estado[0] == 1:
				return True
			elif estado == None:
				print("No hubo resultado en la busqueda")
	except TypeError as t:
		print(f"Error de nonetype, un error en la consulta {t}")
	except sqlite3.Error as e:
		print(f"Ha ocurrido un error {e}")
	return False

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
					raise ValueError("tipo de busqueda invalido")

			cur.execute(f"SELECT Libro_ID FROM Libro where {columna} = ? ", (libroLimpio,))
			lid = cur.fetchone()
			cur.execute("SELECT User_id FROM Usuario WHERE Nombre LIKE ? and Apellido LIKE ? ",(f"%{nombre}%", f"%{apellido}%"))
			usid = cur.fetchone()

			#  Esto  daria un error al igresar el id del libro
			#  sacando el valor de la tupla (nombre,)
			Libro_id = lid[0]
			Usuario_id = usid[0]
			if verificarEstadoPrestamo(Libro_id):
					print("Este libro ya esta prestado\nporfavor selecciona otro.")
			else:
				# utilizamos esto para extraer el valor, ya que al ser una tupla con un solo valor lleva una coma (5,)
				cur.execute("""
					CREATE TABLE IF NOT EXISTS Prestamo (
					Libro_ID INTEGER,
					Usuario_id INTEGER,
					FechaPrestamo TEXT,
					prestado BOOLEAN
				)
				""")
				cur.execute("CREATE IF NOT EXISTS INSERT INTO Prestamo (Libro_ID,Usuario_id,FechaPrestamo,prestado) VALUES (?,?,?,?)", (Libro_id, Usuario_id, hoy, True))
				con.commit()
				try:
					with open('logs/log_prestamos.txt') as log:
						log.writelines(f"Libro ID: {Libro_id}| User: {Usuario_id}| FechaP: {hoy}| Prestado: {1}\n")
						print("Prestamo guardado en log")
				except FileNotFoundError:
						print("Asegurate de que el archivo exista o la ruta este bien escrita")

				system("clear")
				print("El prestamo se realizo correctamente. tienes 3 meses.")
			
			print(f"Usuario o Libro no encontrados {Libro_id} {Usuario_id}")
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
