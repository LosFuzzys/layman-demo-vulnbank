

def user_exists(mysql, user):
    try:
        cur = mysql.connection.cursor()
        print("before check user sql query", flush=True)
        cur.execute("SELECT user FROM users WHERE user=%s;", (user, ))
        print("after check user sql query", flush=True)

        num_rows = cur.rowcount

        if num_rows > 0:
            return True
    except Exception as e:
        print(e, flush=True)
        return True

    return False


def create_user(mysql, user, pwd, balance):
    try:
        cur = mysql.connection.cursor()

        print("before create user sql query", flush=True)
        cur.execute("INSERT INTO users (user, pwd, balance) VALUES(%s,%s,%s);", (user, pwd, str(balance)))
        print("after create user sql query", flush=True)

        mysql.connection.commit()
        return True
    except Exception as e:
        print(e, flush=True)
        return False


def create_session(mysql, user_id, token):
    try:
        cur = mysql.connection.cursor()

        print("before create session sql query", flush=True)
        print("user_id: ", user_id, "token: ", token)
        cur.execute("INSERT INTO sessions (user_id, token) VALUES(%s,%s);", (str(user_id), token))
        print("after create session sql query", flush=True)

        mysql.connection.commit()
        return True
    except Exception as e:
        print(e, flush=True)
        return False


def get_pwd(mysql, user):
    try:
        cur = mysql.connection.cursor()

        print("before get pwd sql query", flush=True)
        cur.execute("SELECT pwd FROM users WHERE user=%s;", (user, ))
        print("after  get pwd sql query", flush=True)

        # castle approach: there has to be only one user with that name
        num_rows = cur.rowcount
        if num_rows != 1:
            return None

        result = cur.fetchone()
        pwd = result[0]
        return pwd
    except Exception as e:
        print(e, flush=True)
        return None


# def get_name(mysql, user_id):
#     try:
#         cur = mysql.connection.cursor()
#         print("before get name sql query", flush=True)
#         cur.execute("SELECT name FROM users WHERE id='" + str(user_id) + "';")
#         print("after  get name sql query", flush=True)
#
#         # castle approach: there has to be only one user with that id
#         num_rows = cur.rowcount
#         if num_rows != 1:
#             return None
#
#         result = cur.fetchone()
#         name = result[0]
#         return name
#     except Exception as e:
#         print(e, flush=True)
#         return None


def get_balance(mysql, user):
    try:
        cur = mysql.connection.cursor()

        print("before get balance sql query", flush=True)
        cur.execute("SELECT balance FROM users WHERE user=%s;", (user, ))
        print("after  get balance sql query", flush=True)

        # castle approach: there has to be only one user with that name
        num_rows = cur.rowcount
        if num_rows != 1:
            return None

        result = cur.fetchone()
        balance = result[0]
        return balance
    except Exception as e:
        print(e, flush=True)
        return None


def get_user_id(mysql, user):
    try:
        cur = mysql.connection.cursor()

        print("before get user_id sql query", flush=True)
        cur.execute("SELECT id FROM users WHERE user=%s;", (user, ))
        print("after  get user_id sql query", flush=True)

        # castle approach: there has to be only one user with that name
        num_rows = cur.rowcount
        if num_rows != 1:
            return None

        result = cur.fetchone()
        id = result[0]
        return id
    except Exception as e:
        print(e, flush=True)
        return None


def get_user_balance_list(mysql, user_id):
    try:
        cur = mysql.connection.cursor()

        print("before get user balance list sql query", flush=True)
        cur.execute("SELECT user, balance FROM users WHERE id!=%s;", (str(user_id), ))
        print("after  get user balance list sql query", flush=True)

        result = cur.fetchall()
        user_list = []

        for r in result:
            account = dict()
            account['user'] = r[0]
            account['balance'] = r[1]
            user_list.append(account)

        return user_list
    except Exception as e:
        print(e, flush=True)
        return None


def get_session_token(mysql, user_id):
    try:
        cur = mysql.connection.cursor()
        # print("before get session token sql query", flush=True)
        cur.execute("SELECT token FROM sessions WHERE user_id=%s;", (str(user_id), ))
        # print("after  get session token sql query", flush=True)

        # castle approach: there has to be only one token with that user id
        num_rows = cur.rowcount
        if num_rows != 1:
            print("More than one session token for a the user with id '%s'!" % str(user_id), flush=True)
            return None

        result = cur.fetchone()
        token = result[0]
        return token
    except Exception as e:
        print(e, flush=True)
        return None


def delete_session(mysql, user_id):
    try:
        cur = mysql.connection.cursor()

        print("before delete session token sql query", flush=True)
        cur.execute("DELETE FROM sessions WHERE user_id=%s;", (str(user_id), ))
        print("after delete session token sql query", flush=True)

        mysql.connection.commit()
        return True
    except Exception as e:
        print(e, flush=True)
        return False
