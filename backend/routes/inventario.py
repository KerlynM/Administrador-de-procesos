import pandas as pd
import pymysql.err
from flask import Blueprint, render_template, request, redirect, url_for, session, flash

from models.inventario import (
    obtener_inventario,
    crear_gps,
    buscar_gps_por_id,
    actualizar_gps,
    eliminar_gps,
    obtener_tecnicos
)

inventario_bp = Blueprint(
    "inventario_bp",
    __name__
)

@inventario_bp.route("/inventario")
def inventario():

    if "usuario" not in session:
        return redirect(url_for("login"))

    lista_inventario = obtener_inventario()

    return render_template(
        "inventario.html",
        inventario=lista_inventario
    )

@inventario_bp.route("/inventario/nuevo", methods=["GET", "POST"])
def nuevo_gps():

    if "usuario" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":

        imei = request.form["imei"]
        modelo = request.form["modelo"]
        estado = request.form["estado"]
        id_tecnico = request.form["id_tecnico"] or None
        fecha_entrega = request.form["fecha_entrega"] or None

        exito, error = crear_gps(
            imei,
            modelo,
            estado,
            id_tecnico,
            fecha_entrega
        )

        if not exito:
            flash(error, "danger")
            tecnicos = obtener_tecnicos()
            return render_template("nuevo_gps.html", tecnicos=tecnicos)

        return redirect(url_for("inventario_bp.inventario"))

    tecnicos = obtener_tecnicos()
    return render_template("nuevo_gps.html", tecnicos=tecnicos)

@inventario_bp.route(
    "/inventario/editar/<int:id_gps>",
    methods=["GET", "POST"]
)
def editar_gps(id_gps):

    if "usuario" not in session:
        return redirect(url_for("login"))

    gps = buscar_gps_por_id(id_gps)

    if request.method == "POST":

        imei = request.form["imei"]
        modelo = request.form["modelo"]
        estado = request.form["estado"]
        id_tecnico = request.form["id_tecnico"] or None
        fecha_entrega = request.form["fecha_entrega"] or None

        actualizar_gps(
            id_gps,
            imei,
            modelo,
            estado,
            id_tecnico,
            fecha_entrega
        )

        return redirect(url_for("inventario_bp.inventario"))

    tecnicos = obtener_tecnicos()
    return render_template(
        "editar_gps.html",
        gps=gps,
        tecnicos=tecnicos
    )

@inventario_bp.route(
    "/inventario/eliminar/<int:id_gps>",
    methods=["POST"]
)
def eliminar(id_gps):

    if "usuario" not in session:
        return redirect(url_for("login"))

    eliminar_gps(id_gps)

    return redirect(url_for("inventario_bp.inventario"))


@inventario_bp.route("/inventario/importar", methods=["POST"])
def importar_inventario():
    if "usuario" not in session:
        return redirect(url_for("login"))

    if "archivo" not in request.files:
        flash("No se seleccionó ningún archivo", "danger")
        return redirect(url_for("inventario_bp.inventario"))
    
    archivo = request.files["archivo"]
    
    if archivo.filename == "":
        flash("Nombre de archivo inválido", "danger")
        return redirect(url_for("inventario_bp.inventario"))

    try:
        # Leemos el archivo con Pandas
        df = pd.read_excel(archivo)

        # Nombre de la columna en tu archivo de Excel (modifícalo si se llama distinto)
        columna_imei = 'IMEI_CodigoBarras' 
        
        # Limpiamos y normalizamos la columna para evitar el error de duplicados por celdas vacías
        if columna_imei in df.columns:
            df[columna_imei] = df[columna_imei].astype(str).str.strip()
            df[columna_imei] = df[columna_imei].replace(['', 'nan', 'None', 'NAT', 'NaT'], None)

        # Contadores para el resumen de la importación
        insertados = 0
        duplicados = 0

        # Recorremos cada fila del Excel e insertamos
        for index, row in df.iterrows():
            imei = row.get(columna_imei)
            
            # Si el IMEI viene vacío o es nulo (por espacios en blanco del excel), saltamos la fila
            if pd.isna(imei) or imei is None:
                continue

            # Obtenemos los demás datos, si están nulos les damos valores por defecto
            modelo_excel = row.get("Modelo")
            modelo = str(modelo_excel).strip() if pd.notna(modelo_excel) else ""
            
            estado_excel = row.get("Estado")
            estado = str(estado_excel).strip() if pd.notna(estado_excel) else "Disponible"
            
            # Llamamos a tu función crear_gps importada de models.inventario
            exito, error = crear_gps(
                imei,           # imei
                modelo,          # modelo
                estado,          # estado
                None,            # id_tecnico (vacío por defecto al importar)
                None             # fecha_entrega (vacío por defecto al importar)
            )

            if exito:
                insertados += 1
            else:
                duplicados += 1

        if duplicados:
            flash(f"Se importaron {insertados} GPS. {duplicados} fila(s) con IMEI duplicado fueron omitidas.", "warning")
        else:
            flash("Inventario importado exitosamente desde Excel.", "success")

        return redirect(url_for("inventario_bp.inventario"))

    # CAPTURAMOS EL ERROR DE DUPLICIDAD ESPECÍFICAMENTE AQUÍ:
    except pymysql.err.IntegrityError:
        flash("Error: El archivo contiene uno o más IMEI (o códigos de barra) que ya están registrados en la base de datos.", "danger")
        return redirect(url_for("inventario_bp.inventario"))

    # CAPTURAMOS CUALQUIER OTRO ERROR GENERAL:
    except Exception as e:
        flash(f"Error al procesar el archivo Excel: {e}", "danger")
        return redirect(url_for("inventario_bp.inventario"))