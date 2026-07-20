from flask import Blueprint, render_template, request, redirect, url_for
from db import get_database
from bson.objectid import ObjectId
from bson.errors import InvalidId
from datetime import datetime, time

quartos_bp = Blueprint("quartos", __name__)
db = get_database()


def montar_status_quartos(quartos):
    agora = datetime.now()
    inicio_hoje = datetime.combine(agora.date(), time.min)
    fim_hoje = datetime.combine(agora.date(), time.max)

    for quarto in quartos:
        reserva_hoje = db["reservas"].find_one({
            "quarto_numero": quarto["numero"],
            "status": {"$ne": "cancelada"},
            "data_checkin": {"$lte": fim_hoje},
            "data_checkout": {"$gt": inicio_hoje}
        })

        reserva_futura = db["reservas"].find_one({
            "quarto_numero": quarto["numero"],
            "status": {"$ne": "cancelada"},
            "data_checkin": {"$gt": fim_hoje}
        })

        if reserva_hoje:
            quarto["status_exibicao"] = "ocupado"
        elif reserva_futura:
            quarto["status_exibicao"] = "reservado"
        else:
            quarto["status_exibicao"] = "disponível"

    return quartos


@quartos_bp.route("/quartos")
def listar_quartos():
    quartos = list(db["quartos"].find().sort("numero", 1))
    quartos = montar_status_quartos(quartos)

    return render_template(
        "quartos.html",
        quartos=quartos,
        quarto_selecionado=None,
        reservas_quarto=[]
    )


@quartos_bp.route("/quartos/<int:numero>")
def detalhar_quarto(numero):
    quartos = list(db["quartos"].find().sort("numero", 1))
    quartos = montar_status_quartos(quartos)

    quarto_selecionado = db["quartos"].find_one({"numero": numero})

    if not quarto_selecionado:
        return redirect(url_for("quartos.listar_quartos"))

    reservas_quarto = list(
        db["reservas"]
        .find({
            "quarto_numero": numero,
            "status": {"$ne": "cancelada"}
        })
        .sort("data_checkin", 1)
    )

    for reserva in reservas_quarto:
        hospede = db["hospedes"].find_one({"cpf": reserva["hospede_cpf"]})
        reserva["hospede_nome"] = hospede["nome"] if hospede else "Não encontrado"

    return render_template(
        "quartos.html",
        quartos=quartos,
        quarto_selecionado=quarto_selecionado,
        reservas_quarto=reservas_quarto
    )


@quartos_bp.route("/quartos/novo", methods=["GET", "POST"])
def novo_quarto():
    if request.method == "POST":
        db["quartos"].insert_one({
            "numero": int(request.form["numero"]),
            "tipo": request.form["tipo"],
            "capacidade": int(request.form["capacidade"]),
            "valor_diaria": float(request.form["valor_diaria"])
        })
        return redirect(url_for("quartos.listar_quartos"))

    return render_template("quarto_form.html")


@quartos_bp.route("/quartos/editar/<id>", methods=["GET", "POST"])
def editar_quarto(id):
    try:
        quarto = db["quartos"].find_one({"_id": ObjectId(id)})
    except InvalidId:
        return redirect(url_for("quartos.listar_quartos"))

    if not quarto:
        return redirect(url_for("quartos.listar_quartos"))

    if request.method == "POST":
        db["quartos"].update_one(
            {"_id": ObjectId(id)},
            {
                "$set": {
                    "numero": int(request.form["numero"]),
                    "tipo": request.form["tipo"],
                    "capacidade": int(request.form["capacidade"]),
                    "valor_diaria": float(request.form["valor_diaria"])
                }
            }
        )
        return redirect(url_for("quartos.listar_quartos"))

    return render_template("quarto_form.html", quarto=quarto)


@quartos_bp.route("/quartos/excluir/<id>")
def excluir_quarto(id):
    try:
        db["quartos"].delete_one({"_id": ObjectId(id)})
    except InvalidId:
        pass

    return redirect(url_for("quartos.listar_quartos"))