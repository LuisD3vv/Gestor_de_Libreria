Diseño general  


>**NO OLVIDAR REPASAR EJERCICIOS Y TEMAS VISTOS, DOCUMENTACION, PRACTICAR, USAR HERRRAMIENTAS, INTENTRALO, PROBAR, EQUIVOCARSE, APRENDER, TODO ES PARTE.**
#
>biblioteca/
├── main.py                  ← Punto de entrada (interfaz por consola)
├── gestor_libros.py         ← Funciones y clases para libros
├── gestor_usuarios.py       ← Funciones y clases para usuarios
├── gestor_prestamos.py      ← Funciones y lógica de préstamos
├── utils.py                 ← Funciones útiles (map, filtros, validaciones)
├── tests/
│   ├── test_libros.py
│   ├── test_usuarios.py
│   └── test_prestamos.py

Lo que se pondra a prueba

 POO (clases y objetos) setter y getter

✅ Manejo de listas, diccionarios y sets

✅ Funciones de orden superior (map, filter, lambda)

✅ Manejo de errores

✅ unittest para probar lógica de negocio

✅ Uso de __name__ == "__main__"

✅ Separación en módulos (recuerda que para que una carpeta se considere paquete se necesita tener u archivo llamado __init__.py)

#
#Funcionalidades esperadas

>Libros

    Agregar libro (título, autor, año, ISBN)

    Buscar libro por título o autor

    Listar todos los libros

    Usar map() para mostrar títulos en mayúscula

    Usar filter() para buscar por año
#
>Usuarios

    Registrar usuario (nombre, ID único)

    Buscar usuario por ID

    Listar usuarios
#
>Préstamos

    Prestar libro a usuario

    Ver libros prestados

    Devolver libro

    Verificar disponibilidad del libro
#
>🧪 Tests esperados

    ¿Se guarda bien un libro?

    ¿Buscar por autor devuelve los libros correctos?

    ¿El préstamo no se puede duplicar?

    ¿Un usuario inexistente no puede pedir un libro?
#
>Interfaz esperada 

1. Agregar libro
2. Registrar usuario
3. Prestar libro
4. Listar libros
5. Buscar libro
6. Salir
#
>Acomodo de secciones

# Clase Libro: título, autor, año, ISBN
# Lista de libros
# Funciones:
# - agregar_libro()
# - buscar_por_titulo()
# - buscar_por_autor()
# - listar_libros()
#
>🧍 gestor_usuarios.py

# Clase Usuario: nombre, ID único
# Lista de usuarios
# Funciones:
# - registrar_usuario()
# - buscar_usuario()
# - listar_usuarios()
#
>🔄 gestor_prestamos.py

# Clase Prestamo: usuario, libro
# Lista de préstamos
# Funciones:
# - prestar_libro()
# - devolver_libro()
# - ver_prestamos()
# Validación: no prestar si ya está prestado
#
>🔧 utils.py

# Funciones comunes
# - validar texto no vacío
# - funciones con map, filter, lambda
# - formatear strings
#
>🧪 tests/

# test_libros.py       → Prueba agregar/buscar libros
# test_usuarios.py     → Prueba registrar/buscar usuarios
# test_prestamos.py    → Prueba préstamos y devoluciones

# Todos deben usar unittest y tener su bloque:
# if __name__ == "__main__":
#     unittest.main()

>🧭 main.py (menú por consola) # modulo principal, donde se llamara a los demas modulos para tener una interfaz limpia y tener buenas practicas como programador

# Menú con opciones numeradas
# Usar input() para elegir acción
# Llamar funciones desde otros módulos
# Cerrar con opción "salir"

>Ejemplo de testeo de un setter

import unittest
from gestor_libros import Libro

class TestLibro(unittest.TestCase):
    def test_setter_titulo_invalido(self):
        libro = Libro("1984", "Orwell", 1949, "123ABC")
        with self.assertRaises(ValueError):
            libro.titulo = ""  # setter activado

if __name__ == "__main__":
    unittest.main()
