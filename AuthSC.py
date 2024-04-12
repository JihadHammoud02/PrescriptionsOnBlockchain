from web3 import Web3
from web3.middleware import geth_poa
from eth_account import Account
import environ
from eth_account.messages import encode_defunct
env = environ.Env()
environ.Env.read_env()
proj_id = "2Qrs6mmPXUPVgyBsaK4GEO6JDai"
proj_secret = "6c4a430ca570bfc603e0c2b9cd1699a7"
# Init
w3 = Web3(Web3.HTTPProvider("https://polygon-amoy.infura.io/v3/b0f53a900b384eb1924a4cc9785afa39"))
w3.middleware_onion.inject(geth_poa.geth_poa_middleware, layer=0)
ABI=[{"inputs":[{"internalType":"address","name":"adminAddress","type":"address"}],"name":"addAdmin","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"add","type":"address"}],"name":"containAdmin","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"add","type":"address"}],"name":"onlyAdmin","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"}]
contractAddress="0xe4e573c776Ea54764E25aAf99B7b99De2ff4d78C"

contract_instance = w3.eth.contract(address=contractAddress, abi=ABI)

# For testing purposes we will sign transactions with provided keys , when we connect metamask we are gonna move it to support wallet signature
public_key="0x9cd4D8EcA8954e55ea1B8d194B2A4E5dfb4EE7dc"
private_key="ce136daa0b7ffc83cf1ac6aae719e25e31037b117913b751a0726a551a5e9d17"

# For sending transactions
def send_signed_transaction(signed_transaction):
    response = w3.eth.sendRawTransaction(signed_transaction.rawTransaction)
    return response.hex()

def to_32byte_hex(val):
  return Web3.toHex(Web3.toBytes(val).rjust(32, b'\0'))

def fireTransaction(transaction_data):
    # Sign the transaction locally
    signed_transaction = Account.sign_transaction(
        transaction_data, private_key)

    # Send the signed transaction
    transaction_hash = send_signed_transaction(signed_transaction)
    tx_receipt = w3.eth.waitForTransactionReceipt(transaction_hash)
    return tx_receipt 

def addAdmin(address):
    # Construct the transaction data
    nounce=w3.eth.getTransactionCount(public_key)
    transaction_data = contract_instance.functions.addAdmin(address).buildTransaction({
        'from': public_key,
        'value': 0,
        'gas': 2000000,
        'gasPrice':w3.toWei('50', 'gwei'),
        'nonce': nounce,
        'chainId': 80002  # Chain ID of the Polygon Mumbai chain
    })

    return fireTransaction(transaction_data)

def containAdmin(address):
    nounce=w3.eth.getTransactionCount(public_key)
    transaction_data = contract_instance.functions.containAdmin(address).buildTransaction({
        'from': public_key,
        'value': 0,
        'gas': 2000000,
        'gasPrice':w3.toWei('50', 'gwei'),
        'nonce': nounce,
        'chainId': 80002  # Chain ID of the Polygon Mumbai chain
    })

    return fireTransaction(transaction_data)



print(containAdmin("0x9cd4D8EcA8954e55ea1B8d194B2A4E5dfb4EE7dc"))