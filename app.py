from credentials import *
from flask import Flask, render_template, redirect, url_for
from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SECRET_KEY'] = SECRET_KEY
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)


class SimpleForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={'placeholder': 'Usuário'})
    password = PasswordField(validators=[InputRequired(), Length(min=4, max=80)], render_kw={'placeholder': 'Senha'})


@app.route('/login', methods=['GET', 'POST'])
def login():
    logout_user()
    form = SimpleForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
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


with app.app_context():
    db.create_all()