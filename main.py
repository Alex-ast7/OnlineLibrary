import os

from flask import Flask, render_template, redirect

from flask_login import LoginManager, login_user, login_required, logout_user, current_user

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


if __name__ == '__main__':
    db_session.global_init("db/onlineLibrary.db")
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
