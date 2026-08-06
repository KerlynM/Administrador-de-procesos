from database.conexion import conectar
 
 
def obtener_clientes():
    conexion = conectar()
    try:
        with conexion.cursor() as cursor:
            sql = "SELECT * FROM Clientes"
            cursor.execute(sql)
 
            clientes = cursor.fetchall()
 
        return clientes
    finally:
        conexion.close()
 
 
def crear_cliente(nombre, rnc_cedula, telefono):
    conexion = conectar()
    try:
        with conexion.cursor() as cursor:
            sql = """
            INSERT INTO Clientes (Nombre, RncCedula, Telefono)
            VALUES (%s, %s, %s)
            """
 
            cursor.execute(sql, (nombre, rnc_cedula, telefono))
 
        conexion.commit()
    finally:
        conexion.close()
 
 
def buscar_cliente_por_id(id_cliente):
    conexion = conectar()
    try:
        with conexion.cursor() as cursor:
            sql = """
            SELECT *
            FROM Clientes
            WHERE ID_Cliente = %s
            """
            cursor.execute(sql, (id_cliente,))
 
            cliente = cursor.fetchone()
 
        return cliente
    finally:
        conexion.close()
 
 
def actualizar_cliente(
    id_cliente,
    nombre,
    rnc_cedula,
    telefono
):
    conexion = conectar()
    try:
        with conexion.cursor() as cursor:
            sql = """
            UPDATE Clientes
            SET Nombre = %s,
                RncCedula = %s,
                Telefono = %s
            WHERE ID_Cliente = %s
            """
 
            cursor.execute(
                sql,
                (
                    nombre,
                    rnc_cedula,
                    telefono,
                    id_cliente
                )
            )
 
        conexion.commit()
    finally:
        conexion.close()
 
 
def eliminar_cliente(id_cliente):
    conexion = conectar()
    try:
        with conexion.cursor() as cursor:
            sql = """
            DELETE FROM Clientes
            WHERE ID_Cliente = %s
            """
 
            cursor.execute(sql, (id_cliente,))
 
        conexion.commit()
    finally:
        conexion.close()
 
 
def buscar_cliente_por_rnc(rnc_cedula):
    conexion = conectar()
    try:
        with conexion.cursor() as cursor:
            sql = """
            SELECT *
            FROM Clientes
            WHERE RncCedula = %s
            """
            cursor.execute(sql, (rnc_cedula,))
 
            cliente = cursor.fetchone()
 
        return cliente
    finally:
        conexion.close()