from flask import Blueprint, render_template, request, redirect, url_for
from db import get_database
from bson.objectid import ObjectId
from bson.errors import InvalidId
from datetime import datetime

reservas_bp = Blueprint("reservas", __name__)
db = get_database()

SERVICOS_PREDEFINIDOS = [
    {"nome": "Lavanderia", "valor": 30.00},
    {"nome": "Serviço de Quarto", "valor": 45.00},
    {"nome": "Café da Manhã no Quarto", "valor": 35.00},
    {"nome": "Frigobar - Água", "valor": 6.00},
    {"nome": "Frigobar - Refrigerante", "valor": 8.00},
    {"nome": "Frigobar - Suco", "valor": 9.00},
    {"nome": "Frigobar - Chocolate", "valor": 12.00},
    {"nome": "Frigobar - Bala", "valor": 10.00},
    {"nome": "Limpeza Extra", "valor": 25.00},
    {"nome": "Passadoria", "valor": 20.00},
    {"nome": "Transfer", "valor": 80.00},
    {"nome": "Estacionamento", "valor": 20.00}
]


@reservas_bp.route("/reservas")
def listar_reservas():
    busca = request.args.get("busca", "").strip()
    query = {}

    if busca:
        hospedes_encontrados = list(db["hospedes"].find({
            "nome": {"$regex": busca, "$options": "i"}
        }))

        cpfs_encontrados = [h["cpf"] for h in hospedes_encontrados]

        or_filters = [
            {"hospede_cpf": {"$regex": busca, "$options": "i"}},
            {"quarto_numero": int(busca)} if busca.isdigit() else None,
            {"hospede_cpf": {"$in": cpfs_encontrados}} if cpfs_encontrados else None
        ]

        try:
            or_filters.append({"_id": ObjectId(busca)})
        except InvalidId:
            pass

        filtros_validos = [f for f in or_filters if f is not None]
        if filtros_validos:
            query = {"$or": filtros_validos}

    reservas = list(db["reservas"].find(query))

    for reserva in reservas:
        hospede = db["hospedes"].find_one({"cpf": reserva["hospede_cpf"]})
        reserva["hospede_nome"] = hospede["nome"] if hospede else "Não encontrado"

    return render_template("reservas.html", reservas=reservas, busca=busca)


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
    try:
        reserva = db["reservas"].find_one({"_id": ObjectId(id)})
    except InvalidId:
        return redirect(url_for("reservas.listar_reservas"))

    if not reserva:
        return redirect(url_for("reservas.listar_reservas"))

    funcionarios = list(db["funcionarios"].find())

    return render_template(
        "reserva_detalhe.html",
        reserva=reserva,
        funcionarios=funcionarios,
        servicos_predefinidos=SERVICOS_PREDEFINIDOS
    )


@reservas_bp.route("/reservas/excluir/<id>")
def excluir_reserva(id):
    try:
        db["reservas"].delete_one({"_id": ObjectId(id)})
    except InvalidId:
        pass

    return redirect(url_for("reservas.listar_reservas"))


@reservas_bp.route("/reservas/<id>/servico/novo", methods=["POST"])
def adicionar_servico(id):
    try:
        reserva = db["reservas"].find_one({"_id": ObjectId(id)})
    except InvalidId:
        return redirect(url_for("reservas.listar_reservas"))

    if not reserva:
        return redirect(url_for("reservas.listar_reservas"))

    if reserva["status"] == "finalizada":
        return redirect(url_for("reservas.detalhe_reserva", id=id))

    ultimo_id = 0
    if reserva["servicos"]:
        ultimo_id = max(s["id_servico"] for s in reserva["servicos"])

    descricao = request.form["descricao"]
    valor_unitario = float(request.form["valor_unitario"])
    quantidade = int(request.form["quantidade"])
    total_servico = valor_unitario * quantidade

    novo_servico = {
        "id_servico": ultimo_id + 1,
        "descricao": descricao,
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
    try:
        reserva = db["reservas"].find_one({"_id": ObjectId(id)})
    except InvalidId:
        return redirect(url_for("reservas.listar_reservas"))

    if not reserva:
        return redirect(url_for("reservas.listar_reservas"))

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
    try:
        reserva = db["reservas"].find_one({"_id": ObjectId(id)})
    except InvalidId:
        return redirect(url_for("reservas.listar_reservas"))

    if not reserva:
        return redirect(url_for("reservas.listar_reservas"))

    db["reservas"].update_one(
        {"_id": ObjectId(id)},
        {"$set": {"status": "finalizada"}}
    )

    return redirect(url_for("reservas.detalhe_reserva", id=id))