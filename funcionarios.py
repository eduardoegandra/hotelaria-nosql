from flask import Blueprint, render_template, request, redirect, url_for
from db import get_database
from bson.objectid import ObjectId

funcionarios_bp = Blueprint("funcionarios", __name__)
db = get_database()

@funcionarios_bp.route("/funcionarios")
def listar_funcionarios():
    funcionarios = list(db["funcionarios"].find())
    return render_template("funcionarios.html", funcionarios=funcionarios)

@funcionarios_bp.route("/funcionarios/novo", methods=["GET", "POST"])
def novo_funcionario():
    if request.method == "POST":
        ultimo = db["funcionarios"].find_one(sort=[("id_func", -1)])
        proximo_id = (ultimo["id_func"] + 1) if ultimo else 1

        db["funcionarios"].insert_one({
            "id_func": proximo_id,
            "cpf": request.form["cpf"],
            "nome": request.form["nome"],
            "cargo": request.form["cargo"]
        })
        return redirect(url_for("funcionarios.listar_funcionarios"))
    return render_template("funcionario_form.html", funcionario=None)

@funcionarios_bp.route("/funcionarios/editar/<id>", methods=["GET", "POST"])
def editar_funcionario(id):
    if request.method == "POST":
        db["funcionarios"].update_one(
            {"_id": ObjectId(id)},
            {"$set": {
                "cpf": request.form["cpf"],
                "nome": request.form["nome"],
                "cargo": request.form["cargo"]
            }}
        )
        return redirect(url_for("funcionarios.listar_funcionarios"))
    funcionario = db["funcionarios"].find_one({"_id": ObjectId(id)})
    return render_template("funcionario_form.html", funcionario=funcionario)

@funcionarios_bp.route("/funcionarios/excluir/<id>")
def excluir_funcionario(id):
    db["funcionarios"].delete_one({"_id": ObjectId(id)})
    return redirect(url_for("funcionarios.listar_funcionarios"))