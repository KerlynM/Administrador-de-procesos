from database.conexion import conectar

try:
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("SHOW TABLES;")
    tablas = cursor.fetchall()
    
    print("¡Conexión exitosa desde Python!")
    print("Tablas encontradas en la base de datos:")
    for tabla in tablas:
        print(f"- {list(tabla.values())[0]}")
        
    cursor.close()
    conexion.close()
except Exception as e:
    print(f"Ocurrió un error: {e}")