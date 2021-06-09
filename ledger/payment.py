import datetime

from ledger.schema import *
from ledger.blockchain import blockchain

from flask import session


def precessPayment(tId, status):
    processingTransaction = pendingTransaction.objects(transaction_id=tId).first()
    client = Businesses.objects(b_id=session['user_id']).first()
    index = 0
    for i in client.clients:
        if i.clientEmail == processingTransaction.clientEmail:
            break
        index += 1
    
    transaction = client.clients[index].clientTransactions
    timestamp = datetime.datetime.now()
    if client.clients[index].firstTransaction == 1:
        hashes = blockchain.addNewTransactionBlock(
            firstTransaction=client.clients[index].firstTransaction, 
            amount=processingTransaction.amount, 
            remarks=processingTransaction.remarks, 
            timeStamp=timestamp,
            status=status
        )
    else:
        hashes = blockchain.addNewTransactionBlock(
            firstTransaction=client.clients[index].firstTransaction, 
            amount=processingTransaction.amount, 
            remarks=processingTransaction.remarks, 
            timeStamp=timestamp,
            status=status,
            previousHash=transaction[-1]._hash
        )
    currentTransaction = Transaction(
        transaction_id=tId,
        amount=processingTransaction.amount,
        timeStamp=str(timestamp),
        status=status,
        remarks=processingTransaction.remarks,
        previousHash=hashes['previousHash'],
        _hash=hashes['hash']
    )
    
    # sets first transaction to False
    client.clients[index].firstTransaction = 0
    client.clients[index].clientTransactions.append(currentTransaction)
    client.save()
    
    # remove pending
    processingTransaction.delete()
