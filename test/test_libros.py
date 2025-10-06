import unittest
from Gestores.gestor_libros import agregar_libro as agl,Libro
from utils import generar_id,creacion_isbn
import sqlite3



# Funcion de insersion
# def ingresar_libro(titulo_libro,autor_libro,fecha,isbn,genero,editoria):
#     conn = sqlite3.connect(":memory:")
#     cursor = conn.cursor()
#     #  Creando la base de datos de los libros
#     cursor.execute("CREATE TABLE IF NOT EXIST Libro ("
#                 "Titulo VARCHAR(45) NOT NULL"
#                 "Autor VARCHAR(45) NOT NULL"
#                 "Fecha DATE"
#                 "Genero VARCHAR(45) NOT NULL"
#                 "Editorial(45) NOT NULL"
#                 "ISBN INTEGER"
#                 ")")
#     conn.execute("INSERT INTO Libro () values (?,?,?,?,?,?)",(titulo_libro,autor_libro,fecha,genero,editoria,isbn))
#     conn.commit()
#     conn.close()


"""_summary_
Las funciones setup y teardown nos ayduan a crear un ambiente donde podemos ejecutar purebas en base de datos temporaales por cada una de als preubas que hagamos.
"""

class PruebaLibro(unittest.TestCase):
    def setUp(self):
        """
        Set up crea una conexion con la base de datos en memoria
        """
        self.conn = sqlite3.connect(":memory:")
        self.cursor = self.conn.cursor()
        #  Creando la base de datos de los libros
        self.cursor.execute("CREATE TABLE Libro ("
                "Titulo VARCHAR(45) NOT NULL,"
                "Autor VARCHAR(45) NOT NULL,"
                "Fecha DATE,"
                "Genero VARCHAR(45) NOT NULL,"
                "Editorial VARCHAR(45) NOT NULL,"
                "ISBN INTEGER"
                ")")
        self.conn.commit()
    
    def tearDown(self):
        """
        tearDown termina la conexion con la base de datos en memoria para liberar recursos
        """
        self.conn.close()

    def test_ingreso_libro(self):
        titulo_libro = "Harry potter"
        autor_libro = "JK Rowling"
        gen_isb = creacion_isbn()
        # pasar argumentos con nombre
        fecha =  "10-01-1999"
        genero= "ciencia ficcion",
        editorial = "LissandroDEv"
    
        LibroActual = agl(titulo_libro,autor_libro,fecha,gen_isb,genero,editorial)
        self.assertIsInstance(LibroActual,Libro, "Es una instancia")

    def test_ingreso_libro_a_databse_exitoso(self):
        titulo_libro = "Harry potter"
        autor_libro = "JK Rowling"
        gen_isb = creacion_isbn()
        # pasar argumentos con nombre
        fecha =  "10-01-1999"
        isbn = gen_isb
        genero= "ciencia ficcion"
        editorial = "LissandroDEv"
        
        
        self.conn.execute("INSERT INTO Libro (Titulo, Autor, Fecha, Genero, Editorial,ISBN) values (?,?,?,?,?,?)",(titulo_libro,autor_libro,fecha,genero,editorial,isbn))
        self.conn.commit()
        
        
        self.conn.execute("select Titulo,Autor from libro where Titulo like ?",(titulo_libro,))
        resultado = self.cursor.fetchone()
        
        self.assertIsNone(resultado,"no se encontro una coinciencia en la base de datos")
        if resultado:
            self.assertEqual(resultado[0],titulo_libro)
            self.assertEqual(resultado[1],autor_libro)
        
        
if __name__ == "__main__":
    unittest.main()
