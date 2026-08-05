from database.conexion import conectar
import pymysql.err
from werkzeug.security import generate_password_hash

def buscar_usuario(correo):
    conexion = conectar()
    cursor = conexion.cursor()

    sql = "SELECT * FROM usuarios WHERE correo = %s"
    cursor.execute(sql, (correo,))
    
    usuario = cursor.fetchone()

    conexion.close()

    return usuario

def obtener_usuarios():
    conexion = conectar()
    cursor = conexion.cursor()

    sql = "SELECT * FROM usuarios"
    cursor.execute(sql)

    usuarios = cursor.fetchall()

    conexion.close()

    return usuarios

def crear_usuario(nombre, correo, contrasena, rol):
    conexion = conectar()

    try:
        cursor = conexion.cursor()

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
    cursor = conexion.cursor()

    sql = "SELECT * FROM usuarios WHERE ID_usuario = %s"
    cursor.execute(sql, (id_usuario,))

    usuario = cursor.fetchone()

    conexion.close()

    return usuario

def actualizar_usuario(id_usuario, nombre, correo, contrasena, rol):
    conexion = conectar()

    try:
        cursor = conexion.cursor()

        # Ciframos la nueva contraseña antes de actualizarla
        contrasena_hash = generate_password_hash(contrasena)

        sql = """
            UPDATE usuarios
            SET Nombre = %s,
                Correo = %s,
                Contrasena = %s,
                Rol = %s
            WHERE ID_usuario = %s
        """

        cursor.execute(
            sql,
            (nombre, correo, contrasena_hash, rol, id_usuario)
        )

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

    with conexion.cursor() as cursor:
        sql = "DELETE FROM Usuarios WHERE ID_usuario = %s"
        cursor.execute(sql, (id_usuario,))

    conexion.commit()
    conexion.close()