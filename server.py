from flask import Flask, render_template, request, jsonify
from hashlib import sha256
from flask_restful import Resource, Api,reqparse

app = Flask(__name__)
chain = {
            'index':'0',
            'block':[],
        }
api = Api(app)
parser = reqparse.RequestParser()
pendingTransaction = []
pendingTransaction.append({"from": "arthur", "to": "tony", "amount": "1"})

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
        pendingTransaction.append(args)
        resp = jsonify(success=True)
        resp.status_code = 200
        return resp

api.add_resource(Chain,'/chain')
api.add_resource(Transactions,'/transactions')
api.add_resource(NewTransaction,'/transactions/new')
app.run()