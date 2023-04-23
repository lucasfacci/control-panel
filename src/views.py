from flask import abort, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

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
            if User.query.filter_by(username=form.username.data).first():
                return render_template('register.html', form=form, error_message='Este nome de usuário já existe!')
            elif form.password.data == form.password_confirm.data:
                db.session.add(User(username=form.username.data, password=generate_password_hash(form.password.data), is_admin=form.is_admin.data))
                db.session.commit()
                form.username.data = ''
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


@app.route('/admin')
@login_required
def admin():
    if current_user.is_admin:
        return render_template('admin.html')
    else:
        abort(404)


@app.route('/users', defaults={'user_id': None})
@app.route('/users/<int:user_id>', methods=['GET', 'POST'])
@login_required
def users(user_id):
    if current_user.is_admin:
        if request.form.get('_method') == 'DELETE':
            user = User.query.get(user_id)
            db.session.delete(user)
            db.session.commit()
            return redirect(url_for('users'))
        users = User.query.all()
        return render_template('users.html', users=users)
    else:
        abort(404)