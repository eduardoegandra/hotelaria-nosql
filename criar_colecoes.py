from db import get_database

def criar_colecoes():
    db = get_database()

    colecoes = ["hospedes", "quartos", "funcionarios", "reservas"]
    for nome in colecoes:
        if nome not in db.list_collection_names():
            db.create_collection(nome)
            print(f"Coleção '{nome}' criada.")
        else:
            print(f"Coleção '{nome}' já existe.")

    db["hospedes"].create_index("cpf", unique=True)
    db["funcionarios"].create_index("id_func", unique=True)
    db["quartos"].create_index("numero", unique=True)
    db["reservas"].create_index([("hospede_cpf", 1), ("quarto_numero    ", 1)])

    print("Índices criados com sucesso.")

if __name__ == "__main__":
    criar_colecoes()