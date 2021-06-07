from ledger import mongo as db
from ledger import bcrypt
from ledger import login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return Businesses.objects(user_id=user_id)


class pendingTransaction(db.Document):
    transaction_id = db.StringField(sparse=True, unique=True)
    amount = db.IntField(sparse=True)
    clientEmail = db.StringField(sparse=True)
    remarks = db.StringField(sparse=True)
    b_email = db.StringField(sparse=True)


class Transaction(db.EmbeddedDocument):
    transaction_id = db.StringField(sparse=True, unique=True)
    amount = db.IntField()
    timeStamp = db.StringField(sparse=True)
    status = db.StringField(sparse=True)
    remarks = db.StringField(sparse=True)
    previousHash = db.StringField(sparse=True, unique=True)
    _hash = db.StringField(sparse=True, unique=True)


class Clients(db.EmbeddedDocument):
    clientName = db.StringField(sparse=True)
    clientEmail = db.StringField(sparse=True, unique=True)
    clientMobile = db.IntField(sparse=True, unique=True)
    firstTransaction = db.IntField(sparse=True)
    clientTransactions = db.ListField(db.EmbeddedDocumentField('Transaction'))


class Businesses(db.Document, UserMixin):
    b_id = db.StringField(required=True, unique=True)
    b_name = db.StringField(required=True, unique=True)
    b_owner = db.StringField(required=True)
    b_email = db.StringField(required=True, unique=True)
    b_mobile = db.IntField(required=True, unique=True)
    b_password_hash = db.StringField(required=True)
    clients = db.ListField(db.EmbeddedDocumentField('Clients'))

    @property
    def b_password(self):
        return self.b_password_hash

    @b_password.setter
    def b_password(self, plain_text_password):
        self.b_password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')


    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.b_password_hash, attempted_password)