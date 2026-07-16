from flask import Blueprint, render_template, request, redirect, url_for
from db import get_database
from bson.objectid import ObjectId

quartos_bp = Blueprint("quartos", __name__)
db = get_database()

@quartos_bp.route("/quartos")
def listar_quartos():
    quartos = list(db["quartos"].find())
    return render_template("quartos.html", quartos=quartos)

@quartos_bp.route("/quartos/novo", methods=["GET", "POST"])
def novo_quarto():
    if request.method == "POST":
        db["quartos"].insert_one({
            "numero": int(request.form["numero"]),
            "tipo": request.form["tipo"],
            "capacidade": int(request.form["capacidade"]),
            "valor_diaria": float(request.form["valor_diaria"]),
            "status_disponibilidade": request.form["status_disponibilidade"]
        })
        return redirect(url_for("quartos.listar_quartos"))
    return render_template("quarto_form.html", quarto=None)

@quartos_bp.route("/quartos/editar/<id>", methods=["GET", "POST"])
def editar_quarto(id):
    if request.method == "POST":
        db["quartos"].update_one(
            {"_id": ObjectId(id)},
            {"$set": {
                "numero": int(request.form["numero"]),
                "tipo": request.form["tipo"],
                "capacidade": int(request.form["capacidade"]),
                "valor_diaria": float(request.form["valor_diaria"]),
                "status_disponibilidade": request.form["status_disponibilidade"]
            }}
        )
        return redirect(url_for("quartos.listar_quartos"))
    quarto = db["quartos"].find_one({"_id": ObjectId(id)})
    return render_template("quarto_form.html", quarto=quarto)

@quartos_bp.route("/quartos/excluir/<id>")
def excluir_quarto(id):
    db["quartos"].delete_one({"_id": ObjectId(id)})
    return redirect(url_for("quartos.listar_quartos"))