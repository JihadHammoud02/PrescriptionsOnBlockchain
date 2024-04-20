from web3 import Web3
from web3.middleware import geth_poa
from eth_account import Account
import json
proj_id = "2Qrs6mmPXUPVgyBsaK4GEO6JDai"
proj_secret = "6c4a430ca570bfc603e0c2b9cd1699a7"
# Init
w3 = Web3(Web3.HTTPProvider("https://polygon-amoy.infura.io/v3/b0f53a900b384eb1924a4cc9785afa39"))
w3.middleware_onion.inject(geth_poa.geth_poa_middleware, layer=0)
ABI=[{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[{"internalType":"address","name":"admin","type":"address"}],"name":"addAdmin","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"doctor","type":"address"},{"internalType":"string","name":"name","type":"string"},{"internalType":"string","name":"specialty","type":"string"}],"name":"addDoctor","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"patientAddress","type":"address"},{"internalType":"string","name":"normalMedication","type":"string"},{"internalType":"string","name":"normalDosage","type":"string"},{"internalType":"string","name":"brandedMedication","type":"string"},{"internalType":"string","name":"brandedDosage","type":"string"},{"internalType":"string","name":"age","type":"string"},{"internalType":"string","name":"diagnoses","type":"string"}],"name":"addPrescription","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"doctor","type":"address"}],"name":"getDoctorInfo","outputs":[{"internalType":"string","name":"name","type":"string"},{"internalType":"string","name":"specialty","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getDoctors","outputs":[{"internalType":"address[]","name":"","type":"address[]"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getPatients","outputs":[{"internalType":"address[]","name":"","type":"address[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"patientAddress","type":"address"}],"name":"getPrescriptions","outputs":[{"components":[{"internalType":"address","name":"patientAddress","type":"address"},{"internalType":"string","name":"normalMedication","type":"string"},{"internalType":"string","name":"normalDosage","type":"string"},{"internalType":"string","name":"brandedMedication","type":"string"},{"internalType":"string","name":"brandedDosage","type":"string"},{"internalType":"string","name":"age","type":"string"},{"internalType":"string","name":"diagnoses","type":"string"},{"internalType":"uint256","name":"timestamp","type":"uint256"}],"internalType":"struct DoctorApp.Prescription[]","name":"","type":"tuple[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"user","type":"address"}],"name":"isAdmin","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"user","type":"address"}],"name":"isDoctor","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"admin","type":"address"}],"name":"removeAdmin","outputs":[],"stateMutability":"nonpayable","type":"function"}]
contractAddress="0x45fbF9C466f0EA35cBD6a71BF1438Ac68cE15f2d"

contract_instance = w3.eth.contract(address=contractAddress, abi=ABI)

# For testing purposes we will sign transactions with provided keys , when we connect metamask we are gonna move it to support wallet signature
Adminpublic_key="0x09DE81704a9e21166089e99423721648e6C52f29"
Adminprivate_key="aaabbb0f56d8cda0e7443608cf6ee3c66b7d4bfd03766f84cc528ff23bcff0d0"




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
    print(tx_receipt)
    return tx_receipt


# EMILE WORK
def addAdmin(address,pk,privKey):
    # Construct the transaction data
    nounce=w3.eth.getTransactionCount(pk)
    transaction_data = contract_instance.functions.addAdmin(address).buildTransaction({
        'from': pk,
        'value': 0,
        'gas': 2000000,
        'gasPrice':w3.toWei('50', 'gwei'),
        'nonce': nounce,
        'chainId': 80002  # Chain ID of the Polygon Mumbai chain
    })

    signed_transaction = Account.sign_transaction(
        transaction_data, privKey)

    return send_signed_transaction(signed_transaction)

def containAdmin(address):
    result = contract_instance.functions.isAdmin(address).call()
    return result

def addDoctor(docAdd,name,spec,pk,privKey):
    print("public_key")
# Construct the transaction data
    nounce=w3.eth.getTransactionCount(pk)
    transaction_data = contract_instance.functions.addDoctor(docAdd,name,spec).buildTransaction({
        'from': pk,
        'value': 0,
        'gas': 2000000,
        'gasPrice':w3.toWei('50', 'gwei'),
        'nonce': nounce,
        'chainId': 80002  # Chain ID of the Polygon Mumbai chain
    })

    signed_transaction = Account.sign_transaction(
        transaction_data, privKey)
    
    transaction_hash = send_signed_transaction(signed_transaction)

    tx_receipt = w3.eth.waitForTransactionReceipt(transaction_hash)


    return tx_receipt


def containDoctor(address):
    result = contract_instance.functions.isDoctor(address).call()
    return result



def addPrescription(patAdd,normalMedic,normalDos,brandedMedic,brandedDosage,age,diagnoses,pk,privKey):
# Construct the transaction data
    nounce=w3.eth.getTransactionCount(pk)
    transaction_data = contract_instance.functions.addPrescription(patAdd,normalMedic,normalDos,brandedMedic,brandedDosage,age,diagnoses).buildTransaction({
        'from': pk,
        'value': 0,
        'gas': 2000000,
        'gasPrice':w3.toWei('50', 'gwei'),
        'nonce': nounce,
        'chainId': 80002  # Chain ID of the Polygon Mumbai chain
    })

    signed_transaction = Account.sign_transaction(
        transaction_data, privKey)
    
    transaction_hash = send_signed_transaction(signed_transaction)

    tx_receipt = w3.eth.waitForTransactionReceipt(transaction_hash)


    return tx_receipt

def get_patients():
    result = contract_instance.functions.getPatients().call()
    return result


def get_prescriptions(add):
    # Construct the transaction data

    result = contract_instance.functions.getPrescriptions(add).call()
    presc=[]
    for res in result:
        presc.append({"patientAddress":res[0],"normalMedication":res[1],"normalDosage":res[2],"brandedMedication":res[3],"brandedDosage":res[4],"age":res[5],"diagnoses":res[6]})

    return json.dumps(presc)
