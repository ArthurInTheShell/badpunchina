
import sys
import requests
import Crypto

publickey = 0
privatekey = 0

def post_new_transaction(from_wallet, to_wallet, amount):
    transaction = {
        "From": from_wallet,
        "To": to_wallet,
        "Amount": amount
        }
    response = requests.post(url="http://127.0.0.1:5000/transactions/new",json=transaction)
    print(response)

def balance():
    response = requests.get(url="http://127.0.0.1:5000/balance")
    return response.json()

def transactions():
    response = requests.get(url="http://127.0.0.1:5000/transactions")
    return response.json()

def new_rsa():
    random_generator = Crypto.Random.new().read
    key = Crypto.PublicKey.RSA.generate(1024, random_generator)
    global publickey
    global privatekey
    publickey = key.publickey()
    privatekey = key.privatekey()
    print("Your Public Key is: " + key.publickey())
    print("Your Private Key is: " + key.privatekey())


#print ('Number of Arguments:'+ str(len(sys.argv))+ 'arguments.')
#print ('Argument List:'+ str(sys.argv))

if(sys.argv[1] == '-n'):
    post_new_transaction(sys.argv[2], sys.argv[3], sys.argv[4])
elif(sys.argv[1] == '-b'):
    print(balance())
elif(sys.argv[1] == '-t'):
    print(transactions())
elif(sys.argv[1] == '-new_rsa'):
    new_rsa()