import uuid
import datetime

from ledger import app
from ledger.schema import *
from ledger.payment import precessPayment
from ledger.blockchain.blockchain import *
from ledger.mail_service.sender import send_mail

from flask import render_template, redirect, url_for, session, flash, request
from flask_login import login_user
from ledger.forms import RegistrationForm, LoginForm, AddClientsForm, paymentRequest


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
        attempted_user = Businesses.objects(b_email=form.user_email.data).first()
        if attempted_user and attempted_user.check_password_correction(attempted_password=form.user_password.data):
            login_user(attempted_user)
            session['user'] = attempted_user.b_owner
            session['user_id'] = attempted_user.b_id
            return redirect(url_for('dashboard'))
        else:
            flash("Email and Password don't match. Try again")

    return render_template('login.html', form=form)

@app.route('/register/', methods=['POST', 'GET'])
def register_page():
    form = RegistrationForm()
    
    if form.validate_on_submit():
        
        # create user
        newUser = Businesses(
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

@app.route('/profile/')
def user_profile():
    if 'user' in session:
        user_data = Businesses.objects(b_id=session['user_id']).first()
        return render_template('user_profile.html', user_data=user_data)
    
    return render_template('landing_page.html')

@app.route('/paymentrequest/', methods=['POST', 'GET'])
def payment_request():
    if 'user' in session:
        userData = Businesses.objects(b_id=session.get('user_id')).first()
        clients = [client for client in userData.clients]
        if request.method == 'POST':
            transaction_id = uuid.uuid4().hex
            clientMail = request.form.get('clientList')
            amount = request.form.get('paymentAmt')
            remarks = request.form.get('remarks')
            try:
                send_mail(transaction_id, clientMail, amount, remarks)
                flash("Mail was sent to the client.", category='success')
            except :
                flash("Mail was NOT sent!!", category='danger')
            
            paymentReq = pendingTransaction(
                transaction_id=transaction_id,
                amount=amount,
                clientEmail=clientMail,
                remarks=remarks,
                b_email=userData.b_email
            )
            paymentReq.save()
        return render_template('payment_request.html', clients=clients)
    
    return render_template('landing_page.html')

@app.route('/viewclients/')
def view_clients():
    if 'user' in session:
        userData = Businesses.objects(b_id=session.get('user_id')).first()
        clients = [client for client in userData.clients]
        return render_template('view_clients.html', clients=clients)

    return render_template('landing_page.html')

@app.route('/addclients/', methods=['POST', 'GET'])
def add_clients():
    form = AddClientsForm()
    if 'user' in session:
        if form.validate_on_submit():
            userData = Businesses.objects(b_id=session['user_id']).first()
            clientInfo = Clients(
                clientName=form.client_name.data,
                clientEmail=form.client_email.data,
                clientMobile=form.client_phone.data,
                firstTransaction=1
            )
            userData.clients.append(clientInfo)
            userData.save()
            
            if form.errors != {}:
                for err_msg in form.errors.values():
                    flash(err_msg)
            else:
                flash(f"{form.client_name.data} has been added to your clients", category='success')
                
        return render_template('add_clients.html', form=form)
    return render_template('landing_page.html')

@app.route('/transactions/<cPos>')
def view_transactions(cPos):
    if 'user' in session:
        userData = Businesses.objects(b_id=session['user_id']).first().clients
        transactions = userData[int(cPos)-1].clientTransactions
        return render_template('client_transactions.html', transactions=transactions, cPos=cPos)
    
    return render_template('landing_page.html')

@app.route('/clientApproval/<tId>', methods=['POST', 'GET'])
def client_approval(tId):
    form = paymentRequest()
    processingTransaction = pendingTransaction.objects(transaction_id=tId).first()
    if processingTransaction != None:
        owner = Businesses.objects(b_email=processingTransaction.b_email).first()
        if form.validate_on_submit():
            if form.accept.data:
                precessPayment(tId, status='Approved')
                return '<h1>Payment Accepted, Thank you!!</h1>'
            precessPayment(tId, status='Declined')
            return '<h1>Payment Declined, Thank you!!</h1>'
    else:
        return '<h1>Link Expired</h1>'
    return render_template('payment_confirmation.html', transaction=processingTransaction, ownerName=owner.b_owner, form=form)


@app.route('/removeClient/<clientMail>', methods=['GET', 'POST'])
def remove_clients(clientMail):
    userData = Businesses.objects(b_id=session['user_id']).first()
    userData.update(pull__clients__clientEmail=clientMail)

    return redirect(url_for('view_clients'))

@app.route('/logout/')
def logout():
    session.pop('user', None)
    session.pop('user_id', None)
    return redirect(url_for('landing_page'))

@app.route('/validateChain/<cPos>')
def validate_chain(cPos):
    userData = Businesses.objects(b_id=session['user_id']).first().clients
    client = userData[int(cPos)-1]
    dangerIndex = ''
    if client.clientTransactions:
        res = isTransactionChainValid(client.clientTransactions)
        if res['isOk']:
            print('in If')
            flash('All good, your data is safe', category='success')
        else:
            print('in Else')
            dangerIndex=str(res['index'])
            flash('Your Data has been compromised!!', category='danger')
    else:
        flash('No transaction yet!!', category='warning')
    
    if dangerIndex != '':
        return render_template('client_transactions.html', transactions=client.clientTransactions, cPos=cPos, dangerIndex=int(dangerIndex)+1)
    
    return render_template('client_transactions.html', transactions=client.clientTransactions, cPos=cPos)
