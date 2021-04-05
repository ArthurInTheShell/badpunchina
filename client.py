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
    balance_cpy = requests.get(url="http://127.0.0.1:5000/balance").json()
    transaction_map = response.json()
    transaction_list = []
    for hash in transaction_map.keys():
        transact = transaction_map[hash]
        source = transact['From']
        dest = transact['To']
        amount = int(transact['Amount'])
        if(source not in balance_cpy):
            balance_cpy[source] = 0
        if(dest not in balance_cpy):
            balance_cpy[dest] = 0
        if(balance_cpy[source] < amount):
            print("insuccient gold")
            continue
        balance_cpy[source] -= amount
        balance_cpy[dest] += amount
        transaction_list.append(transaction_map[hash])

    if(len(transaction_list) == 0):
        return

    for proof in range(0,1000000):
        possible_block = json.dumps({"transactions": transaction_list, "previous_hash": previous_hash.json(), "proof": proof})
        prefix = sha256(possible_block.encode()).hexdigest()[0:4]
        if(prefix == "0000"):
            print(possible_block)
            break
    response = requests.post(url="http://127.0.0.1:5000/mine/proof",json=possible_block)

proof()