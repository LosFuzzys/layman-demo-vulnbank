# flask & general app stuff
from flask import current_app, render_template, Markup, make_response
from iron_bank import account, db, utils


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
    token = utils.generate_session_token()

    #   a. delete previous session token in DB (if one exists)
    if not db.delete_session(mysql, id):
        return provide_form("Problem while storing data. Please contact an administrator.")

    #   b. create session token in DB
    if not db.create_session(mysql, id, token):
        return provide_form("Problem while storing data. Please contact an administrator.")

    # 3. get user's balance
    balance = db.get_balance(mysql, user)
    if balance is None:
        return provide_form("Problem while getting data. Please contact an administrator.")

    # 4. get other users

    #[{'user': 'jsnowddd', 'balance': 100}, {'user': 'dstormbornbbb', 'balance': 100}]
    user_list = db.get_user_balance_list(mysql, id)
    print("user_list from db: ", user_list)
    if user_list is None:
        return provide_form("Problem while getting data. Please contact an administrator.")

    user_dict = dict()
    user_dict['name'] = user
    user_dict['balance'] = balance
    user_dict['user_list'] = user_list

    cookie = utils.generate_cookie(id, token)

    # 3. navigate to account page
    response = make_response(account.provide_form(account=user_dict))
    response.set_cookie(current_app.config['COOKIE_NAME'], cookie, httponly=True)

    return response


