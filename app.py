from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from models import User, Post, db
from shifr import adfgvx_decrypt, adfgvx_encrypt
import click

app = Flask(__name__)
app.config['SECRET_KEY'] = 'a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
migrate = Migrate(app, db)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

key = b'a1b2c3d4e5f6g7h8'  # Ваш 16-байтный ключ

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Основные маршруты и функции 
@app.context_processor
def utility_processor():
    return dict(decrypt=adfgvx_decrypt)


@app.route('/')
def home():
    if current_user.is_authenticated:
        posts = Post.query.filter_by(user_id=current_user.id).all()

        for post in posts:
            try:
                decrypted_content = adfgvx_decrypt(post.content, key)
                post.content = decrypted_content
            except UnicodeDecodeError as e:
                # Если возникла ошибка, вывести сообщение в лог
                print(f"Ошибка декодирования поста {post.id}: {e}")
                post.content = "Ошибка: не удалось расшифровать контент."
    else:
        posts = []

    return render_template('home.html', posts=posts)

@app.route('/create_post', methods=['GET', 'POST'])
@login_required
def create_post():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        encrypted_content = adfgvx_encrypt(content, key)
        new_post = Post(title=title, content=encrypted_content,
                        user_id=current_user.id)
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('create_post.html')

@app.route('/edit_post/<int:post_id>', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.user_id != current_user.id:
        flash("You can't edit this post")
        return redirect(url_for('home'))
    if request.method == 'POST':
        post.title = request.form.get('title')
        post.content = adfgvx_encrypt(request.form.get('content'), key)
        db.session.commit()
        return redirect(url_for('home'))

    # Передача расшифрованного содержания
    decrypted_content = adfgvx_decrypt(post.content, key)
    return render_template('edit_post.html', post=post, decrypted_content=decrypted_content)


@app.route('/delete_post/<int:post_id>')
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.user_id == current_user.id:
        db.session.delete(post)
        db.session.commit()
    return redirect(url_for('home'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        users = User.query.all()

        for user in users:
            decrypted_username = user.get_username(key)
            if decrypted_username == username and user.check_password(password, key):
                login_user(user)
                return redirect(url_for('home'))
        
        flash('Invalid username or password')
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        telefon = request.form.get('telefon')

        new_user = User()
        new_user.set_username(username, key)
        new_user.set_password(password,  key)
        new_user.set_telefon(telefon, key)

        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
