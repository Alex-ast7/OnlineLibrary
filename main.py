import datetime
import os
from json import dumps
from random import randint

from flask import Flask, render_template, redirect, request, url_for, session

from flask_login import LoginManager, login_user, login_required, logout_user, current_user

from data.user_marks import UserMarks
from data.books import Books
from data.users import User
from data.comments import Comment
from data.user_marks import UserMarks

from forms.user import RegisterForm, LoginForm, EditProfileForm
from forms.comments import AddCommentForm

from data import db_session

from config import secret_admin_password

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'dnuiwy38noqmcxq8yr1FV&^npmNZB6ernm;s,c/'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(days=1)


def info(id):
    db_sess = db_session.create_session()

    book = db_sess.query(Books).filter(Books.id == id).first()
    params = {'title': book.title, 'author': book.author,
              'description': book.description, 'genre': book.genre,
              'language': book.language, 'total_amount': book.total_amount,
              'amount_in_library': book.amount_in_library,
              'image_link': book.image_link}

    marks_info = {'mark_1': False, 'mark_2': False, 'mark_3': False, 'mark_4': False, 'mark_5': False}
    marks = db_sess.query(UserMarks).filter(UserMarks.book_id == id, UserMarks.user == current_user.id).all()
    for i in marks:
        marks_info[f'mark_{i.type}'] = True

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

    return params, data, book_comments, len(book_comments), marks_info


def check_user_authorised():
    if not current_user.is_authenticated:
        session['message'] = 'Зарегистрируйтесь или войдите, чтобы просматривать эту страницу'
        return redirect(url_for('login'))


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/login-register")


@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
    if check_user_authorised():
        return check_user_authorised()
    db_sess = db_session.create_session()
    book = db_sess.query(Books).all()
    data = []
    for i in book:
        if len(i.title) > 13:
            i.title = i.title[0:14] + '...'
        if len(i.author) > 13:
            i.author = i.author[0:14] + '...'
        data.append({'title': i.title, 'author': i.author, 'total_amount': i.total_amount,
                     'amount_in_library': i.amount_in_library, 'image_link': i.image_link})
    print(data)
    return render_template('index.html', data=data, is_find=False)


@app.route('/login-register', methods=['GET', 'POST'])
def login():
    register_form = RegisterForm()
    login_form = LoginForm()
    if register_form.validate_on_submit():
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == register_form.reg_email.data).first():
            return render_template('login-register.html', register_form=register_form, login_form=login_form,
                                   message='Такой пользователь уже есть', form='register')
        user = User(email=register_form.reg_email.data, is_admin=False)
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
    try:
        message = session['message']
        session.pop('message', None)
        return render_template('login-register.html', register_form=register_form, login_form=login_form,
                               message=message)
    except Exception:
        return render_template('login-register.html', register_form=register_form, login_form=login_form)


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    edit_profile_form = EditProfileForm()
    status = {
        'booked_books': 0,
        'read_now_books': 0,
        'read_later_books': 0,
        'read_past_books': 0,
        'dropped_books': 0
    }

    db_sess = db_session.create_session()
    for book in db_sess.query(UserMarks).filter(UserMarks.user == current_user.id).all():
        if int(book.type) == 1:
            status['booked_books'] += 1
        if int(book.type) == 2:
            status['read_now_books'] += 1
        if int(book.type) == 3:
            status['read_later_books'] += 1
        if int(book.type) == 4:
            status['read_past_books'] += 1
        if int(book.type) == 5:
            status['dropped_books'] += 1

    if request.method == 'GET':
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.id == current_user.id).first()

        edit_profile_form.surname.data = user.surname
        edit_profile_form.name.data = user.name
        edit_profile_form.reg_email.data = user.email
        edit_profile_form.phone.data = user.phone
        is_admin = user.is_admin

    if edit_profile_form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.id == current_user.id).first()

        user.surname = edit_profile_form.surname.data
        user.name = edit_profile_form.name.data
        user.email = edit_profile_form.reg_email.data
        user.phone = edit_profile_form.phone.data

        is_admin = user.is_admin

        if edit_profile_form.photo.data:
            edit_profile_form.photo.data.save(f'static/user_data/user_photo/{current_user.id}.bmp')
            user.photo_link = f'static/user_data/user_photo/{current_user.id}.bmp'

        db_sess.commit()

        if edit_profile_form.old_password.data and edit_profile_form.new_password.data:
            if user.check_password(edit_profile_form.old_password.data):
                user.set_password(edit_profile_form.new_password.data)
                db_sess.commit()
            else:
                return render_template('personal_cabinet.html', edit_profile_form=edit_profile_form,
                                       message='Изменения сохранены, но пароль не изменён - старый пароль указан неверно',
                                       is_admin=is_admin)
        elif edit_profile_form.old_password.data and not edit_profile_form.new_password.data:
            return render_template('personal_cabinet.html', edit_profile_form=edit_profile_form,
                                   message='Изменения сохранены, но пароль не изменён. Заполните поле "Новый пароль"',
                                   is_admin=is_admin)
        elif edit_profile_form.new_password.data and not edit_profile_form.old_password.data:
            return render_template('personal_cabinet.html', edit_profile_form=edit_profile_form,
                                   message='Изменения сохранены, но пароль не изменён - для его смены укажите старый пароль',
                                   is_admin=is_admin)

        admin_password = edit_profile_form.admin_password.data
        if admin_password:
            if admin_password == secret_admin_password:
                user.is_admin = True
                db_sess.commit()
                return render_template('personal_cabinet.html', edit_profile_form=edit_profile_form,
                                       message='Изменения сохранены, вам присвоен статус администратора', is_admin=True)
            else:
                return render_template('personal_cabinet.html', edit_profile_form=edit_profile_form,
                                       message='Изменения сохранены, в статусе администратора отказано', is_admin=False)

        return render_template('personal_cabinet.html', edit_profile_form=edit_profile_form,
                               message='Изменения сохранены', is_admin=is_admin)
    return render_template('personal_cabinet.html', status=status, edit_profile_form=edit_profile_form, is_admin=is_admin)


