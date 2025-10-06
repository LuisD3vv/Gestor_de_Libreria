import unittest
from Gestores.gestor_usuarios import ingresar_usuario,Usuario
import sqlite3
from utils import generar_id,gen_apellidos_pruebas as gena,gen_nombres_pruebas as genn, generar_id_pruebas as gin
from random import *

class Pruebausuario(unittest.TestCase):
    def setUp(self):
        self.conn = sqlite3.connect(":memory:")
        self.cur = self.conn.cursor()
        self.cur.execute("CREATE TABLE Usuario (User_id INTEGER PRIMARY KEY, Nombre text NOT NULL, Apellido text NOT NULL, Edad INTEGER DEFAULT 0);")
        self.conn.commit()

    def tearDown(self):
        self.conn.close()
        
    """Probar el ingreso de un nuevo usuario"""
    def test_ingreso_usuario(self):
        """Comprobar si el usuario se ingreso correctamente"""
        nombre = " "
        apellido = " "
        edad = 21
        user_id = ""
        
        resultado = ingresar_usuario(nombre, apellido, edad, user_id)
        # Si lo que regresa la funcion ingresar usuario es una insatncia de la clase Usuario
        self.assertIsInstance(resultado,Usuario,msg="no es una instancia de la clase")
        
    def test_verificar_ingreso_usuario(self):
        nombre = genn()
        apellido = gena()
        edad = randint(0,99)
        user_id = gin()
        print(f"Type of user_id: {type(user_id)}")
        print(f"Type of nombre: {type(nombre)}")
        print(f"Type of apellido: {type(apellido)}")
        print(f"Type of edad: {type(edad)}")
        
        self.conn.execute("INSERT INTO Usuario (User_id, Nombre, Apellido, Edad) values (?,?,?,?)",(user_id,nombre,apellido,edad))
        self.conn.commit()
        
        self.conn.execute("select nombre,apellido from Usuario where Titulo user_id ?", (user_id,))
        resultado = self.cursor.fetchone()
        
        self.assertIsNone(resultado,"no se encontro una coinciencia en la base de datos")
        if resultado:
            self.assertEqual(resultado[0],nombre)
            self.assertEqual(resultado[1],apellido)


if __name__ == '__name__':
    unittest.main()
