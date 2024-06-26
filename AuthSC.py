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
ABI=[{"inputs":[{"internalType":"address","name":"adminAddress","type":"address"}],"name":"addAdmin","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newDoctorAddress","type":"address"},{"internalType":"address","name":"AdminCalling","type":"address"}],"name":"addDoctor","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"add","type":"address"}],"name":"containAdmin","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"add","type":"address"}],"name":"containDoctor","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"}]
contractAddress="0xeA103529C1D64237d02927Dc91845a5b40A30c14"

contract_instance = w3.eth.contract(address=contractAddress, abi=ABI)

# For testing purposes we will sign transactions with provided keys , when we connect metamask we are gonna move it to support wallet signature
public_key=""
private_key=""


def verify_keys(public_key, private_key):
    
    # Derive the public key from the private key
    derived_public_key = w3.eth.account.from_key(private_key).address
    
    # Compare the derived public key with the provided public key
    if derived_public_key == public_key:
        public_key=public_key
        private_key=private_key
        return True
    else:
        return False




# For sending transactions
def send_signed_transaction(signed_transaction):
    response = w3.eth.sendRawTransaction(signed_transaction.rawTransaction)
    return response.hex()

def to_32byte_hex(val):
  return Web3.toHex(Web3.toBytes(val).rjust(32, b'\0'))

def fireTransaction(transaction_data):
    # Sign the transaction locally
    tx_hash = w3.eth.sendTransaction(transaction_data)
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    return tx_receipt

def addAdmin(address):
    # Construct the transaction data
    nounce=w3.eth.getTransactionCount(w3.eth.defaultAccount)
    transaction_data = contract_instance.functions.addAdmin(address).buildTransaction({
        'from': w3.eth.defaultAccount,
        'value': 0,
        'gas': 2000000,
        'gasPrice':w3.toWei('50', 'gwei'),
        'nonce': nounce,
        'chainId': 80002  # Chain ID of the Polygon Mumbai chain
    })

    return fireTransaction(transaction_data)

def containAdmin(address):
    result = contract_instance.functions.containAdmin(address).call()
    return result

def addDoctor(docAdd,admin):
# Construct the transaction data
    nounce=w3.eth.getTransactionCount(w3.eth.defaultAccount)
    transaction_data = contract_instance.functions.addDoctor(docAdd,admin).buildTransaction({
        'from': public_key,
        'value': 0,
        'gas': 2000000,
        'gasPrice':w3.toWei('50', 'gwei'),
        'nonce': nounce,
        'chainId': 80002  # Chain ID of the Polygon Mumbai chain
    })

    return fireTransaction(transaction_data)


def containDoctor(address):
    result = contract_instance.functions.containDoctor(address).call()
    return result

