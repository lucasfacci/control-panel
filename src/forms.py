from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length

class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={'placeholder': 'Usuário'})
    password = PasswordField(validators=[InputRequired(), Length(min=4, max=80)], render_kw={'placeholder': 'Senha'})


class RegisterForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={'placeholder': 'Usuário'})
    password = PasswordField(validators=[InputRequired(), Length(min=4, max=80)], render_kw={'placeholder': 'Senha'})
    password_confirm = PasswordField(validators=[InputRequired(), Length(min=4, max=80)], render_kw={'placeholder': 'Confirme a Senha'})