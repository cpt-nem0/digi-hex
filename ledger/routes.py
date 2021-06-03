import uuid 

from ledger import app, mongo
from ledger.schema import *
from flask import render_template, redirect, url_for, session, request, flash, get_flashed_messages
from ledger.forms import RegistrationForm, LoginForm


@app.route('/')
def landing_page():
    return render_template('landing_page.html')

@app.route('/dashboard/')
def dashboard():
    if 'user' in session:
        return render_template('dashboard.html')
    
    return render_template('landing_page.html')

@app.route('/login/', methods=['POST', 'GET'])
def login_page():
    form = LoginForm()

    if request.method == 'POST' and form.validate_on_submit():

        login_user = businessSchema.objects(b_email=form.user_email.data).first()
        if login_user:
            if form.user_password.data == login_user.b_password:
                session['user'] = login_user.b_owner
            else:
                flash('Wrong Password')
            return render_template('dashboard.html')

    return render_template('login.html', form=form)

@app.route('/register/', methods=['POST', 'GET'])
def register_page():
    form = RegistrationForm()
    
    if request.method == 'POST' and form.validate_on_submit():
        
        # create user
        newUser = businessSchema(
            b_id = uuid.uuid4().hex,
            b_name = form.business_name.data,
            b_owner = form.owner_name.data,
            b_email = form.owner_email.data,
            b_mobile =  form.owner_phone.data,
            b_password = form.password.data
        )
        newUser.save()
        session['user'] = form.owner_name.data
        return redirect(url_for('dashboard'))

    if form.errors != {}: # errors from the validation
        for err_msg in form.errors.values():
            flash(err_msg)

    return render_template('register.html', form=form)

@app.route('/paymentrequest/')
def payment_request():
    return render_template('payment_request.html')

@app.route('/profile/')
def user_profile():
    return render_template('user_profile.html')

@app.route('/viewclients/')
def view_clients():
    return render_template('view_clients.html')

@app.route('/addclients/')
def add_clients():
    return render_template('add_clients.html')

@app.route('/logout/')
def logout():
    session.pop('user', None)
    return redirect(url_for('landing_page'))