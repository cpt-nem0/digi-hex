from hashlib import sha256

def addNewTransactionBlock(firstTransaction, amount, remarks, timeStamp, status, previousHash='0'):
    if firstTransaction:
        amount = amount
        remarks = remarks
        timeStamp = timeStamp
        status = status
        previousHash = '0'
    else:
        amount = amount
        remarks = remarks
        previousHash = previousHash
        timeStamp = timeStamp
        status = status

    dataString = str(amount) + remarks + previousHash + str(timeStamp) + status
    _hash = sha256(dataString.encode()).hexdigest() 
    return {'hash':_hash, 'previousHash':previousHash}

def isTransactionChainValid(transactionChain):
    for i in range(len(transactionChain)):
        dataString = str(transactionChain[i].amount) + transactionChain[i].remarks + transactionChain[i].previousHash + transactionChain[i].timeStamp + transactionChain[i].status
        _hash = sha256(dataString.encode()).hexdigest()

        if transactionChain[i]._hash != _hash:
            return { 'isOk': False, 'index': i}

        if i > 0 and transactionChain[i].previousHash != transactionChain[i-1]._hash:
            return { 'isOk': False, 'index': i}
    
    return { 'isOk': True }
