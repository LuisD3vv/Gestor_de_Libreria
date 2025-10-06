import unittest
from Gestores.gestor_prestamos import *
import os


class PrestamoPrueba(unittest.TestCase):
    def setUp(self):
        # Conectar a una base de datos en memoria para cada prueba
        self.conn = sqlite3.connect(':memory:')
        self.cursor = self.conn.cursor()
        self.cursor.execute("CREATE TABLE Prestamo (Prestamo_ID INTEGER PRIMARY KEY, Libro_ID text,Usuario_id text, FechaPrestamo DATE,prestado boolean)")
        self.conn.commit()

    def tearDown(self):
        # Cerrar la conexión y eliminar las tablas creadas
        self.conn.close()
        
    def test_validar_metodo(self):
        """Tomando en cuenta que las opciones hasta el momento solo son nombre e id"""
        esperado = "usuario existente"
        nombre = "Lissandro"
        apellido = "Aguilar"
        id_usuario = "Luisdev90"
        valFun = validadar_metodo(1,id_usuario) #@ metodo id
        valFun2 = validadar_metodo(1,nombre,apellido) #@ metodo nombre y apellido
        self.assertEqual(esperado,valFun,msg="No es el resultado esperado")
        self.assertEqual(esperado,valFun2,msg="No es el resultado esperado")
        
        
    def test_prestarLibro(self):
        """Resultado esperado de un prestamo"""
        nombre = "Lissandro"
        apellido = "Aguilar"
        # No funciona con el id 1, ya que es el mismo numero booleano para marcar verdadero
        Libro_ejemplo = "X"
        # busqueda, numero 1 para autor, numero 2 para titulo, numero 3 para genero, numero 4 para isbn
        busqueda = 2
        valorEsperado = "prestamo realizado"
        prestamo = prestar_libro(busqueda,Libro_ejemplo,nombre,apellido)
        self.assertEqual(valorEsperado,prestamo,"El prestamo se realizo")
        
    def test_verificar_prestamo_libro(self):
        prestado = 1
        user_id = 11
        Libro_id = 3
        fecha = "05-05-2004"
        self.conn.execute("INSERT INTO Prestamo (Libro_ID,Usuario_id,FechaPrestamo,prestado) values (?,?,?,?)",(Libro_id,user_id,fecha,prestado))
        self.conn.commit()
        
        self.conn.execute("SELECT Libro_ID,Usuario_id FROM Prestamo where prestado = ?",(prestado,))
        resultado = self.cursor.fetchone()
        
        self.assertIsNone(resultado,"no se encontro una coinciencia en la base de datos")
        if resultado:
            self.assertEqual(resultado[0],Libro_id)
            self.assertEqual(resultado[1],Libro_id)
            
            
if __name__ == "__main__":
    unittest.main()
