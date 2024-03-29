import time

from web3 import Web3, HTTPProvider

import contract_abi



contract_address     = Web3.toChecksumAddress('0x710c1f7f9143232456a6c0e87fd53c63e617a703')

wallet_private_key   = "8ce8b39507ba09ee2b9b18d0d702c5d36ff0b5ed301bdf2ef2863ff54f02ce02"

wallet_address       = Web3.toChecksumAddress('0x788b3c6eb380eb9328667f6bad4815c98310506e')



# web3.py instance

w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))



contract = w3.eth.contract(address = contract_address, abi = contract_abi.abi)



def broadcast_reading(counter):





    nonce = w3.eth.getTransactionCount(wallet_address)



    txn_dict = contract.functions.newReading(counter).buildTransaction({

        'chainId': 3,

        'gas': 140000,

        'gasPrice': w3.toWei('40', 'gwei'),

        'nonce': nonce,

    })



    signed_txn = w3.eth.account.signTransaction(txn_dict, private_key = wallet_private_key)



    txn_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)



    txn_receipt = None

    count = 0

    while txn_receipt is None and (count < 30):



        txn_receipt = w3.eth.getTransactionReceipt(txn_hash)



        print(txn_receipt)



        time.sleep(10)





    if txn_receipt is None:

        return {'status': 'failed', 'error': 'timeout'}



    return {'status': 'added', 'txn_receipt': txn_receipt}



for i in range(5):

    broadcast_reading(i)

def check_reading():



    return(contract.functions.returnCarbonCredits().call())




print(check_reading())
