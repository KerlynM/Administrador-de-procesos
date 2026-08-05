from database.conexion import conectar
import pymysql.err


def obtener_inventario():
    conexion = conectar()

    with conexion.cursor() as cursor:
        sql = """
        SELECT
            Inventario.ID_GPS,
            Inventario.IMEI_CodigoBarras,
            Inventario.Modelo,
            Inventario.Estado,
            Inventario.ID_tecnico,
            Inventario.FechaEntrega,
            Tecnico.Nombre AS NombreTecnico
        FROM Inventario
        LEFT JOIN Tecnico
            ON Inventario.ID_tecnico = Tecnico.ID_tecnico
        """

        cursor.execute(sql)
        inventario = cursor.fetchall()

    conexion.close()
    return inventario


def crear_gps(imei, modelo, estado, id_tecnico, fecha_entrega):
    conexion = conectar()

    try:
        with conexion.cursor() as cursor:
            sql = """
            INSERT INTO Inventario
            (
                IMEI_CodigoBarras,
                Modelo,
                Estado,
                ID_tecnico,
                FechaEntrega
            )
            VALUES (%s, %s, %s, %s, %s)
            """

            cursor.execute(
                sql,
                (
                    imei,
                    modelo,
                    estado,
                    id_tecnico,
                    fecha_entrega
                )
            )

        conexion.commit()
        return True, None

    except pymysql.err.IntegrityError:
        conexion.rollback()
        return False, "Ya existe un GPS registrado con ese IMEI/Código de barras."

    finally:
        conexion.close()


# ==========================================
# FUNCIÓN PARA INSERCIÓN MASIVA DESDE EXCEL (FILTRO ESTRICTO ANTIVACÍOS)
# ==========================================
def crear_gps_lote(lista_gps):
    conexion = conectar()

    datos_validos = []
    for item in lista_gps:
        if not item or len(item) < 2:
            continue
            
        imei_raw = item[0]
        modelo_raw = item[1]
        
        if imei_raw is None or modelo_raw is None:
            continue
            
        imei = str(imei_raw).strip()
        modelo = str(modelo_raw).strip()
        
        # Descartar filas vacías, nulas, con espacios o texto 'nan' de pandas
        if not imei or imei.lower() == "nan" or not modelo or modelo.lower() == "nan":
            continue
            
        # Obtener valores opcionales de manera segura
        estado_raw = item[2] if len(item) > 2 else None
        estado = str(estado_raw).strip() if estado_raw is not None and str(estado_raw).strip().lower() != "nan" and str(estado_raw).strip() != "" else "Disponible"
        
        id_tecnico_raw = item[3] if len(item) > 3 else None
        try:
            id_tecnico = int(id_tecnico_raw) if id_tecnico_raw is not None and str(id_tecnico_raw).strip().lower() != "nan" and str(id_tecnico_raw).strip() != "" else None
        except (ValueError, TypeError):
            id_tecnico = None
            
        fecha_raw = item[4] if len(item) > 4 else None
        fecha_entrega = str(fecha_raw).strip() if fecha_raw is not None and str(fecha_raw).strip().lower() != "nan" and str(fecha_raw).strip() != "" else None
        if fecha_entrega and ' 00:00:00' in fecha_entrega:
            fecha_entrega = fecha_entrega.split(' ')[0]

        datos_validos.append((imei, modelo, estado, id_tecnico, fecha_entrega))

    if not datos_validos:
        conexion.close()
        return

    with conexion.cursor() as cursor:
        sql = """
        INSERT INTO Inventario
        (
            IMEI_CodigoBarras,
            Modelo,
            Estado,
            ID_tecnico,
            FechaEntrega
        )
        VALUES (%s, %s, %s, %s, %s)
        """
        cursor.executemany(sql, datos_validos)

    conexion.commit()
    conexion.close()


def buscar_gps_por_id(id_gps):
    conexion = conectar()

    with conexion.cursor() as cursor:
        sql = """
        SELECT *
        FROM Inventario
        WHERE ID_GPS = %s
        """

        cursor.execute(sql, (id_gps,))
        gps = cursor.fetchone()

    conexion.close()
    return gps 


def actualizar_gps(
    id_gps,
    imei,
    modelo,
    estado,
    id_tecnico,
    fecha_entrega
):
    conexion = conectar()

    with conexion.cursor() as cursor:
        sql = """
        UPDATE Inventario
        SET
            IMEI_CodigoBarras = %s,
            Modelo = %s,
            Estado = %s,
            ID_tecnico = %s,
            FechaEntrega = %s
        WHERE ID_GPS = %s
        """

        cursor.execute(
            sql,
            (
                imei,
                modelo,
                estado,
                id_tecnico,
                fecha_entrega,
                id_gps
            )
        )

    conexion.commit()
    conexion.close()


def eliminar_gps(id_gps):
    conexion = conectar()

    with conexion.cursor() as cursor:
        sql = """
        DELETE FROM Inventario
        WHERE ID_GPS = %s
        """

        cursor.execute(sql, (id_gps,))

    conexion.commit()
    conexion.close()


# ==========================================
# FUNCIÓN PARA EXTRAER DATOS AL DASHBOARD
# ==========================================
def obtener_conteo_inventario():
    conexion = conectar()

    with conexion.cursor() as cursor:
        # Consulta para "Disponible"
        cursor.execute("SELECT COUNT(*) AS total FROM Inventario WHERE Estado = 'Disponible'")
        res1 = cursor.fetchone()
        disponibles = res1['total'] if isinstance(res1, dict) else res1[0]

        # Consulta para "Asignado"
        cursor.execute("SELECT COUNT(*) AS total FROM Inventario WHERE Estado = 'Asignado'")
        res2 = cursor.fetchone()
        asignados = res2['total'] if isinstance(res2, dict) else res2[0]

        # Consulta para "Instalado"
        cursor.execute("SELECT COUNT(*) AS total FROM Inventario WHERE Estado = 'Instalado'")
        res3 = cursor.fetchone()
        instalados = res3['total'] if isinstance(res3, dict) else res3[0]

    conexion.close()

    # Retorna un diccionario listo para usar en tu app.py y enviarlo al HTML/Chart.js
    return {
        "disponibles": disponibles,
        "asignados": asignados,
        "instalados": instalados,
        "chart_data": [disponibles, asignados, instalados]
    }


# ==========================================
# FUNCIÓN PARA OBTENER TÉCNICOS EN EL INVENTARIO
# ==========================================
def obtener_tecnicos():
    conexion = conectar()

    with conexion.cursor() as cursor:
        sql = """
        SELECT ID_tecnico, Nombre
        FROM Tecnico
        """
        cursor.execute(sql)
        tecnicos = cursor.fetchall()

    conexion.close()
    return tecnicos