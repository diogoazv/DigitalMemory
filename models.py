from flask_sqlalchemy import SQLAlchemy

# Funcoes de seguranca do werkzeug para proteger a senha do usuario
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class Usuario(db.Model):
    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(50), unique=True, nullable=False)
    senha = db.Column(db.String(255), nullable=False)

    # Metodo hash para proteger a senha do usuario antes de salvar no banco
    def definir_senha_hash(self, senha):
        self.senha = generate_password_hash(senha)

    # Metodo para verificar a senha do usuario corresponde ao hash salvo
    def verificar_senha(self, senha):
        return check_password_hash(self.senha, senha)