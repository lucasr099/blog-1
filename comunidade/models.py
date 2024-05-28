from comunidade import database, login_manager
from datetime import datetime
from flask_login import UserMixin
from comunidade import bcrypt


@login_manager.user_loader
def load_usuario(id_usuario):
    return Usuario.query.get(int(id_usuario))
                                
                                
                                
class Usuario(database.Model, UserMixin):
    __tablename__ = 'usuarios'
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String(100), nullable=False)
    email = database.Column(database.String(100), nullable=False, unique=True)
    senha = database.Column(database.String(100), nullable=False)
    foto_perfil = database.Column(database.String(100), default='default.jpg')
    posts = database.relationship('Post', backref='autor', lazy=True)
    time_futebol = database.Column(database.String(100), nullable=True, default='Não informou')

    def contar_post(self):
        return len(self.posts)


    

class Post(database.Model):
    __tablename__ = 'posts'
    id = database.Column(database.Integer, primary_key=True)
    titulo = database.Column(database.String(100), nullable=False)
    corpo = database.Column(database.Text, nullable=False)
    data_publicacao = database.Column(database.DateTime, nullable=False, default=datetime.now())
    id_usuario = database.Column(database.Integer, database.ForeignKey('usuarios.id'), nullable=False)