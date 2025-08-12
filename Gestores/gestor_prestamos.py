class Prestamo:
    estado_prestamo = True
    """Generar los prestamos y validaciones correspondientes"""
    def __init__(self,user_id,libro_isbn):
        self.user_id = user_id
        self.libro_isbn = libro_isbn

def prestar_libro():
    ...
def devolver_libro():
    ...
def ver_prestamos():
    ...

# No prestar si ya esta prestado
