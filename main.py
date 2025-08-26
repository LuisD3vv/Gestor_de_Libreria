from os import system
import time
from Gestores.gestor_libros import agregar_libro as agl,mostrar_libros,buscar_libro as bl  # asi agregamos una funcion especifica
from Gestores.gestor_usuarios import ingresar_usuario as inguser
from Gestores.gestor_prestamos import prestar_libro, validadar_metodo
from utils import generar_id
from utils import malas_palabras
from datetime import date

"""
Es mucho mejor utilizar rutas absolutas, MUCHISMO, asi que a la hora de hacerlo portable
esto se debe a desde donde se ejecuta el programa, no se ejecuta donde esta
por ejemplo desde aqui no daria error porque es el principal y desde donde se ejecuta
pero si utilizara rutas relativas desde otro lugar, daria error porque lo buscaria desde donde
esta este archivo
"""

fecha = date.today()
fecha_hoy = fecha.strftime("%d-%m-%Y")
(dia_hoy, mes_hoy, anio_hoy) = fecha_hoy.split("-")


#  print(dia_hoy,mes_hoy,anio_hoy)
def validar_titulo(titulo):
	if malas_palabras(titulo):
		print('Hay palabras mal sonantes')
		return "Titulo del libro con groserias"
	if len(titulo) < 4:
		return "Titulo muy corto"
	else:
		return "correcto"


def validar_autor(autor):
	if malas_palabras(autor):
		print('Hay palabras mal sonantes')
		return "Nombre del autor con groserias"
	if len(autor) < 4:
		return "Nombre del autor muy corto"
	return "correcto"


def validar_genero(genero):
	if malas_palabras(genero):
		print('Hay palabras mal sonantes')
		return "Genero con groserias"
	if len(genero) < 4:
		return "Texto genero demaciado corto"
	return "correcto"


def validar_editorial(editorial):
	if malas_palabras(editorial):
		print('Hay palabras mal sonantes')
		return "Editorial con groserias"
	elif len(editorial) < 4:
		return "Editorial muy corta"
	return "correcto"


def validar_fecha(fecha):
	"""Validacion de fecha
	Arereglar comparacion de fechas
	y que solo aplique cuando el anio
	total es mayor al de hoy,
	individuamente si pueden ser mayores al dia de hoy
	"""
	while True:
		try:
			fecha_usuario = fecha.split("-")
			(dia, mes, anio) = fecha_usuario
			if int(anio) > int(anio_hoy):
				print("El año no puede ser mayor al actual.")
				return "año mayor"
		except IndexError:
			print("Valor fuera del rango")
			return None
		except ValueError:
			print("No hay suficientes valores para la fecha.")
			return None
		else:
			if len(anio) != 4:
				print("El año debe de tener 4 digitos")
				return "mal formato año"

			elif len(mes) != 2:
				print("El mes debe de tener 2 digitos  => [-12 > mes > 00-]")
				return "mal formato mes"

			elif len(dia) != 2:
				print("El dia debe de tener 2 digitos")
				return "mal formato dia"

		return "correcto"


def pedir_dato(mensaje, funcion_validadora):
	"""
	Funcion extra de agregar libros, la cual me ayuda a mantener todos los
	campos de los ingresos de libro, y evitando que el codigo se cierre
	cuadno hayun error, asi solamente regresa la funcion y el mensaje de
	errorque la funcion nos dio.
	"""
	while True:
		dato = input(mensaje)
		if dato == "-1":
			return None  # señal para salir
		resultado = funcion_validadora(dato)
		if resultado == "correcto":
			return dato
		else:
			print(f"❌ {resultado}. Intenta de nuevo.")

# Se modularizo el codigo para hacer más óptimo el codigo y poder probar cada parte por separado
def agregar_libros():
	print("Cargando...")
	time.sleep(2)
	print("Listo!")
	time.sleep(1)
	system("clear")
	print("Ingresa lo solicitado a continuacion: (-1 para salir)")
	print("=====================================================")
	nombre_libro = pedir_dato("Título: ", validar_titulo)
	if nombre_libro is None:
		return
	autor_libro = pedir_dato("Autor(es): ", validar_autor)
	if autor_libro is None:
		return
	genero_libro = pedir_dato("Género del libro: ", validar_genero)
	if genero_libro is None:
		return
	editorial_libro = pedir_dato("Editorial: ", validar_editorial)
	if editorial_libro is None:
		return
	fecha_libro = pedir_dato("Fecha de lanzamiento: ", validar_fecha)
	if fecha_libro is None:
		return
	print("=======================================")
	if agl(nombre_libro, autor_libro, fecha_libro, genero_libro, editorial_libro) == "correcto":
		print("Todos los campos son correctos.")
		return


def registrar_usuario():
	system("clear")
	print("Hola, Bienvenido!\nTe pediremos alguno datos personales para continuar.")
	nombre = input("Nombre(s): ")
	apellido = input("Apellido(s): ")
	edad = int(input("Edad: "))
	userid = generar_id(nombre)
	system("clear")
	inguser(userid, nombre, apellido, edad)
	print(f"Hola {nombre} tu id es [{userid}]\nAsegurate de anotarlo en un lugar seguro, con este id puede solicitar libros...")
	time.sleep(5)
	system("clear")


