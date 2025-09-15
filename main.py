from os import system
import time
from Gestores.gestor_libros import agregar_libro as agl,mostrar_libros,buscar_libro as bl  # asi agregamos una funcion especifica
from Gestores.gestor_usuarios import ingresar_usuario as inguser
from Gestores.gestor_prestamos import prestar_libro, validadar_metodo
from utils import generar_id
from utils import malas_palabras
from datetime import date
from validaciones import *

fecha = date.today()
#  Formatear la fecha dia,mes y anno  
fecha_hoy = fecha.strftime("%d-%m-%Y")

"""
Es mucho mejor utilizar rutas absolutas, MUCHISMO, asi que a la hora de hacerlo portable
esto se debe a desde donde se ejecuta el programa, no se ejecuta donde esta
por ejemplo desde aqui no daria error porque es el principal y desde donde se ejecuta
pero si utilizara rutas relativas desde otro lugar, daria error porque lo buscaria desde donde
esta este archivo
"""

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
	while True:
		edad = input("Edad >> ")
		try:
			edad = int(edad)
			break
		except:
			print("Ingresa un numero")
	userid = generar_id(nombre)
	system("clear")
	inguser(userid, nombre, apellido, edad)
	print(f"Hola {nombre}, tu id es {userid}\nCon este id puedes solicitar libros existentes en el sistema.")
	time.sleep(5)
	system("clear")

def prestamo_libro():
	system("clear")
	print("Es necesario estar Registrado Para Solicitar un libro,\nsi no lo estas, puedes registrarte en cualquier momento en el menu.")
	print("Opciones disponibles para solicitar un Libro:\n• 1) ID\n• 2) Nombre\n• 3) -DNI(decraped)")
	try:
		opcion_prestamo = int(input(" >> "))
		if opcion_prestamo == 1:
			print("Ingresa tu id:")
			temporal_id = input(" >> ")
			try:
				if validadar_metodo(1, temporal_id) == "usuario existente":
					system("clear")
					#  Segundo uso de la funcion  busqueda de libro
					print("¿Como deseas buscar el libro?\n• 1) Autor\n• 2) Titulo\n• 3) Genero\n• 4) ISBN")
					opcion = input(" >> ")
					match opcion:
						case '1':
							system("clear")
							nl = input("Autor: ")
							bl(1,nl)
						case '2':
							system("clear")
							nl = input("Titulo: ")
							bl(2,nl)
						case '3':
							system("clear")
							nl = input("Genero: ")
							if bl(3,nl) == "correcto":
								print("culo")
						case '4':	
							system("clear")
							nl = input("ISBN: ")
							bl(4,nl)
				else:
					system("clear")
					print("El ID proporcionado no es correcto y/o no existe.")
			except ValueError:
				print("No se pudo registrar el prestamo")
		elif opcion_prestamo == 2:
			print("Ingresa lo siguiente a continuacion")
			print("Primer Nombre:")
			nombre = input(" >> ")
			print("Apellido Paterno:")
			apellido = input(" >> ")
			try:
				if validadar_metodo(2, nombre, apellido) == "usuario existente":
					print("¿Como deseas buscar el libro?\n1) Autor\n2) Titulo\n3) Genero\n4) ISBN")
					opcion = input(" >> ")
					match opcion:
						case '1':
							#  si es correcto, asumimos que el usuario existe y el libro tambien
							system("clear")
							nl = input("Autor: ")
							if bl(1,nl) == "correcto":
								print("¿Quieres llevarte alguno de los libro mostrados? ")
								presLibro = input(" >> ")
								if presLibro == 'si':
									print("Ingresa el titulo del libro:")
									nomLibro = input(" >> ")
									prestar_libro(1,nomLibro,nombre,apellido)
							else:
								print("hay un error en la Funcion")
						case '2':
							system("clear")
							nl = input("Titulo: ")
							if bl(2,nl) == "correcto":
								print("¿Deseas llevarte alguno? ")
								presLibro = input(" >> ")
								if presLibro == 'si':
									print("Ingresa el titulo del libro")
									nomLibro = input(" >> ")
									prestar_libro(2,nomLibro,nombre,apellido)
							else:
								print("Hay un error en la Funcion")
						case '3':
							system("clear")
							nl = input("Genero: ")
							if bl(3,nl) == "correcto":
								print("¿Te interesa algun libro de los mostrado? (si-no)")
								presLibro = input(" >> ")
								if presLibro == 'si':
									print("Ingresa su nombre del libro")
									nomLibro = input(" >> ")
									try:
										prestar_libro(2,nomLibro,nombre,apellido)
									except TypeError:
										print("Porfavor Selecciona una opcion valida.")
							else:
								print("hay un error en la Funcion")
						case '4':
							system("clear")
							nl = input("ISBN: ")
							bl(4,nl);
				else:
					system("clear")
					print("El Usuario no existe y/o no esta registrado")
			except ValueError as e:
				print("No se pudo registrar el prestamo {}".format(e))
	except ValueError:
		system("clear")
		print("La opcion debe ser ingresada con un numero.")

