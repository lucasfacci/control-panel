from flask import request, render_template, redirect, url_for
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash

from app import app, db
from .forms import LoginForm, RegisterForm
from .models import User

@app.route('/login', methods=['GET', 'POST'])
def login():
    logout_user()
    form = LoginForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user and check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('index'))
            else:
                return render_template("login.html", form=form, message='Usuário e/ou senha inválidos(as)!')
                
    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
@login_required
def register():
    form = RegisterForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            if form.password.data == form.password_confirm.data:
                db.session.add(User(username=form.username.data, password=generate_password_hash(form.password.data)))
                db.session.commit()
                return render_template('register.html', form=form, success_message='Usuário criado com sucesso!')
            else:
                return render_template("register.html", form=form, error_message='As senhas não correspondem!')
    
    return render_template('register.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/')
@login_required
def index():
    return render_template('index.html')


@app.route('/users')
@login_required
def users():
    return render_template('users.html')