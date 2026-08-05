from database.conexion import conectar


def obtener_clientes():
    conexion = conectar()

    with conexion.cursor() as cursor:
        sql = "SELECT * FROM Clientes"
        cursor.execute(sql)

        clientes = cursor.fetchall()

    conexion.close()

    return clientes

def crear_cliente(nombre, rnc_cedula, telefono):
    conexion = conectar()

    with conexion.cursor() as cursor:
        sql = """
        INSERT INTO Clientes (Nombre, RncCedula, Telefono)
        VALUES (%s, %s, %s)
        """

        cursor.execute(sql, (nombre, rnc_cedula, telefono))

    conexion.commit()
    conexion.close()

def buscar_cliente_por_id(id_cliente):
    conexion = conectar()

    with conexion.cursor() as cursor:
        sql = """
        SELECT *
        FROM Clientes
        WHERE ID_Cliente = %s
        """
        cursor.execute(sql, (id_cliente,))

        cliente = cursor.fetchone()

    conexion.close()

    return cliente

def actualizar_cliente(
    id_cliente,
    nombre,
    rnc_cedula,
    telefono
):
    conexion = conectar()

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
    conexion.close()

def eliminar_cliente(id_cliente):
    conexion = conectar()

    with conexion.cursor() as cursor:
        sql = """
        DELETE FROM Clientes
        WHERE ID_Cliente = %s
        """

        cursor.execute(sql, (id_cliente,))

    conexion.commit()
    conexion.close()

def buscar_cliente_por_rnc(rnc_cedula):
    conexion = conectar()

    with conexion.cursor() as cursor:
        sql = """
        SELECT *
        FROM Clientes
        WHERE RncCedula = %s
        """
        cursor.execute(sql, (rnc_cedula,))

        cliente = cursor.fetchone()

    conexion.close()

    return cliente