from hashlib import sha256
import requests
from flask import Flask, jsonify, request
import json


def proof():
    response = requests.get(url="http://127.0.0.1:5000/transactions")

    # if empty, opt out
    if(len(response.json()) == 0):
        return

    previous_hash = requests.get(url="http://127.0.0.1:5000/previousHash")
    transaction_list = response.json()

    for proof in range(0,1000000):
        possible_block = json.dumps({"transactions": transaction_list, "previous_hash": previous_hash.json(), "proof": proof})
        prefix = sha256(possible_block.encode()).hexdigest()[0:4]
        if(prefix == "0000"):
            print(possible_block)
            break
    response = requests.post(url="http://127.0.0.1:5000/mine/proof",json=possible_block)

proof()


# {
#     TransactionList:[
#         {"amount":"2","from":"tony","to":"arthur"},
#         {"amount":"2","from":"arthur","to":"tony"}
#     ],
#     PreviousHash: 0x12391823791872,
#     Proof: 3
# }

# TODO: Make the miner to select what transactions to include in the block
# TODO: