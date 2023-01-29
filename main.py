import configparser
import os

from flask import Flask, render_template, request
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from werkzeug.security import check_password_hash
from werkzeug.utils import redirect

from Forms.user import RegisterForm, LoginForm
from data import db_session
from data.users import User

DATABASE_PATH = "db/main.db"

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = \
    "njosadiojphadohpjsadohkpsaodjksaojpdhnojphhojpsSOJPHjoppo"


def init_db():
    db_session.global_init(DATABASE_PATH)


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect("/")


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route("/")
def index():
    return render_template("index.html", anonymous=current_user.is_anonymous,
                           c_user=current_user, title="Borsody Auction House", page_type="main.db-page", footer=True)


@app.route("/about")
def about_author():
    return render_template("about.html", anonymous=current_user.is_anonymous,
                           c_user=current_user, page_type="main.db-page", title="About author", footer=False)


@app.route("/registration", methods=['GET', 'POST'])
def registration():
    title = "Registration"
    form_registration = RegisterForm()

    if form_registration.validate_on_submit():
        if is_user_in_database(form_registration.email.data):
            return render_template('registration.html', anonymous=current_user.is_anonymous, c_user=current_user,
                                   title=title, form=form_registration, message="This user already exists", footer=True,
                                   page_type="page")

        add_user(form_registration.name.data, form_registration.email.data, form_registration.password.data)

        return redirect('/login')
    return render_template('registration.html', anonymous=current_user.is_anonymous,
                           c_user=current_user, title=title, form=form_registration, footer=True, page_type="page")


@app.route("/login", methods=['GET', 'POST'])
def login():
    db_sess = db_session.create_session()
    title = "Login"
    form_login = LoginForm()
    if form_login.email.data and form_login.password.data:
        user = db_sess.query(User).filter(User.email == form_login.email.data).first()

        if not user:
            # not in database
            return render_template('login.html', anonymous=current_user.is_anonymous,
                                   c_user=current_user, title=title, form=form_login,
                                   message="There is no such user", footer=True, page_type="page")

        elif not check_password_hash(user.hashed_password, form_login.password.data):
            return render_template('login.html', anonymous=current_user.is_anonymous,
                                   c_user=current_user, title=title, form=form_login, message="Wrong password",
                                   footer=True, page_type="page")

        else:
            login_user(user)
            print(login_user(user))
            return redirect('/')  # OK
    return render_template('login.html', anonymous=current_user.is_anonymous,
                           c_user=current_user, title=title, form=form_login, message='', page_type="page", footer=True)


def is_user_in_database(email):
    db_sess = db_session.create_session()
    return db_sess.query(User).filter(User.email == email).first()


def add_user(name, email, password):
    db_sess = db_session.create_session()
    user = User(name=name, email=email)
    user.set_password(password)
    db_sess.add(user)
    db_sess.commit()


if __name__ == '__main__':
    init_db()
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