@app.route('/product-details/<int:id>', methods=['GET', 'POST'])
def product(id):
    if check_user_authorised():
        return check_user_authorised()
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

    params, data, book_comments, count, marks_info = info(id)
    form = AddCommentForm()
    return render_template('product-details.html', params=params, data=data, form=form, book_comments=book_comments,
                           count=count, id=id, marks_info=marks_info)


@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == "POST":
        is_find_ok = True
        need_text = request.form['text']
        res = []
        db_sess = db_session.create_session()
        for book in db_sess.query(Books).all():
            if need_text.lower() in book.title.lower() or need_text.lower() in book.author.lower():
                res.append(book)
        data = result_find(res)
        if not (data):
            is_find_ok = False
        return render_template('index.html', data=data, is_find=True, is_find_ok=is_find_ok)


def result_find(res):
    data = []
    for i in res:
        if len(i.title) > 13:
            i.title = i.title[0:14] + '...'
        if len(i.author) > 13:
            i.author = i.author[0:14] + '...'
        data.append({'id': i.id, 'title': i.title, 'author': i.author, 'total_amount': i.total_amount,
                     'amount_in_library': i.amount_in_library, 'image_link': i.image_link})
    print(data)
    return data


@app.route('/add_mark/<int:mark_type>/<int:book_id>')
def add_mark(mark_type, book_id):
    db_sess = db_session.create_session()
    mark = db_sess.query(UserMarks).filter(UserMarks.book_id == book_id, UserMarks.user == current_user.id,
                                           UserMarks.type == mark_type).first()
    book = db_sess.query(Books).filter(Books.id == book_id).first()
    if mark:
        db_sess.delete(mark)
        if mark_type == 1:
            book.amount_in_library += 1
    else:
        if mark_type == 1:
            if book.amount_in_library >= 1:
                mark = UserMarks(type=mark_type, user=current_user.id, book_id=book_id)
                db_sess.add(mark)
                book.amount_in_library -= 1
        else:
            mark = UserMarks(type=mark_type, user=current_user.id, book_id=book_id)
            db_sess.add(mark)
    db_sess.commit()
    return '<script>document.location.href = document.referrer</script>'


if __name__ == '__main__':
    db_session.global_init("db/onlineLibrary.db")
    port = int(os.environ.get("PORT", 5000))

    app.run(host='0.0.0.0', port=port)
