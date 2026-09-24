from flask import Flask, render_template, request, session, redirect, url_for, send_from_directory
from dotenv import load_dotenv
from PIL import Image
import os
from models import db, Usuario, Foto
import uuid


# Formatos de imagem que o site aceita
ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "webp"}

# Tamanho maximo que uma imagem pode ter: 5 MB
MAX_FILE_SIZE = 5 * 1024 * 1024

# Carrega as informaçoes que estao no arquivo .env
load_dotenv()

# Cria a aplicaçao Flask
app = Flask(__name__)

# Configura a pasta onde as imagens enviadas pelos usuarios serao salvas
app.config["UPLOAD_FOLDER"] = "uploads"

# Chave usada pelo Flask para proteger a sessao do usuário
app.secret_key = os.getenv("SECRET_KEY")

# Configura a conexao com o banco de dados PostgreSQL
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


# Conecta o SQLAlchemy com a aplicaçao Flask
db.init_app(app)


# Pagina inicial
@app.route("/")
def index():

    return render_template("index.html")




# Pagina para publicar uma nova memoria
@app.route("/publicar", methods=["GET", "POST"])
def publicar():

    # Verifica se o usuario está logado
    if "usuario_id" not in session:

        return redirect(url_for("criar_conta"))


    # Sa executa essa parte quando o formulario for enviado
    if request.method == "POST":

        # Pega os dados enviados pelo formulario publicar.html
        titulo = request.form.get("titulo")
        ano = request.form.get("ano")
        descricao = request.form.get("descricao")
        foto = request.files.get("foto")


        # Verifica se todos os campos foram preenchidos
        if not titulo or not ano or not descricao or not foto:
            return "Todos os campos são obrigatórios!"


        # Verifica o tamanho do titulo
        if len(titulo) > 100:
            return "O título deve ter no máximo 100 caracteres!"


        # Verifica o tamanho da descrição
        if len(descricao) > 300:
            return "A descrição deve ter no máximo 300 caracteres!"


        # Verifica se o ano e valido
        # O campo pode receber um número ou "outros"
        if ano != "outros":

            try:
                ano = int(ano)

            except ValueError:
                return "Ano inválido!"

        # Pega o nome original do arquivo enviado
        nome_arquivo = foto.filename

        # Pega a extensao do arquivo
        extensao = nome_arquivo.rsplit(".", 1)[-1].lower()

        # Verifica se a extensao esta entre os formatos permitidos
        if extensao not in ALLOWED_EXTENSIONS:
            return "Extensão de arquivo não permitida!"


        # Vai ate o final do arquivo para descobrir o tamanho
        foto.seek(0, 2)

        tamanho = foto.tell()


        # Volta o arquivo para o começo
        # Precisa disso porque ainda vai ler a imagem
        foto.seek(0)


        # Impede o envio de imagens maiores que 5 MB
        if tamanho > MAX_FILE_SIZE:
            return "A imagem deve ter no máximo 5 MB!"

        # Tenta abrir o arquivo como uma imagem
        try:

            imagem = Image.open(foto)

            # Confere se o arquivo realmente possui uma imagem valida
            imagem.verify()

            # volta o arquivo para o começo novamente, porque a função verify() lê o arquivo inteiro
            foto.seek(0)

        except Exception:
            return "Arquivo de imagem inválido!"

        # Gera um nome unico para a imagem
        nome_seguro = f"{uuid.uuid4()}.{extensao}"

        # Salva a imagem na pasta de uploads
        foto.save(os.path.join(app.config["UPLOAD_FOLDER"], nome_seguro))

        # Criar o registro da foto no banco de dados
        nova_foto = Foto(
            usuario_id=session["usuario_id"],
            imagem=nome_seguro,
            titulo=titulo,
            ano=ano,
            descricao=descricao
        )

        # Adiciona a foto ao banco de dados
        db.session.add(nova_foto)
        db.session.commit()

        # Mostra os dados no terminal enquanto estamos testando
        print(f"Título: {titulo}")
        print(f"Ano: {ano}")
        print(f"Descrição: {descricao}")
        print(f"Foto: {foto}")
        print(f"Nome seguro: {nome_seguro}")

    # Mostra a pagina de publicação
    return render_template("publicar.html")


