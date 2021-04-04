
import sys
import requests

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

#print ('Number of Arguments:'+ str(len(sys.argv))+ 'arguments.')
#print ('Argument List:'+ str(sys.argv))

if(sys.argv[1] == '-n'):
    post_new_transaction(sys.argv[2], sys.argv[3], sys.argv[4])
elif(sys.argv[1] == '-b'):
    print(balance())
