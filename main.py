import datetime
import os

from flask import Flask, render_template, redirect, request

from flask_login import LoginManager, login_user, login_required, logout_user, current_user

from data.books import Books
from data.users import User
from data.comments import Comment
from data.user_marks import UserMarks
from PIL import Image

from forms.user import RegisterForm, LoginForm, EditProfileForm
from forms.comments import AddCommentForm

from data import db_session


app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'dnuiwy38noqmcxq8yr1FV&^npmNZB6ernm;s,c/'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000


def info(id):
    db_sess = db_session.create_session()

    book = db_sess.query(Books).filter(Books.id == id).first()
    params = {'title': book.title, 'author': book.author,
              'description': book.description, 'genre': book.genre,
              'language': book.language, 'total_amount': book.total_amount,
              'amount_in_library': book.amount_in_library,
              'image_link': book.image_link}

    book = db_sess.query(Books).all()
    data = []
    for i in book:
        if len(i.title) > 13:
            i.title = i.title[0:14] + '...'
        if len(i.author) > 13:
            i.author = i.author[0:14] + '...'
        data.append({'title': i.title, 'author': i.author,
                     'total_amount': i.total_amount,
                     'amount_in_library': i.amount_in_library,
                     'image_link': i.image_link})
    book_comments = []
    db_sess = db_session.create_session()
    for comment in db_sess.query(Comment).filter(Comment.book_id == id).all():
        for user in db_sess.query(User).filter(User.id == comment.user).all():
            book_comments.append([comment.text, comment.date_time, comment.stars, user.name, user.surname])

    return params, data, book_comments, len(book_comments)


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
    db_sess = db_session.create_session()
    book = db_sess.query(Books).all()
    data = []
    for i in book:
        if len(i.title) > 13:
            i.title = i.title[0:14] + '...'
        if len(i.author) > 13:
            i.author = i.author[0:14] + '...'
        data.append({'title': i.title, 'author': i.author, 'total_amount': i.total_amount, 'amount_in_library': i.amount_in_library, 'image_link': i.image_link})
    return render_template('index.html', data=data)


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

        if edit_profile_form.photo.data:
            edit_profile_form.photo.data.save(f'user_data/user_photo/{current_user.id}.bmp')
            user.photo_link = f'user_data/user_photo/{current_user.id}.bmp'

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


@app.route('/product-details/<int:id>', methods=['GET', 'POST'])
def product(id):
    db_sess = db_session.create_session()
    if request.method == 'POST':
        form = AddCommentForm()
        comment = Comment()
        comment.text = form.text.data
        comment.user = current_user.id
        if form.star1.data:
            comment.stars = 5
        elif form.star2.data:
            comment.stars = 4
        elif form.star3.data:
            comment.stars = 3
        elif form.star4.data:
            comment.stars = 2
        elif form.star5.data:
            comment.stars = 1
        comment.book_id = id
        db_sess.add(comment)
        db_sess.commit()
        return redirect(f'/product-details/{id}')

    params, data, book_comments, count = info(id)
    form = AddCommentForm()
    return render_template('product-details.html', params=params, data=data, form=form, book_comments=book_comments, count=count)


if __name__ == '__main__':
    db_session.global_init("db/onlineLibrary.db")
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
