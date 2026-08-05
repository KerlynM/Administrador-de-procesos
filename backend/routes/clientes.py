from flask import Blueprint, render_template, request, redirect, url_for, session
from models.cliente import (
    obtener_clientes,
    crear_cliente,
    buscar_cliente_por_id,
    actualizar_cliente,
    eliminar_cliente,
    buscar_cliente_por_rnc
)

clientes_bp = Blueprint(
    "clientes_bp",
    __name__
)


@clientes_bp.route("/clientes")
def clientes():

    if "usuario" not in session:
        return redirect(url_for("login"))

    lista_clientes = obtener_clientes()

    return render_template(
        "clientes.html",
        clientes=lista_clientes
    )


@clientes_bp.route("/clientes/nuevo", methods=["GET", "POST"])
def nuevo_cliente():

    if "usuario" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        nombre = request.form["nombre"]
        rnc_cedula = request.form["rnc_cedula"]
        telefono = request.form["telefono"]

        if buscar_cliente_por_rnc(rnc_cedula):
            return render_template("nuevo_cliente.html", error="El RNC o Cédula ya está registrado.")

        crear_cliente(
            nombre,
            rnc_cedula,
            telefono
        )

        return redirect(url_for("clientes_bp.clientes"))

    return render_template("nuevo_cliente.html")

@clientes_bp.route("/clientes/editar/<int:id_cliente>", methods=["GET", "POST"])
def editar_cliente(id_cliente):

    if "usuario" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        nombre = request.form["nombre"]
        rnc_cedula = request.form["rnc_cedula"]
        telefono = request.form["telefono"]

        cliente_existente = buscar_cliente_por_rnc(rnc_cedula)
        if cliente_existente and cliente_existente['ID_Cliente'] != id_cliente:
            cliente = buscar_cliente_por_id(id_cliente)
            return render_template("editar_cliente.html", cliente=cliente, error="El RNC o Cédula ya está registrado en otro cliente.")

        actualizar_cliente(
            id_cliente,
            nombre,
            rnc_cedula,
            telefono
        )

        return redirect(url_for("clientes_bp.clientes"))

    cliente = buscar_cliente_por_id(id_cliente)

    return render_template(
        "editar_cliente.html",
        cliente=cliente
    )

@clientes_bp.route("/clientes/eliminar/<int:id_cliente>", methods=["POST"])
def eliminar(id_cliente):

    if "usuario" not in session:
        return redirect(url_for("login"))

    eliminar_cliente(id_cliente)

    return redirect(url_for("clientes_bp.clientes"))