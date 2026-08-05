from database.conexion import conectar

def obtener_controles():
    conexion = conectar()
    with conexion.cursor() as cursor:
        sql = """
        SELECT
            Controles.ID_Control,
            Controles.FechaInstalacion,
            Controles.Tipo,
            Controles.Chasis,
            Controles.Modelo,
            Controles.Ano,
            Controles.Color,
            Controles.Placa,
            Clientes.Nombre AS NombreCliente,
            Tecnico.Nombre AS NombreTecnico,
            Inventario.IMEI_CodigoBarras AS IMEI,
            Usuarios.Nombre AS NombreUsuario
        FROM Controles
        INNER JOIN Clientes
            ON Controles.ID_cliente = Clientes.ID_Cliente
        INNER JOIN Tecnico
            ON Controles.ID_tecnico = Tecnico.ID_tecnico
        INNER JOIN Inventario
            ON Controles.ID_GPS = Inventario.ID_GPS
        INNER JOIN Usuarios
            ON Controles.ID_Usuario = Usuarios.ID_usuario
        ORDER BY Controles.ID_Control DESC
        """
        cursor.execute(sql)
        controles = cursor.fetchall()
    conexion.close()
    return controles

def crear_control(
    fecha_instalacion,
    id_cliente,
    id_tecnico,
    id_gps,
    id_usuario,
    tipo,
    chasis,
    modelo,
    ano,
    color,
    placa
):
    conexion = conectar()
    with conexion.cursor() as cursor:
        if tipo and tipo.strip().lower() in ["instalacion", "instalación"]:
            sql_verificar = """
                SELECT COUNT(*) AS total 
                FROM Controles 
                WHERE ID_GPS = %s AND (LOWER(Tipo) = 'instalacion' OR LOWER(Tipo) = 'instalación')
            """
            cursor.execute(sql_verificar, (id_gps,))
            resultado = cursor.fetchone()
            total = resultado['total'] if isinstance(resultado, dict) else resultado[0]
            
            if total > 0:
                conexion.close()
                return "Este dispositivo GPS ya cuenta con una instalación registrada y no puede tener otra."

        sql = """
        INSERT INTO Controles (
            FechaInstalacion,
            ID_cliente,
            ID_tecnico,
            ID_GPS,
            ID_Usuario,
            Tipo,
            Chasis,
            Modelo,
            Ano,
            Color,
            Placa
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(
            sql,
            (
                fecha_instalacion,
                id_cliente,
                id_tecnico,
                id_gps,
                id_usuario,
                tipo,
                chasis,
                modelo,
                ano,
                color,
                placa
            )
        )

        # Actualizar automáticamente el estado del GPS en el inventario según el tipo
        if tipo:
            tipo_lower = tipo.strip().lower()
            if "instalacion" in tipo_lower or "instalación" in tipo_lower:
                cursor.execute("UPDATE Inventario SET Estado = 'Instalado' WHERE ID_GPS = %s", (id_gps,))
            elif "desinstalacion" in tipo_lower or "desinstalación" in tipo_lower:
                cursor.execute("UPDATE Inventario SET Estado = 'Disponible' WHERE ID_GPS = %s", (id_gps,))

    conexion.commit()
    conexion.close()
    return None

def buscar_control_por_id(id_control):
    conexion = conectar()
    with conexion.cursor() as cursor:
        sql = """
        SELECT *
        FROM Controles
        WHERE ID_Control = %s
        """
        cursor.execute(sql, (id_control,))
        control = cursor.fetchone()
    conexion.close()
    return control

def actualizar_control(
    id_control,
    fecha_instalacion,
    id_cliente,
    id_tecnico,
    id_gps,
    id_usuario,
    tipo,
    chasis,
    modelo,
    ano,
    color,
    placa
):
    conexion = conectar()
    with conexion.cursor() as cursor:
        if tipo and tipo.strip().lower() in ["instalacion", "instalación"]:
            sql_verificar = """
                SELECT COUNT(*) AS total 
                FROM Controles 
                WHERE ID_GPS = %s AND (LOWER(Tipo) = 'instalacion' OR LOWER(Tipo) = 'instalación') AND ID_Control != %s
            """
            cursor.execute(sql_verificar, (id_gps, id_control))
            resultado = cursor.fetchone()
            total = resultado['total'] if isinstance(resultado, dict) else resultado[0]
            
            if total > 0:
                conexion.close()
                return "Este dispositivo GPS ya cuenta con otra instalación registrada."

        sql = """
        UPDATE Controles
        SET
            FechaInstalacion = %s,
            ID_cliente = %s,
            ID_tecnico = %s,
            ID_GPS = %s,
            ID_Usuario = %s,
            Tipo = %s,
            Chasis = %s,
            Modelo = %s,
            Ano = %s,
            Color = %s,
            Placa = %s
        WHERE ID_Control = %s
        """
        cursor.execute(
            sql,
            (
                fecha_instalacion,
                id_cliente,
                id_tecnico,
                id_gps,
                id_usuario,
                tipo,
                chasis,
                modelo,
                ano,
                color,
                placa,
                id_control
            )
        )

        # Actualizar automáticamente el estado del GPS en el inventario según el tipo
        if tipo:
            tipo_lower = tipo.strip().lower()
            if "instalacion" in tipo_lower or "instalación" in tipo_lower:
                cursor.execute("UPDATE Inventario SET Estado = 'Instalado' WHERE ID_GPS = %s", (id_gps,))
            elif "desinstalacion" in tipo_lower or "desinstalación" in tipo_lower:
                cursor.execute("UPDATE Inventario SET Estado = 'Disponible' WHERE ID_GPS = %s", (id_gps,))

    conexion.commit()
    conexion.close()
    return None

def eliminar_control(id_control):
    conexion = conectar()
    with conexion.cursor() as cursor:
        sql = """
        DELETE FROM Controles
        WHERE ID_Control = %s
        """
        cursor.execute(sql, (id_control,))
    conexion.commit()
    conexion.close()

def obtener_clientes():
    conexion = conectar()
    with conexion.cursor() as cursor:
        cursor.execute("""
            SELECT ID_Cliente, Nombre
            FROM Clientes
            ORDER BY Nombre
        """)
        clientes = cursor.fetchall()
    conexion.close()
    return clientes

def obtener_tecnicos():
    conexion = conectar()
    with conexion.cursor() as cursor:
        cursor.execute("""
            SELECT ID_tecnico, Nombre
            FROM Tecnico
            ORDER BY Nombre
        """)
        tecnicos = cursor.fetchall()
    conexion.close()
    return tecnicos

def obtener_gps():
    conexion = conectar()
    with conexion.cursor() as cursor:
        cursor.execute("""
            SELECT
                ID_GPS,
                IMEI_CodigoBarras
            FROM Inventario
            ORDER BY IMEI_CodigoBarras
        """)
        gps = cursor.fetchall()
    conexion.close()
    return gps

def obtener_usuarios():
    conexion = conectar()
    with conexion.cursor() as cursor:
        cursor.execute("""
            SELECT
                ID_usuario,
                Nombre
            FROM Usuarios
            ORDER BY Nombre
        """)
        usuarios = cursor.fetchall()
    conexion.close()
    return usuarios

def obtener_conteo_controles():
    conexion = conectar()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) AS total FROM Controles")
        res = cursor.fetchone()
        total = res['total'] if isinstance(res, dict) else res[0]
    conexion.close()
    return total

def obtener_actividad_mensual():
    conexion = conectar()
    with conexion.cursor() as cursor:
        sql = """
            SELECT MONTH(FechaInstalacion) AS mes, COUNT(*) AS total
            FROM Controles
            WHERE FechaInstalacion IS NOT NULL
            GROUP BY MONTH(FechaInstalacion)
        """
        cursor.execute(sql)
        resultados = cursor.fetchall()
    conexion.close()

    meses_conteo = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for row in resultados:
        if isinstance(row, dict):
            m = row.get('mes')
            t = row.get('total', 0)
        else:
            m = row[0]
            t = row[1]
        
        if m and 1 <= m <= 12:
            meses_conteo[m - 1] = t
            
    return meses_conteo

def obtener_operaciones_por_fecha(fecha):
    conexion = conectar()
    res = None
    try:
        with conexion.cursor() as cursor:
            # COALESCE obliga a que si la consulta SQL da nulo, devuelva directamente un 0 matemático
            cursor.execute("""
                SELECT 
                    COALESCE(SUM(CASE WHEN (LOWER(Tipo) LIKE '%instal%' OR LOWER(Tipo) LIKE '%instalacion%') 
                                   AND LOWER(Tipo) NOT LIKE '%des%' 
                                   AND LOWER(Tipo) NOT LIKE '%re%' THEN 1 ELSE 0 END), 0) as instalaciones,
                    COALESCE(SUM(CASE WHEN LOWER(Tipo) LIKE '%desinst%' THEN 1 ELSE 0 END), 0) as desinstalaciones,
                    COALESCE(SUM(CASE WHEN LOWER(Tipo) LIKE '%cambio%' OR LOWER(Tipo) LIKE '%camb%' THEN 1 ELSE 0 END), 0) as cambios,
                    COALESCE(SUM(CASE WHEN LOWER(Tipo) LIKE '%reinst%' THEN 1 ELSE 0 END), 0) as reinstalaciones
                FROM Controles 
                WHERE DATE(FechaInstalacion) = %s
            """, (fecha,))
            res = cursor.fetchone()
    except Exception as e:
        print(f"Error al obtener operaciones por fecha: {e}")
    finally:
        conexion.close()

    if not res:
        return {'instalaciones': 0, 'desinstalaciones': 0, 'cambios': 0, 'reinstalaciones': 0}
    
    # Se convierte estrictamente a entero int() para que el front no tenga problemas al leer los datos
    if isinstance(res, dict):
        return {
            'instalaciones': int(res.get('instalaciones', 0)),
            'desinstalaciones': int(res.get('desinstalaciones', 0)),
            'cambios': int(res.get('cambios', 0)),
            'reinstalaciones': int(res.get('reinstalaciones', 0))
        }
    else:
        return {
            'instalaciones': int(res[0] if res[0] is not None else 0),
            'desinstalaciones': int(res[1] if res[1] is not None else 0),
            'cambios': int(res[2] if res[2] is not None else 0),
            'reinstalaciones': int(res[3] if res[3] is not None else 0)
        }