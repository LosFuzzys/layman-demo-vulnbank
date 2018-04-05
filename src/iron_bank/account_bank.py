# flask & general app stuff
from flask import current_app, render_template, Markup, make_response
from iron_bank import db, utils


def provide_form_overview(msg="", account=dict()):
    return render_template('account.html', error=Markup.escape(msg), user=account)


def check_transfer_input(request, mysql):
    print("request.form: ", request.form, flush=True)

    # 0. check input
    if request.form is None:
        return None, None, "No form data provided"

    user_to = request.form['to']
    amount = request.form['amount']

    if user_to is None or amount is None:
        return None, None, "No form data provided"

    if not utils.check_user(user_to) or not utils.check_transfer_amount(amount):
        return None, None, "Invalid user or amount"

    try:
        amount = int(amount)
    except ValueError as e:
        return None, None, "Invalid amount. Please enter only numbers"

    # 1. does the user exist?
    if not db.user_exists(mysql, user_to):
        return None, None, "User does not exist"

    return user_to, amount, ''


def handle_view(mysql, user_id):
    # 0. check input
    if mysql is None or user_id is None:
        return render_template('index.html', error=Markup.escape('Internal error. Please contact an administrator.'))

    # 1. get user dict for view
    user_dict = utils.get_user_account_dict(mysql, user_id)
    if user_dict is None:
        return render_template('index.html', error=Markup.escape('Internal error while getting data. '
                                                                 'Please contact an administrator.'))

    # 2. provide view
    return provide_form_overview(account=user_dict)


def handle_transfer(request, mysql, user_id):
    # 0. check input
    if mysql is None or user_id is None:
        return render_template('index.html', error=Markup.escape('Internal error. Please contact an administrator.'))

    # 1. get user account dict
    user_dict = utils.get_user_account_dict(mysql, user_id)
    if user_dict is None:
        msg = 'Internal error during getting of data. Please contact an administrator.'
        return provide_form_overview(msg=msg, account=user_dict)

    user_owner = user_dict['name']
    balance_owner = user_dict['balance']
    print("balance: ", balance_owner, type(balance_owner), flush=True)

    # 2. check form input
    (user_to, amount, msg) = check_transfer_input(request, mysql)
    if msg != '':
        return provide_form_overview(msg=msg, account=user_dict)

    # 3. sending to the own account?
    if user_to == user_owner:
        msg = 'You cannot transfer money to your own account. You already have it ;)'
        return provide_form_overview(msg=msg, account=user_dict)

    # 4. does the user have enough credits?
    if amount > balance_owner:
        msg = 'You do not have enough money'
        return provide_form_overview(msg=msg, account=user_dict)

    # 5. get balance of the receiver
    balance_to = db.get_balance(mysql, user_to)
    if balance_to is None:
        msg = 'Internal error during getting of data. Please contact an administrator.'
        return provide_form_overview(msg=msg, account=user_dict)

    # 6. generate new balances
    balance_owner -= amount
    balance_to += amount

    # 7. set new balances
    if (not db.set_balance(mysql, user_owner, balance_owner)) or \
       (not db.set_balance(mysql, user_to, balance_to)):
        msg = 'Internal error during getting of data. Please contact an administrator.'
        return provide_form_overview(msg=msg, account=user_dict)

    # 8. get new user account dict
    user_dict = utils.get_user_account_dict(mysql, user_id)
    if user_dict is None:
        msg = 'Internal error during getting of data. Please contact an administrator.'
        return provide_form_overview(msg=msg, account=user_dict)

    return provide_form_overview(account=user_dict)



