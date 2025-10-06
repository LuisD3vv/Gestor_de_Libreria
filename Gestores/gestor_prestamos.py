from datetime import datetime
import sqlite3
from pathlib import Path
from os import system,name
from time import sleep

hoy = datetime.now().strftime("%d-%m-%Y")
ruta_db = Path("sql/GestorGeneral.db")
rutalog = Path("logs/log_prestamos.txt")

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
	return "".join(sistema) # type: ignore

def validadar_metodo(*args): # type: ignore
    # Si esperas que el argumento sea 1, args llega como tupla, por eso se compara con args[0][1] etc
    # Buscar usuario por ID
    try:
        with sqlite3.connect(ruta_db) as conn:  # conectar con la base de datos
            if args[0] == 1:
                table_id = args[1] # type: ignore
                try:
                    cur = conn.cursor()  # utilizar los comandos
                    # ejecutar una consulta
                    cur.execute(
                        "SELECT nombre, apellido FROM Usuario WHERE User_id = ?", (table_id,) # type: ignore
                    )
                    user_actual = cur.fetchone()  # traer un solo resultado
                    if user_actual:
                        return "usuario existente"
                    else:
                        return "id inexistente"
                except sqlite3.Error as error:
                    print('Hubo un error =>', error)

            elif args[0] == 2:
                nom = args[1].strip(" ") # pyright: ignore[reportUnknownVariableType, reportUnknownMemberType]
                ape = args[2].strip(" ") # type: ignore
                try:
                    cur = conn.cursor()
                    cur.execute(
                        "SELECT User_id, Nombre FROM Usuario WHERE Nombre like ? and Apellido like ?",
                        (f"%{nom}%", f"%{ape}%"),
                    )
                    user_actual = cur.fetchone()  # traer un solo resultado
                    if user_actual:
                        return "usuario existente"
                except sqlite3.Error as error:
                    print('Hubo un error =>', error)

    # except sqlite3.DatabaseError as e:
    #     print(f" Ha ocurrido un error => {e}")

    except ValueError:
        print("Asegurate de escribir bien la opcion")
    return None

def activarDatabase():
    with sqlite3.connect(ruta_db, timeout=30,check_same_thread=False) as con:
        con.execute("PRAGMA journal_mode = WAL;")
        con.execute("PRAGMA busy_timeout = 30000;")

def prestar_libro(busqueda, libro, *args):
	tipo:int = busqueda
	libroLimpio:str = libro.strip()
	(nombre,apellido) = args
    
    # 1 ) Recibir el datos del usuario
	with sqlite3.connect(ruta_db,timeout=30,check_same_thread=False) as con:
		cur = con.cursor()
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
		cur.execute(f"SELECT Libro_ID FROM Libro WHERE {columna} LIKE ? ", (f"%{libroLimpio}%",))
		lid = cur.fetchone()
		cur.execute("SELECT User_id FROM Usuario WHERE Nombre LIKE ? and Apellido LIKE ? ",(f"%{nombre}%", f"%{apellido}%"),)
		usid = cur.fetchone()
		print(f"DEBUG {lid}  => {type(lid)}")
		print(f"DEBUG {usid} => {type(usid)}")
		if usid and lid == None:
			return "usuario o libro no encontrados"

	# Eliminar coma de la tupla unitaria.
	libroid = lid[0]
	userid = usid[0]
	print(f"DEBUG {libroid} => {type(libroid)}")
	print(f"DEBUG {userid} => {type(userid)}")

	# 2 )  Verificar el estado del libro
	# timeout es para darle mas tiempo de preparacion a la ejecucion de la base de datos, y check_same_tread es para poder usar la conexion en otro hilo si este tarda mas.
	with sqlite3.connect(ruta_db,timeout=30,check_same_thread=False) as con:
		cur = con.cursor()
		cur.execute("SELECT prestado FROM Prestamo WHERE Libro_id = ?", (libroid,))   
		prestado = cur.fetchone()
		if prestado == None or prestado[0] == 0:
			print("El libro esta disponible (sin prestamo aun)")
		elif prestado[0] == 1:
			print(prestado[0])
			print("El Libro esta actualmente prestado")
			return "libro en prestamo"
		else:
			print("Hay algo mal en la funcion")

	# 3 )  Prestar el libro si todo lo de arriba salio correcto.
	with sqlite3.connect(ruta_db,timeout=30,check_same_thread=False) as con:
		cur = con.cursor()
		print("Realizando prestamo...")
		sleep(2)
		system(validar_plataforma())
		cur.execute("INSERT INTO Prestamo (Libro_ID,Usuario_id,FechaPrestamo,prestado) VALUES (?,?,?,?)",(libroid, userid, hoy, True))
		con.commit()
		return "prestamo realizado"
	with open ( rutalog, "a") as log:
		log.writelines(f"USER_ID {userid} | LIBRO ID {libroid}")
	print(f"prestamo realizado por el Usuario => {userid}")

def devolver_libro():
	"""Funcion cambia el estado del libro"""
	print("Selecciona la opcion para regresar el libro\n1) Titulo y Autor \n2) ID")
	opcion = input(">> ")
	match opcion:
		case '1':
			print("A continuacion ingresa el titulo del libro y su autor")
			while True:
				print("Ingresa el nombre del autor.")
				Rautor=input(">> ")
				print("Ingresa el titulo del libro.")
				Rtitulo= input(">> ")
				try:
					with sqlite3.connect(ruta_db,timeout=30,check_same_thread=False) as con:
						cur = con.cursor()
						# tomar el id del libro
						cur.execute("SELECT Libro_ID FROM Libro WHERE Titulo LIKE ? AND Autor LIKE ?",(f"%{Rautor}%", f"%{Rtitulo}%"))
						id_libro = cur.fetchone()
						print(f"La variable : {id_libro} de tipo: {type(id_libro)}")
						if id_libro:
							limpio = id_libro[0]
							cur.execute("UPDATE Prestamo SET prestado = 0 WHERE Libro_ID = ?",(limpio,))
							con.commit()
						else:
							print("No se han encontrado resultados")
							return
					print("Libro regresado con exito.")
				except ValueError:
					print("Valor incorrecto introducido")
		case '2':
			while True:
				print("Ingresa el ID del Libro")
				Regreso = input(">> ")
				try:
					Regreso = int(Regreso)
					with sqlite3.connect(ruta_db,timeout=30,check_same_thread=False) as con:
						cur = con.cursor()
						cur.execute("UPDATE Prestamo SET prestado = 0 where Libro_ID = ?",(Regreso,))
						con.commit()
					
					print("Libro regresado con exito.")
					break
				except ValueError:
					print("El id es numerico")
		case _:
			print("Error en seleccion de opcion crack")

def ver_prestamos():
	try:
		with sqlite3.connect(ruta_db) as conn:
			cur  = conn.cursor()
			cur.execute("SELECT DISTINCT Libro.titulo, Prestamo.Usuario_id FROM Libro JOIN Prestamo ON Libro.Libro_ID = Prestamo.Libro_ID")
			todos = cur.fetchall()
			print(f"DEBUG => {todos}")
			system(validar_plataforma())
			print("Libros en prestamo actualmente: ")
			if todos:
				for prestado,userid in todos:
					print("- Titulo: ", prestado, f"=> ( -{userid}- )")
				print("\n")
			else:
				print("No hubo resultados")
	except TypeError:
		print("Ocurrio un error")
