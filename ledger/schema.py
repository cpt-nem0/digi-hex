from ledger import mongo as db


class pendingTransactionsSchema(db.Document):
    amount = db.IntField(sparse=True)
    clientEmail = db.StringField(sparse=True)
    remarks = db.StringField(sparse=True)
    b_email = db.StringField(sparse=True)


class transactionSchema(db.EmbeddedDocument):
    amount = db.IntField()
    timeStamp = db.StringField(sparse=True)
    status = db.StringField(sparse=True)
    remarks = db.StringField(sparse=True)
    previousHash = db.StringField(sparse=True, unique=True)
    _hash = db.StringField(sparse=True, unique=True)


class clientSchema(db.EmbeddedDocument):
    clientName = db.StringField(sparse=True)
    clientEmail = db.StringField(sparse=True)
    clientMobile = db.IntField(sparse=True)
    firstTransaction = db.IntField(sparse=True)
    clientTransactions = db.ListField(db.EmbeddedDocumentField('transactionSchema'))


class businessSchema(db.Document):
    b_id = db.StringField(required=True, unique=True)
    b_name = db.StringField(required=True, unique=True)
    b_owner = db.StringField(required=True)
    b_email = db.StringField(required=True, unique=True)
    b_mobile = db.IntField(required=True, unique=True)
    b_password = db.StringField(required=True)
    clients = db.ListField(db.EmbeddedDocumentField('clientSchema'))
