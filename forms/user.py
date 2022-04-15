from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField, FileField
from wtforms.validators import DataRequired, EqualTo


class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(message='Это поле обязательное')])
    password = PasswordField('Пароль', validators=[DataRequired(message='Это поле обязательное')])
    submit = SubmitField('Вход')


class RegisterForm(FlaskForm):
    surname_and_name = StringField('Фамилия и имя', validators=[DataRequired(message='Это поле обязательное')])
    reg_email = EmailField('Email', validators=[DataRequired(message='Это поле обязательное')])
    reg_password = PasswordField('Пароль', validators=[DataRequired(message='Это поле обязательное')])
    repeat_password = PasswordField('Повторите пароль',
                                    validators=[DataRequired(message='Это поле обязательное'),
                                                EqualTo('reg_password', message='Пароли не совпадают')])
    reg_submit = SubmitField('Регистрация')


class EditProfileForm(FlaskForm):
    photo = FileField('Выберите файл')
    surname = StringField('Фамилия', validators=[DataRequired(message='Это поле обязательное')])
    name = StringField('Имя', validators=[DataRequired(message='Это поле обязательное')])
    reg_email = EmailField('Email', validators=[DataRequired(message='Это поле обязательное')])
    phone = StringField('Номер телефона', validators=[])
    old_password = PasswordField('Старый пароль', validators=[])
    new_password = PasswordField('Новый пароль', validators=[])
    reg_submit = SubmitField('Сохранить')
