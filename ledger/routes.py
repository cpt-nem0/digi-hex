from ledger import app
from flask import render_template, redirect, url_for

from ledger.forms import RegistrationForm, LoginForm


@app.route('/')
def landing_page():
    return render_template('landing_page.html')

@app.route('/login')
def login_page():
    form = LoginForm()
    return render_template('login.html', form=form)

@app.route('/register')
def register_page():
    form = RegistrationForm()
    # mongo add here
    return render_template('register.html', form=form)

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


@app.route('/paymentrequest')
def payment_request():
    return render_template('payment_request.html')

@app.route('/profile')
def user_profile():
    return render_template('user_profile.html')

@app.route('/viewclients')
def view_clients():
    return render_template('view_clients.html')

@app.route('/addclients')
def add_clients():
    return render_template('add_clients.html')