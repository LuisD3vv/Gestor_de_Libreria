import time
from utils import creacion_isbn
from pathlib import Path
import sqlite3
from os import system,name
from datetime import datetime
from colorama import init, Fore,Back,Style

# INICIAR COLORAMA
init(autoreset=True)
#  No usar mkdir cuando la ruta termine en un archivo, de lo contrario daria un error.
#  Al utilizar Path se convierte en un objeto path
rutaGen = Path("sql/GestorGeneral.db")
ruta_escritura = Path("logs/log_libros.txt")


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


class Libro:
	"""
	Clase en la que definimos la estructura de cada libro
	De esta forma le decimos a python que es un libro y 
	como debe comportarse.
	"""
	def __init__(self, titulo, autor, fecha, isbn, genero, editorial):
		self.titulo = titulo
		self.autor = autor
		self.detalles = {
			"fecha": fecha,
			"isbn": isbn,
			"genero": genero,
			"editorial": editorial
		}
	def __str__(self):
		return f"Titulo: {self.titulo} | Autor: {self.autor} | Fecha: {self.detalles['fecha']} | ISBN: {self.detalles['isbn']} | Editorial: {self.detalles['editorial']}"


	def ingresar_libro_DB(self,ruta):
		"""
		Ingresar datos a la base de datos en lugar de a un texto
		"""
		try:
			with sqlite3.connect(ruta) as conn:
				cur = conn.cursor()
				cur.execute("CREATE TABLE IF NOT EXISTS Libro(titulo, autor, fecha, isbn, genero, editorial)")
				cur.execute(
					"Insert into Libro(Titulo, Autor, Fecha, Genero, Editorial,ISBN) values (?, ?, ?, ?, ?, ?)",
					(self.titulo, self.autor, self.detalles['fecha'], self.detalles['genero'],
					self.detalles['editorial'], self.detalles['isbn']))
				conn.commit()
		except sqlite3.Error as error:
			print(f"Ha ocurrido un error en alguna parte => {error}")
	
	# Property es para obtener los datos almacenados en la variable y regresarlo de manera oculta, tambien es una forma diferente de la habitual al getter.
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
	# Property nos ayuda convertir a fecha en una propiedad
	def fecha(self):
		return self.detalles["fecha"]

	@fecha.setter
	def fecha(self, fecha_nueva):
		try:
			datetime.strftime(fecha_nueva, "%d-%m-%Y") #  Hay diferentes formas para formatear el string de fecha
		except ValueError:
			print("Ingresa la fecha en el formato correcto [DD-MM-YYYY]")
		else:
			self.detalles["fecha"] = fecha_nueva

def agregar_libro(titulo, autor, fecha, genero,isbn, editorial):
	"""Comprobar las entradas del usuario y agregar correctamente el libro"""

	titulo_libro = titulo
	autor_libro = autor
	detalle = ({
		"fecha": fecha,
		"isbn": isbn,
		"genero": genero,
		"editorial": editorial
	})
	# verificar que todas las opciones sean correctas antes de crear el objeto
	objeto = Libro(titulo=titulo_libro, autor=autor_libro, **detalle)
	# el asterico en detalle, es un desempaquetado especial de diccionario clave, valor, si donde queremos sobreescribir los mismos datos, se nombraran como tal
	# es decir, se acoplaran solos a los elementos disponibles
	if isinstance(objeto, Libro): #  verificamos que el libro nuevo sea un objeto de la clase libro
		objeto.ingresar_libro_DB(rutaGen)  # si el objeto se creo, se ingresa a la database
		with open(ruta_escritura, "a") as lerbo:
			try:
				lerbo.writelines(f"Titulo {titulo}| Autor {autor} | Genero {genero} | Fecha {fecha}\n")
			except FileNotFoundError:
				print(f"No se encontro el archivo final de la ruta {objeto}")
			else:
				system("clear")
				print("El Libro fue exitosamente añadido.")
	return objeto

