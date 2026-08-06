import pymysql.err
from flask import Blueprint, render_template, request, redirect, url_for, session, flash

from models.tecnico import (
    obtener_tecnicos,
    crear_tecnico,
    buscar_tecnico_por_id,
    actualizar_tecnico,
    eliminar_tecnico
)

tecnico_bp = Blueprint(
    "tecnico_bp",
    __name__
)


@tecnico_bp.route("/tecnicos")
def tecnicos():

    if "usuario" not in session:
        return redirect(url_for("login"))

    lista_tecnicos = obtener_tecnicos()

    return render_template(
        "tecnicos.html",
        tecnicos=lista_tecnicos
    )

@tecnico_bp.route("/tecnicos/nuevo", methods=["GET", "POST"])
def nuevo_tecnico():

    if "usuario" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":

        nombre = request.form["nombre"]
        telefono = request.form["telefono"]

        crear_tecnico(nombre, telefono)

        return redirect(url_for("tecnico_bp.tecnicos"))

    return render_template("nuevo_tecnico.html")

@tecnico_bp.route(
    "/tecnicos/editar/<int:id_tecnico>",
    methods=["GET", "POST"]
)
def editar_tecnico(id_tecnico):

    if "usuario" not in session:
        return redirect(url_for("login"))

    tecnico = buscar_tecnico_por_id(id_tecnico)

    if request.method == "POST":

        nombre = request.form["nombre"]
        telefono = request.form["telefono"]

        actualizar_tecnico(
            id_tecnico,
            nombre,
            telefono
        )

        return redirect(url_for("tecnico_bp.tecnicos"))

    return render_template(
        "editar_tecnico.html",
        tecnico=tecnico
    )

@tecnico_bp.route(
    "/tecnicos/eliminar/<int:id_tecnico>",
    methods=["POST"]
)
def eliminar(id_tecnico):

    if "usuario" not in session:
        return redirect(url_for("login"))

    try:
        eliminar_tecnico(id_tecnico)
        flash("Técnico eliminado correctamente.", "success")
        
    except pymysql.err.IntegrityError:
        flash("Este técnico tiene registros asociados, no se puede eliminar.", "danger")
        
    except Exception as e:
        flash(f"Ocurrió un error inesperado: {str(e)}", "danger")

    return redirect(url_for("tecnico_bp.tecnicos"))