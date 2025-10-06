# Funciones comunes
# - validar texto no vacío
# - funciones con map, filter, lambda
# - formatear strings
from random import *
from time import sleep
from os import name,system
import sqlite3
from pathlib import Path
from time import sleep
rutaGen = Path("sql/GestorGeneral.db")

"""
limpiar entradas, utilizar funciones lamba

aqui se crearan las funciones extras como generar los id
prefrabicar los isbn con 13 numeros separados por guiones, facil.
validar entradas nulas
y guardar logs
asi mismo formatear las impresiones

"""
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

def creacion_isbn():
	"""
		Creacion del isbn de un libro
		por su puesto es ficticio
	"""
	Ean = 978
	Country = randint(0, 998)
	Editorial = randint(0, 998)
	Publicacion_ID = randint(0, 998)
	DigitoControl = randint(0, 10)
	ISBN = str(Ean) + "-" + str(Country) + "-" + str(Editorial) + "-" + str(Publicacion_ID) + "-" + str(DigitoControl)
	return ISBN
def malas_palabras(palabra):
	groserias = [
		"verga", "culo", "puta", "perra",
		'pendejo', "pinche", "puto", "basura", "mierda", "vagina", "pene",
		"estupido", "cagada", "bastardo", "joto","escoria","vagabundo","mierdero","migajero"]
	if palabra in groserias:
		return True
	else:
		return False

def admon():
	tablas = ['Prestamo','Usuario','Libros'] # type: ignore
	print("Limpiando consola...")
	sleep(2)
	system(validar_plataforma())
	print("Bienvenido al menu de administrador, que desea realizar jefe?")
	print("1) Eliminar usuario \n2) vaciar tabla \n3) Eliminar un libro\n4) Salir")
	opcion = input(">> ")
	try:
		with sqlite3.connect(rutaGen) as conn:
			cur = conn.cursor()
			match opcion:		 # type: ignore
				case '1' :
					print("Seccion para eliminar usuario")
					print("Ingresa el nombre y apellido del usuario a eliminar: ")
					nombre = input("Nombre >> ").strip()
					apellido = input("Apellido >> ").strip()
					cur.execute("DELETE FROM Usuario WHERE (Nombre LIKE ?) AND (Apellido LIKE ? )",(f"%{nombre}%",f"%{apellido}%"))
					conn.commit()
					system(validar_plataforma())
					print(f"Se elimino correctamente el usuario {nombre} {apellido}")
					print("...")
					sleep(3)
					system(validar_plataforma())
				case '2':
					print("Esta seccion es para vaciar tabla")
					eliminar = input("Deseas continuar? ")
					if eliminar == 'si':
						print("Ingresa el nombre de la tabla")
						nombre_eliminar = input(">> ").strip()
						if nombre_eliminar in tablas:
							cur.execute(f"DELETE FROM {nombre_eliminar}")
							print(f"Se vacio la tabla {nombre_eliminar} correctamente.")
							print(f"DEBUG {nombre_eliminar}")
						else:
							print("Tabla no permitida")
				case '3':
					print("Eliminar un libro")
					print("Deseas eliminar el libro por su \n1) ID o \n2) Datos del libro")
					eleccion = input(">> ")
					match eleccion:
						case '1':
							print("ingresa el id del libro: ")
							idlib = input("Libro id>> ")
							cur.execute("DELETE FROM Libro WHERE Libro_ID = ?",(idlib,))
							print("El libro con el ID {} se ha borrado exitosamente ".format(idlib))
							
						case  '2':
							print("Ingresa los siguientes datos: ")
							auth = input("Nombre del autor: ")
							titl = input("Titulo del libro: ")
							cur.execute("DELETE FROM Libro WHERE (Autor LIKE ?) AND (Titulo LIKE ?)",(f"%{auth} %",f"%{titl}%"))
							print("El libro {} del autor {} se ha borrado exitosamente ".format(auth)(titl)) # type: ignore # 
							
						case '3':
							print("Ingresa el ISBN")
							...
						case _:
							print("Opcion incorrecta")
				case '4':
					system(validar_plataforma())
					print("Regresando a menu principal...")
					sleep(2)
					system(validar_plataforma())
					return 
				case _:
					print("ha ocurrido un error")
	except sqlite3.OperationalError as e:
		print(f"ocurrio un error de operacion {e}")
	except:
		print("error")
  
def gen_nombres_pruebas():
	usuarios = [
	"Alejandro", "Fernández",
	"Valeria", "Torres",
	"Miguel", "Gómez",
	"Isabel", "Díaz",
	"Roberto", "Ruiz",
	"Sofía", "Sánchez",
	"Javier", "García",
	"Laura", "Morales",
	"Daniel", "Navarro",
	"Elena", "Ortega",
	"Pablo", "Jiménez",
	"Gabriela", "Ramos",
	"Fernando", "Vargas",
	"Natalia", "Castro",
	"Ricardo", "Herrera",
	"Carolina", "Núñez",
	"Héctor", "Reyes",
	"Lucía", "Silva",
	"Emilio", "Mendoza",
	"Adriana", "Guerrero"
	]
	nomeale = choice(usuarios)
	return nomeale

def gen_apellidos_pruebas():
	apellidos = [
	"García", "Rodríguez", "González", "Fernández", "López",
	"Martínez", "Sánchez", "Pérez", "Gómez", "Martín",
	"Jiménez", "Ruiz", "Hernández", "Díaz", "Moreno",
	"Muñoz", "Álvarez", "Romero", "Alonso", "Gutiérrez",
	"Navarro", "Torres", "Domínguez", "Vázquez", "Ramos",
	"Gil", "Ramírez", "Serrano", "Blanco", "Molina",
	"Morales", "Suárez", "Ortega", "Delgado", "Castro"
	]
	apeale = choice(apellidos)
	return apeale

def generar_id_pruebas():
	nombre_clean = gen_nombres_pruebas() # type: ignore
	nom = list(choices(nombre_clean.strip(), k=5))
	n = randint(1, 99)
	n2 = randint(1, 99)
	Gen_ID = (f" {"".join(nom)}{n}{n2}")
	return str(Gen_ID)

def generar_id(name):
	"""Con esta funcion crearemos un id unico"""
	nombre_clean = gen_nombres_pruebas.strip() # type: ignore
	nom = list(choices(nombre_clean, k=5))
	n = randint(1, 999)
	Gen_ID = f"{"".join(nom)}{n}"
	return str(Gen_ID)

generar_id_pruebas()

