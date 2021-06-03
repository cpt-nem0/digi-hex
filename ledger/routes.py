import uuid 

from ledger import app
from ledger.schema import *
from flask import render_template, redirect, url_for, session, request, flash, get_flashed_messages
from flask_login import login_user
from ledger.forms import RegistrationForm, LoginForm


@app.route('/')
def landing_page():
    return render_template('landing_page.html')

@app.route('/dashboard/')
def dashboard():
    if 'user' in session:
        return render_template('dashboard.html')
    
    return render_template('landing_page.html')

@app.route('/login/', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()

    if form.validate_on_submit():
        attempted_user = businessSchema.objects(b_email=form.user_email.data).first()
        if attempted_user and attempted_user.check_password_correction(attempted_password=form.user_password.data):
            login_user(attempted_user)
            session['user'] = attempted_user.b_owner
            session['user_id'] = attempted_user.b_id
            print(attempted_user.b_owner)
            return redirect(url_for('dashboard'))
        else:
            flash("Email and Password don't match. Try again")

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
        )
        newUser.b_password = form.password.data
        newUser.save()
        session['user'] = form.owner_name.data
        session['user_id'] = newUser.b_id
        return redirect(url_for('dashboard'))

    if form.errors != {}: # errors from the validation
        for err_msg in form.errors.values():
            flash(err_msg)

    return render_template('register.html', form=form)

@app.route('/paymentrequest/')
def payment_request():
    if 'user' in session:
        return render_template('payment_request.html')
    
    return render_template('landing_page.html')

@app.route('/profile/')
def user_profile():
    if 'user' in session:
        user_data = businessSchema.objects(b_id=session['user_id']).first()
        return render_template('user_profile.html', user_data=user_data)
    
    return render_template('landing_page.html')

@app.route('/viewclients/')
def view_clients():
    if 'user' in session:
        return render_template('view_clients.html')

    return render_template('landing_page.html')

@app.route('/addclients/')
def add_clients():
    if 'user' in session:
        return render_template('add_clients.html')
    
    return render_template('landing_page.html')

@app.route('/logout/')
def logout():
    session.pop('user', None)
    session.pop('user_id', None)
    return redirect(url_for('landing_page'))