from db import get_database
from datetime import datetime

def seed():
    db = get_database()

    db["hospedes"].insert_many([
        {"cpf": "12345678900", "nome": "Maria Silva", "telefone": "31999999999", "email": "maria@email.com"},
        {"cpf": "98765432100", "nome": "Carlos Souza", "telefone": "31988888888", "email": "carlos@email.com"}
    ])

    db["quartos"].insert_many([
        {"numero": 101, "tipo": "Suíte", "capacidade": 2, "valor_diaria": 250.00, "status_disponibilidade": "disponivel"},
        {"numero": 102, "tipo": "Standard", "capacidade": 1, "valor_diaria": 150.00, "status_disponibilidade": "disponivel"}
    ])

    db["funcionarios"].insert_many([
        {"id_func": 1, "cpf": "11122233344", "nome": "João Souza", "cargo": "Recepcionista"},
        {"id_func": 2, "cpf": "55566677788", "nome": "Ana Lima", "cargo": "Camareira"}
    ])

    db["reservas"].insert_one({
        "hospede_cpf": "12345678900",
        "quarto_numero": 101,
        "funcionario_id": 1,
        "data_reserva": datetime(2026, 7, 10),
        "data_checkin": datetime(2026, 7, 15),
        "data_checkout": datetime(2026, 7, 20),
        "status": "confirmada",
        "valor_total": 1350.00,
        "servicos": [
            {"id_servico": 1, "descricao": "Lavanderia", "valor_unitario": 30.00, "quantidade": 2, "funcionario_id": 2}
        ],
        "pagamentos": [
            {"id_pagamento": 1, "data_pagamento": datetime(2026, 7, 15), "valor": 700.00, "forma_pagamento": "cartao", "status": "aprovado"}
        ]
    })

    print("Dados de teste inseridos com sucesso.")

if __name__ == "__main__":
    seed()