from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from shifr import adfgvx_decrypt, adfgvx_encrypt
db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)  # Зашифрованное имя пользователя
    password = db.Column(db.String(255), nullable=False)  # Зашифрованный пароль
    telefon = db.Column(db.String(255), unique=True, nullable=False)  # Зашифрованный telefon
    posts = db.relationship('Post', backref='author', lazy=True)

    def set_password(self, password, key):
        self.password = adfgvx_encrypt(password, key)

    def check_password(self, password, key):
        decrypted_password = adfgvx_decrypt(self.password, key)
        return decrypted_password == password

    def set_username(self, username, key):
        self.username = adfgvx_encrypt(username, key)

    def get_username(self, key):
        return adfgvx_decrypt(self.username, key)

    def set_telefon(self, telefon, key):
        self.telefon = adfgvx_encrypt(telefon, key)

    def get_telefon(self, key):
        return adfgvx_decrypt(self.telefon, key)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    content = db.Column(db.String(255), nullable=False)  # Хранение шифрованного контента
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def set_content(self, content, key):
        self.content = adfgvx_encrypt(content, key)

    def get_content(self, content, key):
        self.content = adfgvx_decrypt(content, key)