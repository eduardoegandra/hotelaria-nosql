# Sistema para Gerenciamento de Operações Hoteleiras

Sistema para gerenciamento integrado das operações internas de um hotel, controlando quartos, hóspedes, reservas, funcionários, serviços adicionais e pagamentos.

## Sobre o Projeto

O sistema permite que a equipe do hotel registre reservas, controle a disponibilidade de quartos, gerencie serviços extras (lavanderia, room service) executados por funcionários e registre pagamentos associados a cada reserva. O projeto foi desenvolvido como Projeto Prático da disciplina CSI603 - Banco de Dados II (UFOP).

## Tecnologias Utilizadas

- **Linguagem**: Python 3.11
- **Framework Web**: Flask
- **SGBD**: MongoDB (NoSQL, orientado a documentos)
- **Driver de Conexão**: PyMongo (driver oficial, sem uso de ORM)

## Estrutura do Projeto
hotelaria-nosql/
├── app.py
├── db.py
├── criar_colecoes.py
├── seed.py
├── hospedes.py
├── quartos.py
├── funcionarios.py
├── reservas.py
├── requirements.txt
├── static/
│ └── style.css
└── templates/
├── base.html
├── index.html
├── hospedes.html
├── hospede_form.html
├── quartos.html
├── quarto_form.html
├── funcionarios.html
├── funcionario_form.html
├── reservas.html
├── reserva_form.html
└── reserva_detalhe.html


## Modelagem de Dados

O banco de dados utiliza 4 coleções: `hospedes`, `quartos`, `funcionarios` e `reservas`. A coleção `reservas` concentra os dados centrais do sistema, com **serviços** e **pagamentos** embutidos como arrays de sub-documentos, enquanto **hóspede**, **quarto** e **funcionário** são referenciados por seus identificadores (cpf, numero, id_func) para evitar duplicação de dados cadastrais.

## Instalação e Execução

### Pré-requisitos

- Python 3.11 ou superior
- MongoDB instalado localmente (ou MongoDB Atlas configurado)

### Passos

1. Clone o repositório:

```bash
git clone <url-do-repositorio>
cd hotelaria-nosql
```

2. Instale as dependências:

```bash
pip install -r requirements.txt
```

3. Certifique-se de que o MongoDB está rodando em `localhost:27017` (ou ajuste a connection string em `db.py` para usar MongoDB Atlas).

4. Crie as coleções e índices:

```bash
python criar_colecoes.py
```

5. Insira os dados de teste (opcional):

```bash
python seed.py
```

6. Inicie a aplicação:

```bash
python app.py
```

7. Acesse no navegador:
http://127.0.0.1:5000


## Funcionalidades

- Cadastro, edição, listagem e exclusão de hóspedes
- Cadastro, edição, listagem e exclusão de quartos
- Cadastro, edição, listagem e exclusão de funcionários
- Criação e exclusão de reservas, com adição de serviços e pagamentos vinculados

## Autor

[Seu nome completo] - Matrícula: [sua matrícula]  
Sistemas de Informação - UFOP  
Disciplina: CSI603 - Banco de Dados II
