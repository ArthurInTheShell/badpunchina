from hashlib import sha256
import requests
from flask import Flask, jsonify, request
import json

def post_new_transaction():
    response = requests.post(url="http://127.0.0.1:5000/transactions/new",json=new_transaction)
    print(response)


def proof():
    response = requests.get(url="http://127.0.0.1:5000/transactions")
    transaction_list = response.text

    for proof in range(0,1000000):
        possible_block = json.dumps({"transactions": transaction_list, "previous_hash": 0x0, "proof": proof})
        prefix = sha256(possible_block.encode()).hexdigest()[0:4]
        if(prefix == "0000"):
            print(sha256(possible_block.encode()).hexdigest())
            print(proof)
            break
    response = requests.post(url="http://127.0.0.1:5000/proof",json=possible_block)

new_transaction = {"from": "tony", "to": "arthur", "amount": "2"}
post_new_transaction()
proof()


# {
#     TransactionList:[
#         {"amount":"2","from":"tony","to":"arthur"},
#         {"amount":"2","from":"arthur","to":"tony"}
#     ],
#     PreviousHash: 0x12391823791872,
#     Proof: 3
# }