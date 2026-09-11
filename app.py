from flask import Flask, render_template, request, session, redirect, url_for
from dotenv import load_dotenv
import os

from models import db, Usuario

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        # Pega os dados do usuario do formulario login.html
        nome_usuario = request.form.get("usuario")
        senha_usuario = request.form.get("senha")

        # Faça uma consulta no banco (query)
        # Filtra pelos criterios informados (filter_by)
        # Pega o primeiro resultado encontrado (first)
        usuario = Usuario.query.filter_by(usuario=nome_usuario).first()

        if usuario and usuario.verificar_senha(senha_usuario):
            session["usuario_id"] = usuario.id
            print("Login bem sucedido")
            return redirect(url_for("index"))
        else:
            print("Erro!")

    return render_template("login.html")

    


@app.route("/criar-conta", methods=["GET", "POST"])
def criar_conta():
    if request.method == "POST":
        #Pega os dados do usuario do formulario criar-conta.html
        nome_usuario = request.form.get("usuario")
        senha_usuario = request.form.get("senha")

        #Cria um novo usuario e salva no banco de dados
        novo_usuario = Usuario(usuario=nome_usuario)


        # Define a senha do usuario usando o metodo definir_senha_hash da classe Usuario
        novo_usuario.definir_senha_hash(senha_usuario)

        db.session.add(novo_usuario)
        db.session.commit()

        session["usuario_id"] = novo_usuario.id
        return redirect(url_for("index"))
    
    return render_template("criar-conta.html")


@app.route("/logout")
def logout():
    # Remove o usuario da sessao
    session.pop("usuario_id", None)

    return redirect(url_for("index"))



@app.route("/minha-galeria")
def minha_galeria():
    return "Minha galeria de fotos"





# Cria as tabelas no banco de dados se elas nao existirem
with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(debug=True)