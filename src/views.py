from flask import render_template, redirect, url_for
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash

from app import app, db
from .forms import SimpleForm
from .models import User

@app.route('/login', methods=['GET', 'POST'])
def login():
    logout_user()
    form = SimpleForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('index'))
        else:
            error_message = 'Usuário e/ou senha inválidos(as)!'
            return render_template("login.html",form=form, message=error_message)
                
    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
@login_required
def register():
    form = SimpleForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        db.session.add(User(username=form.username.data, password=hashed_password))
        db.session.commit()
        message = 'Usuário criado com sucesso!'
        return render_template('register.html', message=message)
    
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