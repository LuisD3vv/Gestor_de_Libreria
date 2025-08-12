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
	ean = 978
	country = randint(0, 998)
	editorial = randint(0, 998)
	id_publicacion = randint(0, 998)
	digito_control = randint(0, 10)
	isbn = str(ean) + "-" + str(country) + "-" + str(editorial) + "-" + str(id_publicacion) + "-" + str(digito_control)
	return isbn

def generar_id():
	id_gen = randint(1, 999)
	return id_gen


def malas_palabras(palabra):
	groserias = [
		"verga", "culo", "puta", "perra",
		'pendejo', "pinche", "puto", "basura", "mierda", "vagina", "pene",
		"estupido", "cagada", "bastardo", "joto"]
	if palabra in groserias:
		return True
	else:
		return False

# Posteriormente colocarle el isbn por delante ISBN 000-000-00000-0-0
