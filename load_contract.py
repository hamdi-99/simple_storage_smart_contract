from web3 import Web3
from function import contract_abi
import os
from dotenv import load_dotenv

load_dotenv()

with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()


abi, bytecode = contract_abi(simple_storage_file, "SimpleStorage.sol", "SimpleStorage")

w3 = Web3(Web3.HTTPProvider(os.getenv("URL")))
chain_id = int(os.getenv("CHAIN_ID"))
address = os.getenv("ADDRESS")

# loading the contract from our blockchain network
simple_storage = w3.eth.contract(
    address="0x86C0ca19A9356E11608aDf799e32aAC8C889A4C0", abi=abi
)

nonce = w3.eth.getTransactionCount(address)

# Calling a view function from our loaded contract
print(f"Initial Stored Value {simple_storage.functions.retrieve().call()}")

# Updating contract by calling a function which change the state of our contract which means building a transaction
transaction = simple_storage.functions.store(30).buildTransaction(
    {
        "chainId": chain_id,
        "gasPrice": w3.eth.gas_price,
        "from": address,
        "nonce": nonce,
    }
)

# signing the transaction
signed_transaction = w3.eth.account.sign_transaction(
    transaction, private_key=os.getenv("PRIVATE_KEY")
)

# Updating our contract by sending the transaction
transaction_hash = w3.eth.send_raw_transaction(signed_transaction.rawTransaction)

print("Updating stored Value...")
transaction_receipt = w3.eth.wait_for_transaction_receipt(transaction_hash)


print(f"New Stored Value {simple_storage.functions.retrieve().call()}")
