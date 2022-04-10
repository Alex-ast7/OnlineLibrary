import os

from flask import Flask, render_template, redirect

from flask_login import LoginManager, login_user, login_required, logout_user, current_user

from data.books import Books
from data.users import User
from data.comments import Comment
from data.user_marks import UserMarks

from forms.user import RegisterForm, LoginForm

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


@app.route('/blog')
def blog():
    return render_template('blog.html')


@app.route('/login-register', methods=['GET', 'POST'])
def login():
    register_form = RegisterForm()
    login_form = LoginForm()
    if register_form.validate_on_submit():
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == register_form.reg_email.data).first():
            return render_template('login-register.html', register_form=register_form, login_form=login_form,
                                   message='Такой пользователь уже есть')
        user = User(
            surname=register_form.surname_and_name.data.split()[0],
            name=register_form.surname_and_name.data.split()[1],
            email=register_form.reg_email.data,
        )
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
                               message='Неверный логин или пароль')
    return render_template('login-register.html', register_form=register_form, login_form=login_form)


@app.route('/product-details')
def product():
    return render_template('product-details.html')


if __name__ == '__main__':
    db_session.global_init("db/onlineLibrary.db")
    db_sess = db_session.create_session()
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
