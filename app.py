from flask import Flask, render_template
from db import get_database
from hospedes import hospedes_bp
from quartos import quartos_bp
from funcionarios import funcionarios_bp
from reservas import reservas_bp


app = Flask(__name__)
db = get_database()

app.register_blueprint(hospedes_bp)
app.register_blueprint(quartos_bp)
app.register_blueprint(funcionarios_bp)
app.register_blueprint(reservas_bp)

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)