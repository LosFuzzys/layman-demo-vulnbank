# flask & general app stuff
from flask import current_app, render_template, Markup, make_response
from iron_bank import db, utils


def provide_form(msg=""):
    return render_template('login.html', msg=Markup.escape(msg))


def handle(mysql, name, pwd):
    # 0. does the user exist?
    if not db.user_exists(mysql, name):
        return provide_form("Username does not exist!")

    # 1. check password
    pwd_db= db.get_pwd(mysql, name)
    if pwd_db is None:
        return provide_form("Problem while checking the data! Please contact an administrator.")

    hashed_pwd = utils.get_hash(pwd)
    if hashed_pwd != pwd_db:
        return provide_form("Password is not correct!")

    # 2. get info
    info = db.get_info(mysql, name)
    if info is None:
        return provide_form("Problem while checking the data! Please contact an administrator.")

    # 3. get user id
    id = db.get_user_id(mysql, name)
    if id is None:
        return provide_form("Problem while checking the data! Please contact an administrator.")

    # 4. craft session cookie
    token = utils.generate_session_token()

    #   a. delete previous session token in DB(if one exists)
    if not db.delete_session(mysql, id):
        return provide_form("Problem while storing data! Please contact an administrator.")

    #   b. create session token in DB
    if not db.create_session(mysql, id, token):
        return provide_form("Problem while storing data! Please contact an administrator.")

    cookie = utils.generate_cookie(id, token)

    # 3. navigate to profile page
    # todo: change
    #response = make_response(registration.handle(mysql=mysql, user_id=id))
    #response.set_cookie(current_app.config['COOKIE_NAME'], cookie, httponly=True)

    return provide_form("todo!")

    # if db.create_user(mysql, name, pwd):
    #     return render_template('profile.html', name=name, info=info)
    # else:
    #     msg = "Failed to create user. Please contact an administrator."
    # return render_template('registration.html', msg=Markup.escape(msg))
