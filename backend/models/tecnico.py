from database.conexion import conectar
 
 
def obtener_tecnicos():
    conexion = conectar()
    try:
        with conexion.cursor() as cursor:
            cursor.execute("""
                SELECT
                    ID_tecnico,
                    Nombre,
                    Telefono
                FROM Tecnico
                ORDER BY ID_tecnico DESC
            """)
            tecnicos = cursor.fetchall()
 
        return tecnicos
    finally:
        conexion.close()
 
 
def crear_tecnico(nombre, telefono):
    conexion = conectar()
    try:
        with conexion.cursor() as cursor:
            cursor.execute("""
                INSERT INTO Tecnico (Nombre, Telefono)
                VALUES (%s, %s)
            """, (nombre, telefono))
 
        conexion.commit()
    finally:
        conexion.close()
 
 
def buscar_tecnico_por_id(id_tecnico):
    conexion = conectar()
    try:
        with conexion.cursor() as cursor:
            cursor.execute("""
                SELECT
                    ID_tecnico,
                    Nombre,
                    Telefono
                FROM Tecnico
                WHERE ID_tecnico = %s
            """, (id_tecnico,))
            tecnico = cursor.fetchone()
 
        return tecnico
    finally:
        conexion.close()
 
 
def actualizar_tecnico(id_tecnico, nombre, telefono):
    conexion = conectar()
    try:
        with conexion.cursor() as cursor:
            cursor.execute("""
                UPDATE Tecnico
                SET
                    Nombre = %s,
                    Telefono = %s
                WHERE ID_tecnico = %s
            """, (nombre, telefono, id_tecnico))
 
        conexion.commit()
    finally:
        conexion.close()
 
 
def eliminar_tecnico(id_tecnico):
    conexion = conectar()
    try:
        with conexion.cursor() as cursor:
            cursor.execute("""
                DELETE FROM Tecnico
                WHERE ID_tecnico = %s
            """, (id_tecnico,))
 
        conexion.commit()
    finally:
        conexion.close()