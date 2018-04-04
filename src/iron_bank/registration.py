
from flask import render_template, Markup, url_for
from iron_bank import db, utils
# render_template --> blacklist


def provide_form(msg=""):
    return render_template('registration.html', error=Markup.escape(msg))


def check_input(request, mysql):
    print("request.form: ", request.form, flush=True)

    # 0. check input
    if request.form is None:
        return None, None, "No form data provided"

    user = request.form['user']
    pwd = request.form['password']

    if not utils.validate_input(user, pwd):
        msg = "User name or password is not valid. Allowed characters: [0-9a-zA-Z_] and a minimum length of 4."
        return None, None, msg

    # 1. does the user already exist?
    if db.user_exists(mysql, user):
        return None, None, "Username already exists"

    return user, pwd, ''


def handle(request, mysql):
    # 0. check input
    (user, pwd, msg) = check_input(request, mysql)

    if msg != '':
        return provide_form(msg)

    # 1. hash password
    hashed_pwd = utils.get_hash(pwd)

    # 2. create user
    start_balance = 100
    if not db.create_user(mysql, user, hashed_pwd, start_balance):
        return provide_form("Failed to create user. Please contact an administrator.")

    return render_template('index.html',
                           msg="Successfully registered! Now you can login =)")
