from database.conexion import conectar
import pymysql.err
from werkzeug.security import generate_password_hash
 
 
def buscar_usuario(correo):
    conexion = conectar()
    try:
        with conexion.cursor() as cursor:
            sql = "SELECT * FROM usuarios WHERE correo = %s"
            cursor.execute(sql, (correo,))
 
            usuario = cursor.fetchone()
 
        return usuario
    finally:
        conexion.close()
 
 
def obtener_usuarios():
    conexion = conectar()
    try:
        with conexion.cursor() as cursor:
            sql = "SELECT * FROM usuarios"
            cursor.execute(sql)
 
            usuarios = cursor.fetchall()
 
        return usuarios
    finally:
        conexion.close()
 
 
def crear_usuario(nombre, correo, contrasena, rol):
    conexion = conectar()
 
    try:
        with conexion.cursor() as cursor:
            # Ciframos la contraseña antes de guardarla en la base de datos
            contrasena_hash = generate_password_hash(contrasena)
 
            sql = """
                INSERT INTO usuarios (Nombre, Correo, Contrasena, Rol)
                VALUES (%s, %s, %s, %s)
            """
 
            cursor.execute(sql, (nombre, correo, contrasena_hash, rol))
 
        conexion.commit()
        return True, None
 
    except pymysql.err.IntegrityError:
        conexion.rollback()
        return False, "Ya existe un usuario registrado con ese correo."
 
    except pymysql.err.OperationalError as e:
        conexion.rollback()
        if len(e.args) > 1 and "chk_usuarios_rol" in str(e.args[1]):
            return False, "El rol debe ser 'Administrador' u 'Operaciones'."
        raise
 
    finally:
        conexion.close()
 
 
def buscar_usuario_por_id(id_usuario):
    conexion = conectar()
    try:
        with conexion.cursor() as cursor:
            sql = "SELECT * FROM usuarios WHERE ID_usuario = %s"
            cursor.execute(sql, (id_usuario,))
 
            usuario = cursor.fetchone()
 
        return usuario
    finally:
        conexion.close()
 
 
def actualizar_usuario(id_usuario, nombre, correo, contrasena, rol):
    conexion = conectar()
 
    try:
        with conexion.cursor() as cursor:
            # Solo re-hasheamos y actualizamos la contraseña si mandaron una nueva.
            # Si el campo llega vacío/None, se conserva la contraseña actual del usuario.
            if contrasena:
                contrasena_hash = generate_password_hash(contrasena)
                sql = """
                    UPDATE usuarios
                    SET Nombre = %s,
                        Correo = %s,
                        Contrasena = %s,
                        Rol = %s
                    WHERE ID_usuario = %s
                """
                parametros = (nombre, correo, contrasena_hash, rol, id_usuario)
            else:
                sql = """
                    UPDATE usuarios
                    SET Nombre = %s,
                        Correo = %s,
                        Rol = %s
                    WHERE ID_usuario = %s
                """
                parametros = (nombre, correo, rol, id_usuario)
 
            cursor.execute(sql, parametros)
 
        conexion.commit()
        return True, None
 
    except pymysql.err.IntegrityError:
        conexion.rollback()
        return False, "Ya existe un usuario registrado con ese correo."
 
    except pymysql.err.OperationalError as e:
        conexion.rollback()
        if len(e.args) > 1 and "chk_usuarios_rol" in str(e.args[1]):
            return False, "El rol debe ser 'Administrador' u 'Operaciones'."
        raise
 
    finally:
        conexion.close()
 
 
def eliminar_usuario(id_usuario):
    conexion = conectar()
    try:
        with conexion.cursor() as cursor:
            sql = "DELETE FROM Usuarios WHERE ID_usuario = %s"
            cursor.execute(sql, (id_usuario,))
 
        conexion.commit()
    finally:
        conexion.close()