from typing import Dict
from flask import Flask, render_template, request, jsonify
from hashlib import sha256
import json
import copy
import pickle
from flask_restful import Resource, Api,reqparse

app = Flask(__name__)
chain = []
api = Api(app)
parser = reqparse.RequestParser()
pendingTransaction = {}
balance = dict({'Tony': 1000, 'Arthur': 1000})
latest_hash =0x0 # Need to be updated everytime a chain updates

def save():
    # this method is for saving the chain, balance, pendingTransaction, latest_hash
    with open('chain.pickle', 'wb') as f:
        pickle.dump([chain,balance,pendingTransaction,latest_hash], f)
    return

def load():
    global chain 
    global balance 
    global pendingTransaction
    global latest_hash
    with open('chain.pickle', 'rb') as f:
        chain,balance,pendingTransaction,latest_hash = pickle.load(f)

@app.route('/')
def home():
    return render_template("index.html", data=[balance, pendingTransaction, chain])

class Chain(Resource):
    def get(self):
        return jsonify(chain)

class Transactions(Resource):
    def get(self):
        return jsonify(pendingTransaction)

class NewTransaction(Resource):
    def post(self):
        args = request.get_json()
        # decoded = json.loads(args)
        print(args)
        transaction_hash = sha256(json.dumps(args).encode()).hexdigest()
        pendingTransaction[transaction_hash] = args
        save()
        resp = jsonify(success=True)
        resp.status_code = 200
        return resp

class Proof(Resource):
    def post(self):
        args = request.get_json()
        hash = sha256(args.encode()).hexdigest()
        prefix = hash[0:4]
        if(prefix != "0000"):
            print("wrong!!!!!!")
            return
        decoded = json.loads(args)
        transactions = decoded['transactions']
        global balance
        global latest_hash
        global pendingTransaction
        balance_cpy = copy.deepcopy(balance)
        transaction_hashes = []
        for transact in transactions:
            print(transact)
            source = transact['From']
            dest = transact['To']
            amount = int(transact['Amount'])
            if(source not in balance_cpy):
                balance_cpy[source] = 0
            if(dest not in balance_cpy):
                balance_cpy[dest] = 0
            if(balance_cpy[source] < amount):
                print("insuccient gold")
                return
            balance_cpy[source] -= amount
            balance_cpy[dest] += amount
            transaction_hashes.append(sha256(json.dumps(transact).encode()).hexdigest())
        balance = balance_cpy
        latest_hash = hash
        chain.append(args)
        for transaction_hash in transaction_hashes:
            del pendingTransaction[transaction_hash]
        save()


class PreviousHash(Resource):
    def get(self):
        resp = jsonify(latest_hash)
        return resp

class Balance(Resource):
    def get(self):
        return balance

load()
api.add_resource(Chain,'/chain')
api.add_resource(Transactions,'/transactions')
api.add_resource(NewTransaction,'/transactions/new')
api.add_resource(Proof,'/mine/proof')
api.add_resource(PreviousHash,'/previousHash')
api.add_resource(Balance,'/balance')
app.run()