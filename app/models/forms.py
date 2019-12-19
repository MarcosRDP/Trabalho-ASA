from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, IntegerField, SelectField
from wtforms.validators import DataRequired, InputRequired, Email, Length
from models.dbutils import DbUtils


class loginForm(FlaskForm):
    username = StringField("username", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])
    remember_me = BooleanField("remember_me")

class registerFormProf(FlaskForm):
    username = StringField("username", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])
    afiliacao = StringField('afiliacao', validators=[InputRequired()]) 
    email = StringField('email', validators=[InputRequired()])

class registerFormMateria(FlaskForm):
    nomeMateria = StringField("nomeMateria", validators=[DataRequired()])
    nomeProfessor = SelectField("nomeProfessor", choices=[])

class registerFormAluno(FlaskForm):
    username = StringField("username", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])
    curso = StringField('curso', validators=[InputRequired()])
    email = StringField('email', validators=[InputRequired()])

class matriculaMateria(FlaskForm):
    nome = StringField("nome", validators=[DataRequired()])

class SelectTable(FlaskForm):
    nome = StringField("nome", validators=[DataRequired()])