def mostrar_libros():
	try:
		with sqlite3.connect(rutaGen,timeout=30) as conn:
			cur = conn.cursor()
			cur.execute("SELECT Libro.Autor, Libro.Titulo,Libro.Genero FROM Libro") 
			base = cur.fetchall()
			system(validar_plataforma())
			print(Back.BLACK + Fore.RED + "Libros en el catalogo\n")
			for libro in base:
				(Autor,Titulo,Genero) = libro
				print(Fore.BLUE + "[ - Autor: "+  f"{Fore.GREEN + Autor.strip()}" + Fore.BLUE + " - Titulo: " + f"{Fore.GREEN + Titulo.strip()}" + Fore.BLUE + " - Genero: " + f"{Fore.GREEN +  Genero.strip()} ]\n")
			print(Fore.RED + "Antes de solicitar algun libro, verifique el estado de este en la seccion ver libros en prestamos\n")
	except sqlite3.Error as error:
		print("Ha ocurrido un error => ", error)

def buscar_libro(opcion,param):
	limpio = param.strip()
	try:
		with sqlite3.connect(rutaGen) as con:
			cur = con.cursor()
		if opcion == 1:
			#  no podemos sustituir columnas de sql con el ?, colamente nos queda usarlo en el where, para asi evitar inyeccion sql
			#  cada busqueda es independiete segun el parametro. por eso el multiple res
			cur.execute("SELECT * FROM Libro WHERE Autor like ?", (limpio,))
			res = cur.fetchone()
			if res:
				(_,Titulo,Autor,Fecha,Genero,_,_) = res
				system(validar_plataforma())
				print(f"Libros disponibles del Autor(a) {Autor}:\n")
				print(f"TItulo: {Titulo} | Autor: {Autor} | Fecha de Lanzamiento: {Fecha} | Genero: {Genero}")
				return "correcto"
		elif opcion == 2:
			cur.execute("SELECT * FROM Libro WHERE Titulo like ?", (limpio,))
			res = cur.fetchone()
			if res:
				(_,Titulo,Autor,Fecha,Genero,_,_) = res
				system("clear")
				print(f"Libros con el titulo {Titulo}:")
				print(f"TItulo: {Titulo} | Autor: {Autor} | Fecha de Lanzamiento: {Fecha} | Genero: {Genero}")
				return "correcto"
		elif opcion == 3:
			cur.execute("SELECT Titulo,Autor FROM Libro WHERE Genero like ?", (limpio,))
			res = cur.fetchall()
			if res:
				system("clear")
				print(f"Libros disponibles del genero '{limpio}':\n")
				for Genlibro in res:
					(tit, aut) = Genlibro
					print(f"Titulo: {tit} | Autor: {aut:<12}\n-------") # aqui se utiliza el especificador de ancho de cadena :<n :>n :^n (alinear izquierda, derecha y centrar respectivamente)
					
				return "correcto"
		elif opcion == 4:
			cur.execute("SELECT * FROM Libro WHERE ISBN like ?", (limpio,))
			res = cur.fetchone()
			if res:
				(_,Titulo,Autor,Fecha,Genero,_,isbn) = res
				system(validar_plataforma())
				print(f"Libro con el ISBN {limpio}:\n")
				print(f"TItulo: {Titulo} | Autor: {Autor} | Fecha de Lanzamiento: {Fecha} | Genero: {Genero} | ISBN: {isbn}")
				return "correcto"
		elif opcion == 5:
			cur.execute("SELECT * FROM Libro WHERE Libro_ID like ?", (limpio,))
			res = cur.fetchone()
			if res:
				(_,Titulo,Autor,Fecha,Genero,_,isbn) = res
				system(validar_plataforma())
				print(f"Libro con el ID {limpio}:\n")
				print(f"TItulo: {Titulo} | Autor: {Autor} | Fecha de Lanzamiento: {Fecha} | Genero: {Genero} | ISBN: {isbn}")
				return "correcto"
	except sqlite3.Error as e:
		print(f"Ha ocurrido un error => {e}")

