# Funciones comunes
# - validar texto no vacío
# - funciones con map, filter, lambda
# - formatear strings
from random import *

"""

limpiar entradas, utilizar funciones lamba

aqui se crearan las funciones extras como generar los id
prefrabicar los isbn con 13 numeros separados por guiones, facil.
validar entradas nulas
y guardar logs
asi mismo formatear las impresiones
"""

def creacion_isbn():
	Ean = 978
	Country = randint(0, 998)
	Editorial = randint(0, 998)
	Publicacion_ID = randint(0, 998)
	DigitoControl = randint(0, 10)
	ISBN = str(Ean) + "-" + str(Country) + "-" + str(Editorial) + "-" + str(Publicacion_ID) + "-" + str(DigitoControl)
	return ISBN


def generar_id(name):
	"""Con esta funcion crearemos un id unico"""
	nombre_clean = name.strip(" ")
	nom = list(choices(nombre_clean, k=5))
	n = randint(1, 999)
	Gen_ID = f"{"".join(nom)}{n}"
	return str(Gen_ID)


def malas_palabras(palabra):
	groserias = [
		"verga", "culo", "puta", "perra",
		'pendejo', "pinche", "puto", "basura", "mierda", "vagina", "pene",
		"estupido", "cagada", "bastardo", "joto","escoria","vagabundo","mierdero","migajero"]
	if palabra in groserias:
		return True
	else:
		return False


def verificarIndentidad():

	return

def idArtifcial():
	n = 0
	while True:
		yield n
		n += 1

#------------------------------------------------

def admon():
	"""
	No es la gran cosa
	es solamente para modificar
	elementos comunes y faciles	
	"""