def mostrar_libros_disponibles():
	mostrar_libros()

def BusquedaDeLibro():
	"""Buscar por nombre, autor y género"""
	system("clear")
	print("Buscar Libro por\n• 1) Autor\n• 2) Titulo\n• 3) Genero\n• 4) ISBN\n• 5) ID")
	try:
		busqueda = int(input(" >> "))
		if busqueda == 1:
			system("clear")
			print("Ingresa el nombre del Autor:")
			atg = input(" => ")
			if bl(1,atg) == "correcto":
				print("=============================")
			else:
				print(f"No existe un Autor con ese nombre {atg}.")
		elif busqueda == 2:
			system("clear")
			print("Titulo: ")
			atg = input(" => ")
			if bl(2,atg) == "correcto":
				print("=============================")
			else:
				print(f"No existe un libro con ese titulo {atg}.")
		elif busqueda == 3:
			print("Ingresa el genero del Libro:")
			atg = input(" >> ")
			if bl(3,atg) == "correcto":
				print("=============================")
			else:
				print(f"Asegurate de habber escrito bien el genero {atg}.")
		elif busqueda == 4:
			print("Ingresa el ISBN del Libro:")
			atg = input(" >> ")
			if bl(5,atg) == "correcto":
				print("=============================")
			else:
				print(f"¿El ISBN esta bien escrito?: {atg}")
		elif busqueda == 5:
			print("Ingresa el ID corresponiente al Libro.")
			atg = input(" >> ")
			if bl(5,atg) == "correcto":
				print("=============================")
			else:
				print(f"No hay ningun Libro relacionado con el ID proporcionado => {atg}.")
	except ValueError:
		print("Hay un error")

def admon():
	print("Limpiando consola...")
	time.sleep(2)
	system("clear")

print("Cargando...")
print("Sistema operado por RoXxon\nTodos los derechos reservados(2025)")
time.sleep(3)
print("Listo!")
#   Interfaz base del codigo
def main():
	system("clear")
	while True: 
		print("Welcome back to\nAutomated Library Service Management System = > [A.L.S.M.S]")
		print("=============================")
		print(
			"Opciones Disponibles:\n• 1) Agregar un Libro 📚\n• 2) Registrar Usuario 🧑‍💻\n• 3) Solicitar Libro 🤲\n• 4) Libros Disponibles 📖\n• 5) Buscar Libro 🔍\n• 6) Salir🚪\n• 7) Limpiar Consola\n• 8) (NUEVO) Recetas -->")
		print("Terminos y garantias Limitadas.\n===================================")
		while True:
			try:
				print("¿Que deseas realizar?")
				opcion = input(">> ")
				opcion = opcion.strip(" ")
				if opcion == "nada" or opcion == "no":
					print("Has salido.")
					exit()
			except ValueError as e:
				system("clear")
				print(f"Opcion incorrecta => {e}")
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
				print("Sistema operado bajo WesTek todos los derechos reservados")
				time.sleep(2)
				system("clear")
				break
			case '7':
				admon()
			case _:
				print(f"Opcion fuera del rango '{opcion}'")
#  LLamar a la funcion principal
main()
