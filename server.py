from flask import Flask, render_template

app = Flask(__name__)
chain = []

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/chain')
def printChain():
    return len(chain)


app.run()