from flask import Blueprint, render_template, request, redirect, url_for
from db import get_database
from bson.objectid import ObjectId
from datetime import datetime

reservas_bp = Blueprint("reservas", __name__)
db = get_database()


@reservas_bp.route("/reservas")
def listar_reservas():
    reservas = list(db["reservas"].find())
    return render_template("reservas.html", reservas=reservas)


@reservas_bp.route("/reservas/novo", methods=["GET", "POST"])
def nova_reserva():
    if request.method == "POST":
        db["reservas"].insert_one({
            "hospede_cpf": request.form["hospede_cpf"],
            "quarto_numero": int(request.form["quarto_numero"]),
            "funcionario_id": int(request.form["funcionario_id"]),
            "data_reserva": datetime.now(),
            "data_checkin": datetime.strptime(request.form["data_checkin"], "%Y-%m-%d"),
            "data_checkout": datetime.strptime(request.form["data_checkout"], "%Y-%m-%d"),
            "status": request.form["status"],
            "valor_total": float(request.form["valor_total"]),
            "servicos": [],
            "pagamentos": []
        })
        return redirect(url_for("reservas.listar_reservas"))

    hospedes = list(db["hospedes"].find())
    quartos = list(db["quartos"].find())
    funcionarios = list(db["funcionarios"].find())
    return render_template(
        "reserva_form.html",
        hospedes=hospedes,
        quartos=quartos,
        funcionarios=funcionarios
    )


@reservas_bp.route("/reservas/<id>")
def detalhe_reserva(id):
    reserva = db["reservas"].find_one({"_id": ObjectId(id)})
    funcionarios = list(db["funcionarios"].find())
    return render_template("reserva_detalhe.html", reserva=reserva, funcionarios=funcionarios)


@reservas_bp.route("/reservas/excluir/<id>")
def excluir_reserva(id):
    db["reservas"].delete_one({"_id": ObjectId(id)})
    return redirect(url_for("reservas.listar_reservas"))


@reservas_bp.route("/reservas/<id>/servico/novo", methods=["POST"])
def adicionar_servico(id):
    reserva = db["reservas"].find_one({"_id": ObjectId(id)})

    if reserva["status"] == "finalizada":
        return redirect(url_for("reservas.detalhe_reserva", id=id))

    ultimo_id = 0
    if reserva["servicos"]:
        ultimo_id = max(s["id_servico"] for s in reserva["servicos"])

    valor_unitario = float(request.form["valor_unitario"])
    quantidade = int(request.form["quantidade"])
    total_servico = valor_unitario * quantidade

    novo_servico = {
        "id_servico": ultimo_id + 1,
        "descricao": request.form["descricao"],
        "valor_unitario": valor_unitario,
        "quantidade": quantidade,
        "funcionario_id": int(request.form["funcionario_id"])
    }

    novo_valor_total = float(reserva.get("valor_total", 0)) + total_servico

    db["reservas"].update_one(
        {"_id": ObjectId(id)},
        {
            "$push": {"servicos": novo_servico},
            "$set": {"valor_total": novo_valor_total}
        }
    )

    return redirect(url_for("reservas.detalhe_reserva", id=id))


@reservas_bp.route("/reservas/<id>/pagamento/novo", methods=["POST"])
def adicionar_pagamento(id):
    reserva = db["reservas"].find_one({"_id": ObjectId(id)})

    if reserva["status"] != "finalizada":
        return redirect(url_for("reservas.detalhe_reserva", id=id))

    ultimo_id = 0
    if reserva["pagamentos"]:
        ultimo_id = max(p["id_pagamento"] for p in reserva["pagamentos"])

    novo_pagamento = {
        "id_pagamento": ultimo_id + 1,
        "data_pagamento": datetime.now(),
        "valor": float(request.form["valor"]),
        "forma_pagamento": request.form["forma_pagamento"],
        "status": request.form["status"]
    }

    db["reservas"].update_one(
        {"_id": ObjectId(id)},
        {"$push": {"pagamentos": novo_pagamento}}
    )

    return redirect(url_for("reservas.detalhe_reserva", id=id))


@reservas_bp.route("/reservas/<id>/finalizar", methods=["POST"])
def finalizar_reserva(id):
    db["reservas"].update_one(
        {"_id": ObjectId(id)},
        {"$set": {"status": "finalizada"}}
    )
    return redirect(url_for("reservas.detalhe_reserva", id=id))