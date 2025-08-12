import time
from utils import creacion_isbn
from pathlib import Path
import sqlite3

# No usar mkdir cuando la ruta termine en un archivo.
#  Crear el archivo si no extiste
rutaFolder = Path("/home/lissandro/Python_Repox/Gestor de Libreria/Libros")
# es un directorio

def puta_ruta():
	try:
		if rutaFolder.exists():
			print("Ruta existente \U0001F54A.")
	except FileNotFoundError:
			print("Carpeta no encontrada")
			rutaFolder.mkdir(parents=True, exist_ok=True)
			# si alguna carpeta del camino no existe se crea con parents = true, y con exist, si el archhivo
			# ya existe no se lanza error
			time.sleep(2)
			print("Creando carpeta...")
			time.sleep(2)
			print("Carpeta creada con exito")
	archivo = rutaFolder / "Libros.txt"
	archivo.touch(exist_ok=True)
	return archivo
# Crear archivo




class Libro:
	prestado = False
	"""Clase en la que definimos la estructura de cada libro"""

	def __init__(self, titulo, autor, fecha, isbn, genero, editorial):
		self.titulo = titulo
		self.autor = autor
		self.detalles = {
			"fecha": fecha,
			"isbn": isbn,
			"genero": genero,
			"editorial": editorial
		}

	"""
	Crear opcion por si no existe la base de datos
	"""

	def __str__(self):
		return f"Titulo: {self.titulo} | Autor: {self.autor} | Fecha: {self.detalles['fecha']} | ISBN: {self.detalles['isbn']} | Editorial: {self.detalles['editorial']}"

	def ingresar_libro_DB(self):
		"""
		Ingresar datos a la base de datos en lugar de a un texto
		"""
		try:
			with sqlite3.connect("/home/lissandro/Python_Repox/Gestor de Libreria/Libros/Libros.db") as conn:
				cur = conn.cursor()
				cur.execute("CREATE TABLE IF NOT EXISTS DetalleLibro (titulo,autor,fecha,isbn,genero,editorial)")
				cur.execute(
					"Insert into DetalleLibro (titulo, autor, fecha, isbn, genero, editorial) values (?, ?, ?, ?, ?, ?)",
					(self.titulo, self.autor, self.detalles['fecha'], self.detalles['isbn'],
					 self.detalles['genero'], self.detalles['editorial']))
				conn.commit()
		except sqlite3.Error as error:
			print("Ha ocurrido un error en alguna parte", error)

	def buscar_libro(self):
		...

	#  Property es para obtener los datos almacenados en la variable y regresarlo de manera oculta, tambien es una forma diferente dela habitual al getter
	@property
	def titulo(self):
		return self._titulo

	@titulo.setter
	def titulo(self, titulo_nuevo):
		if len(titulo_nuevo) > 100:
			print("El texto es demaciado largo")
		else:
			self._titulo = titulo_nuevo

	@property
	def autor(self):
		return self._autor

	@autor.setter
	def autor(self, autor_nuevo):
		if not isinstance(autor_nuevo, str):
			print("Ingresa un nombre valido")
		else:
			self._autor = autor_nuevo

	@property
	# utilizar metodos como atributos, es decir, al momento de llamarlos no necesitaremos parentesis, solo un objeto.atributo
	def fecha(self):
		return self.detalles["fecha"]

	@fecha.setter
	def fecha(self, fecha_nuevo):
		try:
			sep = fecha_nuevo.split("-")
		except ValueError:
			print("Ingresa la fecha completa")
		else:
			anio, mes, dia = sep
			if int(anio) > 2999 or int(anio) < 0000:
				print(f"mamon, como vas a tener esa edad {anio}")
			elif int(mes) > 12 or int(mes) < 0:
				print(f"Ingresa un numero dentro del rango {mes}")
			elif int(dia) <= 0 or int(dia) > 31:
				print(f"dia fuera del rango {dia}")
			else:
				self.detalles["fecha"] = fecha_nuevo


def agregar_libro(titulo, autor, fecha, genero, editorial):
	"""Comprobar las entradas del usuario y agregar correctamente el libro"""

	titulo_libro = titulo
	autor_libro = autor
	gen_isb = creacion_isbn()
	detalle = ({
		"fecha": fecha,
		"isbn": gen_isb,
		"genero": genero,
		"editorial": editorial
	})
	# verificar que todas las opciones sean correctas antes de crear el objeto
	objeto = Libro(titulo=titulo_libro, autor=autor_libro, **detalle)
	# el asterico en detalle, es un desempaquetado especial de diccionario clave, valor, si donde queremos sobreescribir los mismos datos, se nombraran como tal
	# es decir, se acoplaran solos a los elementos disponibles
	libro_actual = Path("/home/lissandro/Python_Repox/Gestor de Libreria/Libros/Libros.txt")
	if isinstance(objeto, Libro):
		objeto.ingresar_libro_DB() # si el objeto se creo, se ingresa a la database
		with open(libro_actual, "a") as lerbo:
			try:
				lerbo.writelines(str(objeto) + "\n")
			except FileNotFoundError:
				print(f"No se encontro el archivo final de la ruta {libro_actual}")
			else:
				print("EL libro se anadio exitosamente")
	return objeto

# libro_nuevo = agregar_libro()
# print("Libro nuevo creado")
#
# todos_los_libros = []
# todos_los_libros.append(libro_nuevo)
