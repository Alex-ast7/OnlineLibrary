import os

from flask import Flask, render_template, redirect, request

from flask_login import LoginManager, login_user, login_required, logout_user, current_user

from data.books import Books
from data.users import User
from data.comments import Comment
from data.user_marks import UserMarks

from forms.user import RegisterForm, LoginForm, EditProfileForm

from data import db_session


app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'dnuiwy38noqmcxq8yr1FV&^npmNZB6ernm;s,c/'


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/login-register', methods=['GET', 'POST'])
def login():
    register_form = RegisterForm()
    login_form = LoginForm()
    if register_form.validate_on_submit():
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == register_form.reg_email.data).first():
            return render_template('login-register.html', register_form=register_form, login_form=login_form,
                                   message='Такой пользователь уже есть', form='register')
        user = User(email=register_form.reg_email.data)
        name_surname = register_form.surname_and_name.data.split()
        if len(name_surname) >= 2:
            user.surname = name_surname[0]
            user.name = ' '.join(name_surname[1:])
        elif len(name_surname) < 2:
            user.name = name_surname[0]
        user.set_password(register_form.reg_password.data)
        db_sess.add(user)
        db_sess.commit()
        user = db_sess.query(User).filter(User.email == register_form.reg_email.data).first()
        login_user(user)
        return redirect('/')
    elif login_form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == login_form.email.data).first()
        if user and user.check_password(login_form.password.data):
            login_user(user)
            return redirect("/")
        return render_template('login-register.html', register_form=register_form, login_form=login_form,
                               message='Неверный логин или пароль', form='login')
    return render_template('login-register.html', register_form=register_form, login_form=login_form)


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    edit_profile_form = EditProfileForm()

    if request.method == 'GET':
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.id == current_user.id).first()

        edit_profile_form.surname.data = user.surname
        edit_profile_form.name.data = user.name
        edit_profile_form.reg_email.data = user.email
        edit_profile_form.phone.data = user.phone

    if edit_profile_form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.id == current_user.id).first()

        user.surname = edit_profile_form.surname.data
        user.name = edit_profile_form.name.data
        user.email = edit_profile_form.reg_email.data
        user.phone = edit_profile_form.phone.data

        db_sess.commit()

        if edit_profile_form.old_password.data and edit_profile_form.new_password.data:
            if user.check_password(edit_profile_form.old_password.data):
                user.set_password(edit_profile_form.new_password.data)
                db_sess.commit()
            else:
                return render_template('personal_cabinet.html', edit_profile_form=edit_profile_form,
                                       message='Изменения сохранены, но пароль не изменён - старый пароль указан неверно')
        elif edit_profile_form.old_password.data and not edit_profile_form.new_password.data:
            return render_template('personal_cabinet.html', edit_profile_form=edit_profile_form,
                                   message='Изменения сохранены, но пароль не изменён. Заполните поле "Новый пароль"')
        elif edit_profile_form.new_password.data and not edit_profile_form.old_password.data:
            return render_template('personal_cabinet.html', edit_profile_form=edit_profile_form,
                                   message='Изменения сохранены, но пароль не изменён - для его смены укажите старый пароль')

        return render_template('personal_cabinet.html', edit_profile_form=edit_profile_form,
                               message='Изменения сохранены')
    return render_template('personal_cabinet.html', edit_profile_form=edit_profile_form)


@app.route('/product-details/<int:id>')
def product(id):
    db_sess = db_session.create_session()
    book = db_sess.query(Books).filter(Books.id == id).first()
    data = {'title': book.title, 'author': book.author, 'description': book.description, 'genre': book.genre, 'language': book.language, 'total_amount': book.total_amount, 'amount_in_library': book.amount_in_library}
    return render_template('product-details.html', params=data)


if __name__ == '__main__':
    db_session.global_init("db/onlineLibrary.db")
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
