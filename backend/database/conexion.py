import pymysql

def conectar():
    conexion = pymysql.connect(
        host="localhost",
        user="root",
        password="",
        database="administrador_procesos",
        cursorclass=pymysql.cursors.DictCursor
    )

    return conexion
if __name__ == "__main__":
    try:
        db = conectar()
        print("¡Conexión exitosa a la base de datos!")
        db.close()
    except Exception as e:
        print(f"Error al conectar: {e}")