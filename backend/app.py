from datetime import datetime
from werkzeug.security import check_password_hash
from flask import Flask, render_template, request, redirect, url_for, session, flash
from models.usuario import buscar_usuario
from models.inventario import obtener_conteo_inventario
from models.control import obtener_conteo_controles, obtener_actividad_mensual, obtener_operaciones_por_fecha
from database.conexion import conectar
from routes.usuarios import usuarios_bp
from routes.clientes import clientes_bp
from routes.inventario import inventario_bp
from routes.control import control_bp
from routes.tecnico import tecnico_bp
 
app = Flask(__name__, static_folder="../frontend/static")
app.secret_key = "GPS_CONTROL_2026_clave_segura_8xP94"
 
app.register_blueprint(usuarios_bp)
app.register_blueprint(clientes_bp)
app.register_blueprint(inventario_bp)
app.register_blueprint(control_bp)
app.register_blueprint(tecnico_bp)
 
# Función para contar los clientes de forma segura (compatible con DictCursor)
def obtener_conteo_clientes():
    conexion = conectar()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) AS total FROM Clientes")
        res = cursor.fetchone()
        total = res['total'] if isinstance(res, dict) else res[0]
    conexion.close()
    return total
 
@app.route("/")
def inicio():
    return render_template("index.html")
 
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        correo = request.form["correo"]
        contrasena = request.form["contrasena"]
 
        usuario = buscar_usuario(correo)
 
        if usuario and check_password_hash(usuario["Contrasena"], contrasena):
            session["usuario"] = usuario["Nombre"]
            session["id_usuario"] = usuario["ID_usuario"]
            session["rol"] = usuario["Rol"]
            return redirect(url_for("dashboard"))
        else:
            flash("Correo o contraseña incorrectos.", "danger")
 
    return render_template("login.html")
 
@app.route("/olvide-contrasena")
def olvide_contrasena():
    return render_template("olvide.html")
 
@app.route("/dashboard")
def dashboard():
    if "usuario" not in session:
        return redirect(url_for("login"))
 
    fecha_seleccionada = request.args.get("fecha", datetime.now().strftime("%Y-%m-%d"))
 
    inventario_info = obtener_conteo_inventario()
    total_controles_reales = obtener_conteo_controles()
    total_clientes_reales = obtener_conteo_clientes()
    actividad_mensual_reales = obtener_actividad_mensual()
    
    operaciones_dia = obtener_operaciones_por_fecha(fecha_seleccionada)
 
    return render_template(
        "dashboard.html", 
        usuario=session["usuario"], 
        rol=session["rol"],
        gps_disponibles=inventario_info["disponibles"],      
        inventario_chart=inventario_info["chart_data"],      
        total_controles=total_controles_reales,  
        total_clientes=total_clientes_reales,
        actividad_chart=actividad_mensual_reales,
        operaciones_dia=operaciones_dia,          
        fecha_actual=fecha_seleccionada          
    )
 
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))
 
if __name__ == "__main__":
    app.run(debug=True)