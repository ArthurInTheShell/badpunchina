from flask import Flask, render_template, request, jsonify
from hashlib import sha256
import json
from flask_restful import Resource, Api,reqparse

app = Flask(__name__)
chain = {
            'index':'0',
            'block':[],
        }
api = Api(app)
parser = reqparse.RequestParser()
pendingTransaction = []

@app.route('/')
def home():
    return render_template("index.html", data=pendingTransaction)

class Chain(Resource):
    def get(self):
        return chain

class Transactions(Resource):
    def get(self):
        return jsonify(pendingTransaction)

class NewTransaction(Resource):
    def post(self):
        args = request.get_data()
        decoded = json.loads(args.decode())
        pendingTransaction.append(decoded)
        print(pendingTransaction)
        resp = jsonify(success=True)
        resp.status_code = 200
        return resp

class Proof(Resource):
    def post(self):
        args = request.get_data()


api.add_resource(Chain,'/chain')
api.add_resource(Transactions,'/transactions')
api.add_resource(NewTransaction,'/transactions/new')
api.add_resource(Proof,'/proof')
app.run()