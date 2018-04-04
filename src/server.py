#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: set fileencoding=utf-8

from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_mysqldb import MySQL
from iron_bank import registration, login_bank

app = Flask(__name__)
Bootstrap(app)

# IP address of Docker service or name of the Docker service's name, when in the same network
app.config['MYSQL_HOST'] = 'db'
app.config['MYSQL_PORT'] = 3306
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1amR00t!'
app.config['MYSQL_DB'] = 'iron_bank'

app.config['COOKIE_NAME'] = 'iron_session'

mysql = MySQL(app)

accounts = {'jdoe': {'name': 'John Doe',
                     'balance': 100,
                     'transactions': [
                         {'type': 'from', 'who': "Big Mama Doe", 'amount': 100}
                     ]
                     },
            'mmustermann': {'name': 'Max Mustermann',
                            'balance': 100000000,
                            'transactions': [
                                {'type': 'from', 'who': 'Employer',
                                    'amount': 3000},
                                {'type': 'to', 'who': 'Landlord',
                                    'amount': 1200},
                                {'type': 'to', 'who': 'Money Launderer',
                                    'amount': 5000},
                            ]
                            }
            }


def perform_transaction(sender, receiver, amount):

    accounts[sender]['balance'] -= amount
    accounts[receiver]['balance'] += amount

    accounts[sender]['transactions'].append({'type': 'to',
                                             'who': receiver,
                                             'amount': amount})
    accounts[receiver]['transactions'].append({'type': 'from',
                                               'who': sender,
                                               'amount': amount})


@app.route('/logout')
def logout():
    return redirect(url_for('index'))


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return registration.provide_form()
    else:
        return registration.handle(request, mysql)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return login_bank.provide_form()
    else:
        return login_bank.handle(request, mysql)


@app.route('/account', methods=['GET', 'POST'])
def account():
    error = None
    if request.method == "POST":
        if request.form['user'] and request.form['user'] in accounts:
            user = request.form['user']
            return redirect(url_for("account_status", username=user))
        else:
            error = "Invalid Username or Password"

    return render_template('login.html', error=error)


@app.route('/account/<username>')
def account_status(username):
    return render_template('account.html',
                           user=accounts[username],
                           username=username)


@app.route('/account/<username>/transfer', methods=['GET', 'POST'])
def transfer_moneyz(username):
    if request.method == 'GET':
        return render_template('transfer.html', username=username)
    else:
        toUser = request.form['to']
        amount = int(request.form['amount'])

        if toUser not in accounts:
            # TODO: error
            error = "no such user '{}'".format(toUser)
            return render_template('transfer.html', error=error)

        perform_transaction(username, toUser, amount)

        return redirect(url_for("account_status", username=username))


@app.route('/help')
def help():
    return render_template('help.html')


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5555)
