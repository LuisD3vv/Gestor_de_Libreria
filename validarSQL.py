import sqlite3
ruta = "sql/GestorGeneral.db"
try:
    with sqlite3.connect(ruta) as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM Libro")
        conn.commit()
        todos = cur.fetchall()
        for i in todos:
            print(*i)
except sqlite3.Error as e:
    print(f"error {e}")
    
try:
    with sqlite3.connect(ruta) as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM Prestamo")
        conn.commit()
        todos = cur.fetchall()
        for i in todos:
            print(*i)
except sqlite3.Error as e:
    print(f"error {e}")

    
try:
    with sqlite3.connect(ruta) as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM Usuario")
        conn.commit()
        todos = cur.fetchall()
        for i in todos:
            print(*i)
except sqlite3.Error as e:
    print(f"error {e}")
    
    