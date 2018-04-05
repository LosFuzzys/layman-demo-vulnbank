# flask & general app stuff
from flask import current_app, render_template, Markup, make_response
from iron_bank import db, utils


def provide_form_overview(msg="", account=dict()):
    return render_template('account.html', error=Markup.escape(msg), user=account)


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

    # if request.form['user'] and request.form['user'] in accounts:
    #     user = request.form['user']
    #     return redirect(url_for("account_status", username=user))
    # else:
    #     error = "Invalid Username or Password"


# @app.route('/account/<username>/transfer', methods=['GET', 'POST'])
# def transfer_moneyz(username):
#     if request.method == 'GET':
#         return render_template('transfer.html', username=username)
#     else:
#         toUser = request.form['to']
#         amount = int(request.form['amount'])
#
#         if toUser not in accounts:
#             # TODO: error
#             error = "no such user '{}'".format(toUser)
#             return render_template('transfer.html', error=error)

        perform_transaction(username, toUser, amount)

        return redirect(url_for("account_status", username=username))
