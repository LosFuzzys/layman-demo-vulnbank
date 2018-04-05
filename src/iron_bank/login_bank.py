# flask & general app stuff
from flask import current_app, render_template, Markup, make_response, redirect, url_for
from iron_bank import account_bank, db, utils


def provide_form(msg=""):
    return render_template('login.html', error=Markup.escape(msg))


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

    # 1. does the user exist?
    if not db.user_exists(mysql, user):
        return None, None, "Username does not exist"

    # 2. check password
    pwd_db = db.get_pwd(mysql, user)
    if pwd_db is None:
        return None, None, "Problem while checking the data. Please contact an administrator."

    hashed_pwd = utils.get_hash(pwd)
    if hashed_pwd != pwd_db:
        return None, None, "Password is not correct"

    return user, pwd, ''


def handle(request, mysql):
    # 0. check input
    (user, pwd, msg) = check_input(request, mysql)

    if msg != '':
        return provide_form(msg)

    # 1. get user id
    id = db.get_user_id(mysql, user)
    if id is None:
        return provide_form("Problem while checking the data. Please contact an administrator.")

    # 2. craft session cookie
    #   a. delete previous session token in DB (if one exists)
    if not db.delete_session(mysql, id):
        return provide_form("Problem while storing data. Please contact an administrator.")

    #   b. create session token
    token = utils.generate_session_token()
    if not db.create_session(mysql, id, token):
        return provide_form("Problem while storing data. Please contact an administrator.")

    cookie = utils.generate_cookie(id, token)

    # 3. get user dict
    user_dict = utils.get_user_account_dict(mysql, id)
    if user_dict is None:
        return provide_form("Problem while getting data. Please contact an administrator.")

    # 4. navigate to account page
    #response = make_response(account_bank.provide_form_overview(account=user_dict))
    response = make_response(redirect(url_for('account')))
    response.set_cookie(current_app.config['COOKIE_NAME'], cookie, httponly=True)

    return response

