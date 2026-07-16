from flask import Blueprint, render_template, request, redirect, url_for
from db import get_database
from bson.objectid import ObjectId

hospedes_bp = Blueprint("hospedes", __name__)
db = get_database()

@hospedes_bp.route("/hospedes")
def listar_hospedes():
    hospedes = list(db["hospedes"].find())
    return render_template("hospedes.html", hospedes=hospedes)

@hospedes_bp.route("/hospedes/novo", methods=["GET", "POST"])
def novo_hospede():
    if request.method == "POST":
        db["hospedes"].insert_one({
            "cpf": request.form["cpf"],
            "nome": request.form["nome"],
            "telefone": request.form["telefone"],
            "email": request.form["email"]
        })
        return redirect(url_for("hospedes.listar_hospedes"))
    return render_template("hospede_form.html", hospede=None)

@hospedes_bp.route("/hospedes/editar/<id>", methods=["GET", "POST"])
def editar_hospede(id):
    if request.method == "POST":
        db["hospedes"].update_one(
            {"_id": ObjectId(id)},
            {"$set": {
                "cpf": request.form["cpf"],
                "nome": request.form["nome"],
                "telefone": request.form["telefone"],
                "email": request.form["email"]
            }}
        )
        return redirect(url_for("hospedes.listar_hospedes"))
    hospede = db["hospedes"].find_one({"_id": ObjectId(id)})
    return render_template("hospede_form.html", hospede=hospede)

@hospedes_bp.route("/hospedes/excluir/<id>")
def excluir_hospede(id):
    db["hospedes"].delete_one({"_id": ObjectId(id)})
    return redirect(url_for("hospedes.listar_hospedes"))