def prestamo_libro():
	system("clear")
	print("Para realizar un prestamo es necesario estar Registrado.")
	print("Opciones para solicitar un Libro:\n1) ID\n2) Nombre\n3) DNI")
	try:
		opcion_prestamo = int(input(">> "))
		if opcion_prestamo == 1:
			print("Ingresa tu id:")
			temporal_id = input(">> ")
			try:
				if validadar_metodo(1, temporal_id) == "usuario existente":
					print("Como deseas buscar el libro?\n1) Autor\n2) Titulo\n3) Genero\n4) ISBN")
					opcion = input(">> ")
					match opcion:
						case '1':
							nl = input("Autor: ")
							bl(1,nl);
						case '2':
							nl = input("Titulo: ")
							bl(2,nl);
						case '3':
							nl = input("Genero: ")
							bl(3,nl);
						case '4':	
							nl = input("ISBN: ")
							bl(4,nl);
				else:
					print("El ID proporcionado no es correcto y/o no existe.")
			except ValueError:
				print("No se pudo registrar el prestamo")
		elif opcion_prestamo == 2:
			print("Ingresa lo siguiente a continuacion")
			print("Primer Nombre:")
			nombre = input(">> ")
			print("Apellido Paterno:")
			apellido = input(">> ")
			try:
				if validadar_metodo(2, nombre, apellido) == "usuario existente":
					print("Como deseas buscar el libro?\n1) Autor\n2) Titulo\n3) Genero\n4) ISBN")
					opcion = input(">> ")
					match opcion:
						case '1':
							nl = input("Autor: ")
							if bl(1,nl) == "correcto":
								# si existe el libro se hara el prestamo
								prestamo_libro(nl)
						case '2':
							nl = input("Titulo: ")
							bl(2,nl);
						case '3':
							nl = input("Genero: ")
							bl(3,nl);
						case '4':	
							nl = input("ISBN: ")
							bl(4,nl);
				else:
					print("El Usuario no existe y/o no esta registrado")
			except ValueError:
				print("No se pudo registrar el prestamo")
	except ValueError:
		system("clear")
		print("La opcion debe ser ingresada con un numero.")

def mostrar_libros_disponibles():
	mostrar_libros()


def BusquedaDeLibro():
	"""Buscar por nombre, autor y género"""
	system("clear")
	print("Buscar Libro por\n• 1) Autor\n• 2) Titulo\n• 3) Genero\n• 4) ID")
	try:
		busqueda = int(input(">> "))
		if busqueda == 1:
			system("clear")
			print("Ingresa el nombre del Autor:")
			atg = input("=> ")
			if bl(1,atg) == "correcto":
				print("=============================")
			else:
				print("El dato proporcionado no es correcto")
		elif busqueda == 2:
			system("clear")
			print("Titulo: ")
			atg = input("=> ")
			if bl(2,atg) == "correcto":
				print("=============================")
			else:
				print("El dato proporcionado no es correcto")
		elif busqueda == 3:
			print("Ingresa el genero del Libro:")
			gdl = input(">> ")
			if bl(3,gdl) == "correcto":
				print("=============================")
			else:
				print("El dato proporcionado no es correcto")
		elif busqueda == 4:
			print("Ingresa el ID del Libro:")
			gdl = input(">> ")
			if bl(5,gdl) == "correcto":
				print("=============================")
			else:
				print("El dato proporcionado no es correcto")
	except ValueError:
		print("Hay un error")


def admon():
	print("Limpiando consola...")
	time.sleep(2)
	system("clear")

print("Cargando...")
time.sleep(3)
print("Listo!")
#   Interfaz base del codigo
def main():
	system("clear")
	while True:  # Sistema de gestion internacional de biblioteca
		print("Sistema de Gestion `Alejandria`")
		print("=============================")
		print(
			"• 1) Agregar un Libro 📚\n• 2) Registrar Usuario 🧑‍💻\n• 3) Solicitar Libro 🤲\n• 4) Libros Disponibles 📖\n• 5) Buscar Libro 🔍\n• 6) Salir🚪\n• 7) Limpiar Consola")
		print("===========================")
		while True:
			try:
				print("¿Que deseas realizar?")
				opcion = input(">> ")
				opcion = opcion.strip(" ")
				if opcion == "nada":
					exit()
			except ValueError as e:
				system("clear")
				print(f"Opcion entera incorrecta => error [=>{e}<=]")
			except KeyboardInterrupt:
				print("Saliendo...")
				break
			else:
				break
		match opcion:
			case '1':
				agregar_libros()
			case '2':
				registrar_usuario()
			case '3':
				prestamo_libro()
			case '4':
				mostrar_libros_disponibles()	
			case '5':
				BusquedaDeLibro()
			case '6':
				print(f"Hasta luego\nUltimo acceso => {fecha}")
				time.sleep(2)
				system("clear")
				break
			case '7':
				admon()
			case _:
				print(f"Opcion fuera del rango '{opcion}'")
#  LLamar a la funcion principal
main()
