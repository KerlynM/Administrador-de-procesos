from flask import Blueprint, render_template, request, redirect, url_for, session, flash

from models.usuario import (
    obtener_usuarios,
    crear_usuario,
    buscar_usuario_por_id,
    actualizar_usuario,
    eliminar_usuario
)

usuarios_bp = Blueprint(
    "usuarios_bp",
    __name__
)

@usuarios_bp.route("/usuarios")
def usuarios():

    if "usuario" not in session:
        return redirect(url_for("login"))

    lista_usuarios = obtener_usuarios()

    return render_template(
        "usuarios.html",
        usuarios=lista_usuarios
    )
@usuarios_bp.route("/usuarios/nuevo", methods=["GET", "POST"])
def nuevo_usuario():

    if request.method == "POST":
        nombre = request.form["nombre"]
        correo = request.form["correo"]
        contrasena = request.form["contrasena"]
        rol = request.form["rol"]

        exito, error = crear_usuario(nombre, correo, contrasena, rol)

        if not exito:
            flash(error, "danger")
            return render_template("nuevo_usuario.html")

        return redirect(url_for("usuarios_bp.usuarios"))

    return render_template("nuevo_usuario.html")

@usuarios_bp.route("/usuarios/editar/<int:id_usuario>", methods=["GET", "POST"])
def editar_usuario(id_usuario):

    usuario = buscar_usuario_por_id(id_usuario)

    if request.method == "POST":
        nombre = request.form["nombre"]
        correo = request.form["correo"]
        contrasena = request.form["contrasena"]
        rol = request.form["rol"]

        exito, error = actualizar_usuario(
            id_usuario,
            nombre,
            correo,
            contrasena,
            rol
        )

        if not exito:
            flash(error, "danger")
            return render_template(
                "editar_usuario.html",
                usuario=usuario
            )

        return redirect(url_for("usuarios_bp.usuarios"))

    return render_template(
        "editar_usuario.html",
        usuario=usuario
    )

@usuarios_bp.route(
    "/usuarios/eliminar/<int:id_usuario>",
    methods=["POST"]
)
def eliminar(id_usuario):

    eliminar_usuario(id_usuario)

    return redirect(url_for("usuarios_bp.usuarios"))