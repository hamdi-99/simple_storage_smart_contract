import json
from web3 import Web3
from function import contract_abi
from dotenv import load_dotenv
import os

load_dotenv()

with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()

# Getting the contract abi
abi, bytecode = contract_abi(simple_storage_file, "SimpleStorage.sol", "SimpleStorage")

# connecting web3 and setting the wanted variables
w3 = Web3(Web3.HTTPProvider(os.getenv("URL")))
chain_id = int(os.getenv("CHAIN_ID"))
address = os.getenv("ADDRESS")

# initializing the contract as an object
simple_storage = w3.eth.contract(abi=abi, bytecode=bytecode)

# getting the nonce which here is the number of the transactions that are made
nonce = w3.eth.getTransactionCount(address)

# building the transaction (the transaction here is the creation of the contract)
transaction = simple_storage.constructor().buildTransaction(
    {"chainId": chain_id, "from": address, "gasPrice": w3.eth.gas_price, "nonce": nonce}
)

# signing the transaction
signed_transaction = w3.eth.account.sign_transaction(
    transaction, private_key=os.getenv("PRIVATE_KEY")
)

# Deploying our contract by sending the transaction
print("Deploying contract ...")
transaction_hash = w3.eth.send_raw_transaction(signed_transaction.rawTransaction)
print("Waiting for transaction to finish...")
transaction_receipt = w3.eth.wait_for_transaction_receipt(transaction_hash)
print(f"Done! Contract deployed to {transaction_receipt.contractAddress}")
