
# flask & general app stuff
from flask import current_app
from iron_bank import db

# helper stuff
import re
import os
import json
import hashlib
from base64 import b64encode as b64e, b64decode as b64d

REGEX_USER     = "^[0-9a-zA-Z_]{4,50}$"
REGEX_PWD      = "^[0-9a-zA-Z_]{4,100}$"
REGEX_USER_ID  = "^[0-9]+$"


def check_user(name):
    if not re.match(REGEX_USER, name):
        return False

    return True


def check_pwd(pwd):
    if not re.match(REGEX_PWD, pwd):
        return False

    return True


def check_user_id(user_id):
    if not re.match(REGEX_USER_ID, user_id):
        return False

    return True


def validate_input(user, pwd):
    if (user is None) or (pwd is None):
        return False

    # user valid?
    if not check_user(user):
        return False

    # password valid?
    if not check_pwd(pwd):
        return False

    return True


def check_session(request, mysql):
    try:
        cookie = request.cookies[current_app.config['COOKIE_NAME']]
    except KeyError as e:
        print(e, flush=True)
        return None

    if (cookie is None) or (cookie is ''):
        return None

    try:
        cookie_dict = json.loads(b64d(cookie).decode('utf-8'))
        user_id = cookie_dict['id']
        token = cookie_dict['token']
    except Exception as e:
        print(e, flush=True)
        return None

    if (user_id is None) or (token is None) or (not check_user_id(str(user_id))):
        return None

    token_db = db.get_session_token(mysql, user_id)
    if token_db is None:
        return None

    if token != token_db:
        return None

    return user_id


def get_hash(hinput):
    h = hashlib.sha256()
    h.update(hinput.encode('utf-8'))

    output = h.digest()
    return output.hex()


def generate_session_token():
    token_bytes = os.urandom(16)
    return token_bytes.hex().lower()


def generate_cookie(id, token):
    cookie_dict = dict()
    cookie_dict['id'] = id
    cookie_dict['token'] = token

    print("cookie: ", cookie_dict, flush=True)

    cookie = b64e(json.dumps(cookie_dict).encode('utf-8'))
    return cookie
