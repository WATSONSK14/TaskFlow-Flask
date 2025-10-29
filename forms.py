from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, EmailField
from wtforms.validators import DataRequired, Email, Length, EqualTo

class RegisterForm(FlaskForm):
    email = EmailField('Email', validators=[
        DataRequired(message="Bu alan boş bırakılamaz"),
        Email(message="Lütfen geçerli bir email adresi girin")
    ])
    password = PasswordField('Password', validators=[
        DataRequired("Bu alan boş bırakılamaz"),
        Length(min=6, max=30, message="Minimum 6 Maximum 30 Digits")
    ])
    password_confirm = PasswordField('Password Confirm', validators=[
        DataRequired("Bu alan boş bırakılamaz"),
        EqualTo('password',message="Şifreler Eşleşmiyor")
    ])
    submit = SubmitField(label="Register")

class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[
        DataRequired(message="Bu alan boş bırakılamaz"),
        Email(message="Lütfen geçerli bir email adresi girin")
    ])
    password = PasswordField('Password', validators=[
        DataRequired("Bu alan boş bırakılamaz"),
        Length(min=6, max=30, message="Minimum 6 Maximum 30 Digits")
    ])
    submit = SubmitField(label="Login")