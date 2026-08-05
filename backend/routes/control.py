from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from datetime import date

from models.control import (
    obtener_controles,
    crear_control,
    buscar_control_por_id,
    actualizar_control,
    eliminar_control,
    obtener_clientes,
    obtener_tecnicos,
    obtener_gps,
    obtener_usuarios,
    obtener_operaciones_por_fecha
)

control_bp = Blueprint(
    "control_bp",
    __name__
)

@control_bp.route("/controles")
def controles():
    if "usuario" not in session:
        return redirect(url_for("login"))

    lista_controles = obtener_controles()
    return render_template(
        "controles.html",
        controles=lista_controles
    )

@control_bp.route("/controles/nuevo", methods=["GET", "POST"])
def nuevo_control():
    if "usuario" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        fecha_instalacion = request.form["fecha_instalacion"]
        id_cliente = request.form["id_cliente"]
        id_tecnico = request.form["id_tecnico"]
        id_gps = request.form["id_gps"]
        id_usuario = request.form["id_usuario"]
        tipo = request.form["tipo"]
        chasis = request.form["chasis"]
        modelo = request.form["modelo"]
        ano = request.form["ano"]
        color = request.form["color"]
        placa = request.form["placa"] or None

        mensaje_error = crear_control(
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
        
        if mensaje_error:
            flash(mensaje_error, "danger")
            return redirect(url_for("control_bp.nuevo_control"))
        
        flash("Control registrado exitosamente.", "success")
        return redirect(url_for("control_bp.controles"))

    clientes = obtener_clientes()
    tecnicos = obtener_tecnicos()
    gps = obtener_gps()
    usuarios = obtener_usuarios()
    
    return render_template(
        "nuevo_control.html",
        clientes=clientes,
        tecnicos=tecnicos,
        gps=gps,
        usuarios=usuarios
    )

@control_bp.route(
    "/controles/editar/<int:id_control>",
    methods=["GET", "POST"]
)
def editar_control(id_control):
    if "usuario" not in session:
        return redirect(url_for("login"))

    control = buscar_control_por_id(id_control)

    if request.method == "POST":
        fecha_instalacion = request.form["fecha_instalacion"]
        id_cliente = request.form["id_cliente"]
        id_tecnico = request.form["id_tecnico"]
        id_gps = request.form["id_gps"]
        id_usuario = request.form["id_usuario"]
        tipo = request.form["tipo"]
        chasis = request.form["chasis"]
        modelo = request.form["modelo"]
        ano = request.form["ano"]
        color = request.form["color"]
        placa = request.form["placa"] or None

        mensaje_error = actualizar_control(
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
        )

        if mensaje_error:
            flash(mensaje_error, "danger")
            return redirect(url_for("control_bp.editar_control", id_control=id_control))

        flash("Control actualizado exitosamente.", "success")
        return redirect(url_for("control_bp.controles"))

    clientes = obtener_clientes()
    tecnicos = obtener_tecnicos()
    gps = obtener_gps()
    usuarios = obtener_usuarios()

    return render_template(
        "editar_control.html",
        control=control,
        clientes=clientes,
        tecnicos=tecnicos,
        gps=gps,
        usuarios=usuarios
    )

@control_bp.route("/controles/eliminar/<int:id_control>", methods=["POST"])
def eliminar(id_control):
    if "usuario" not in session:
        return redirect(url_for("login"))

    eliminar_control(id_control)
    flash("Control eliminado exitosamente.", "success")
    return redirect(url_for("control_bp.controles"))

@control_bp.route("/controles/api/operaciones", methods=["GET"])
def api_operaciones_por_fecha():
    if "usuario" not in session:
        return jsonify({"error": "No autorizado"}), 401

    fecha_seleccionada = request.args.get("fecha")
    if not fecha_seleccionada:
        fecha_seleccionada = date.today().strftime("%Y-%m-%d")

    datos = obtener_operaciones_por_fecha(fecha_seleccionada)
    return jsonify(datos)