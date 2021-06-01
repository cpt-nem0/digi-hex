from ledger import app
from flask import render_template, redirect, url_for


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/register')
def register_page():
    return render_template('register.html')

@app.route('/login')
def login_page():
    return render_template('login.html')

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