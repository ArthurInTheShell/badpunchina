from typing import Dict
from flask import Flask, render_template, request, jsonify
from hashlib import sha256
import json
import copy
from flask_restful import Resource, Api,reqparse

app = Flask(__name__)
chain = []
api = Api(app)
parser = reqparse.RequestParser()
pendingTransaction = []
balance = dict({'Tony': 1000, 'Arthur': 1000})
latest_hash =0x0 # Need to be updated everytime a chain updates

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
        pendingTransaction.append(args)
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
        balance_cpy = copy.deepcopy(balance)
        for transact in transactions:
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
        balance = balance_cpy
        latest_hash = hash
        chain.append(args)

class PreviousHash(Resource):
    def get(self):
        resp = jsonify(latest_hash)
        return resp

class Balance(Resource):
    def get(self):
        return balance

api.add_resource(Chain,'/chain')
api.add_resource(Transactions,'/transactions')
api.add_resource(NewTransaction,'/transactions/new')
api.add_resource(Proof,'/mine/proof')
api.add_resource(PreviousHash,'/previousHash')
api.add_resource(Balance,'/balance')
app.run()

# TODO: Get all the data to the Website
# TODO: Save to local