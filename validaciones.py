#  print(dia_hoy,mes_hoy,anio_hoy)
from utils import malas_palabras
from datetime import date

fecha = date.today()
#  Formatear la fecha dia,mes y anno  
fecha_hoy = fecha.strftime("%d-%m-%Y")
(dia_hoy, mes_hoy, anio_hoy) = fecha_hoy.split("-")

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