# Pagina de login
@app.route("/login", methods=["GET", "POST"])
def login():

    # Verifica se o formulario foi enviado
    if request.method == "POST":

        # Pega os dados do usuario enviados pelo formulario
        nome_usuario = request.form.get("usuario")
        senha_usuario = request.form.get("senha")

        # Procura no banco um usuario com esse nome
        usuario = Usuario.query.filter_by(usuario=nome_usuario).first()

        # Verifica se o usuario existe e se a senha esta correta
        if usuario and usuario.verificar_senha(senha_usuario):

            # Guarda o ID do usuario na sessao
            session["usuario_id"] = usuario.id
            print("Login bem sucedido")

            return redirect(url_for("index"))

        else:
            print("Erro!")

    return render_template("login.html")

# Pagina para criar uma nova conta
@app.route("/criar-conta", methods=["GET", "POST"])
def criar_conta():

    # Verifica se o formulario foi enviado
    if request.method == "POST":

        # Pega os dados enviados pelo formulario
        nome_usuario = request.form.get("usuario")
        senha_usuario = request.form.get("senha")

        # Cria um novo usuario
        novo_usuario = Usuario(usuario=nome_usuario)

        # Protege a senha antes de salvar no banco
        novo_usuario.definir_senha_hash(senha_usuario)

        # Adiciona o usuario ao banco
        db.session.add(novo_usuario)
        db.session.commit()

        # Já deixa o usuario logado depois do cadastro
        session["usuario_id"] = novo_usuario.id

        return redirect(url_for("index"))

    return render_template("criar-conta.html")


# Encerra a sessao do usuario
@app.route("/logout")
def logout():

    # Remove o usuario da sessao
    session.pop("usuario_id", None)

    return redirect(url_for("index"))


@app.route("/uploads/<nome_arquivo>")
def servir_upload(nome_arquivo):

    print("Tentando abrir:", nome_arquivo)
    print("Pasta:", app.config["UPLOAD_FOLDER"])

    return send_from_directory(
        app.config["UPLOAD_FOLDER"],
        nome_arquivo
    )




# Pagina onde o usuario poderá ver suas proprias fotos
@app.route("/minha-galeria")
def minha_galeria():
    # Verifica se o usuario está logado
    if "usuario_id" not in session:
        return redirect(url_for("login"))

    # Busca todas as fotos do usuario logado no banco de dados
    fotos = Foto.query.filter_by(usuario_id=session["usuario_id"]).all()

    # Renderiza a pagina minha_galeria.html passando as fotos do usuario
    return render_template("minha_galeria.html", fotos=fotos)


@app.route("/excluir_foto/<int:foto_id>", methods=["POST"])
def excluir_foto(foto_id):

    # Verifica se o usuario esta logado
    if "usuario_id" not in session:
        return redirect(url_for("login"))

    # Busca a foto no banco de dados pelo ID e pelo ID do usuario logado
    foto = Foto.query.filter_by(id=foto_id, usuario_id=session["usuario_id"]).first()

    # Verifica se a foto existe e pertence ao usuario logado
    if not foto:
        return redirect(url_for("minha_galeria"))

    # Remove a foto do banco de dados
    caminho = os.path.join(app.config["UPLOAD_FOLDER"], foto.imagem)

    # Verifica se o arquivo existe antes de tentar remove-lo
    if os.path.exists(caminho):
        os.remove(caminho)

    # Remove a foto do banco de dados
    db.session.delete(foto)
    db.session.commit()

    return redirect(url_for("minha_galeria"))



# Cria as tabelas no banco caso elas ainda nao existam
with app.app_context():
    db.create_all()

# Inicia o servidor Flask
if __name__ == "__main__":
    app.run(debug=True)