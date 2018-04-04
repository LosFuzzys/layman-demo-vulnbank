# flask & general app stuff
from flask import current_app, render_template, Markup, make_response
from iron_bank import db, utils


def provide_form(msg="", account=dict()):
    return render_template('account.html', error=Markup.escape(msg), user=account)
