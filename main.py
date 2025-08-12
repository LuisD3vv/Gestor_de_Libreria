#from os import system
import time
from Gestores.gestor_libros import agregar_libro as agl  # asi agregamos una funcion especifica
from Gestores.gestor_usuarios import ingresar_usuario as inguser
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
	print("Hay palabras malsonantes")
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
				return "anio mayor"
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
	# system("clear")
	print("listo!")
	print("Menú de ingreso de libros (-1 para salir en cualquier campo):")
	nombre_libro = pedir_dato("Título del libro: ", validar_titulo)
	if nombre_libro is None:
		return
	autor_libro = pedir_dato("Nombre del autor: ", validar_autor)
	if autor_libro is None:
		return
	genero_libro = pedir_dato("Género del libro: ", validar_genero)
	if genero_libro is None:
		return
	editorial_libro = pedir_dato("Editorial del libro: ", validar_editorial)
	if editorial_libro is None:
		return
	fecha_libro = pedir_dato("Fecha del libro: ", validar_fecha)
	if fecha_libro is None:
		return
	if agl(nombre_libro, autor_libro, fecha_libro, genero_libro, editorial_libro) == "correcto":
		print("Libro correcto")
		return


def registrar_usuario():
	#system("clear")
	print("Hola, Bienvenido!\nTe pediremos algunos datos para continuar.")
	nombre = input("Ingresa tu nombre: ")
	apellido = input("Ingresa tu apellido: ")
	edad = int(input("Edad: "))

	inguser(nombre, apellido, edad)


def prestamo_libro():
	print("Has seleccionado prestar libro")
	print("Para realizar un prestamo es necesario estar registrado con una id.")


def mostrar_libros_disponibles():
	...


def buscar_Libro():
	"""Buscar por nombre, autor y género"""
	#system("clear")
	print("Buscar por\n1) Autor\n2) Nombre\n3) Genero")
	busqueda = int(input("Eleccion: "))


print("Cargando...")
time.sleep(3)
print("Listo!")


#system("clear")
#  Interfaz base
def main():
	#system("clear")
	while True:  # Sistema de gestion internacional de biblioteca
		print("Bienvenido al -SDGIB-")
		print(
			"1) Agregar Libro\n2) Registrar usuario\n3) Pedir un Libro\n4) Libros disponibles\n5) Buscar Libro\n6) Salir")
		while True:
			try:
				print("Selecciona la opcion de tu interes")
				opcion = input(">> ")
				if opcion == "nada":
					exit()
			except ValueError as e:
				#system("clear")
				print(f"Opcion entera incorrecta => error [|{e}|]")
			except KeyboardInterrupt:
				print("Has salido del codigo")
			else:
				break
		print(f"La opcion elegida es {opcion}")
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
				buscar_Libro()
			case '6':
				break
			case _:
				print(f"Opcion fuera del rango '{opcion}'")


#  LLamar a la funcion principal
main()
#  Probar funciones por separado
"""while True:
	try:
		print("Ingresa una fecha")
		fech = input("fecha = [-DD-MM-YYYY-]:")
		if fech == "-1":
			break
	except ValueError:
		print("ERROR")
	except KeyboardInterrupt:
		print("se interrumpio el loop")
	else:
		if validar_fecha(fech) == "correcto":
			print(fech)
			break
		else:
			continue
print(validar_fecha(fech))
"""
