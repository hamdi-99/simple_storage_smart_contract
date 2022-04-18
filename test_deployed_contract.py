from web3 import Web3
import os
from dotenv import load_dotenv
from function import contract_abi

load_dotenv()

with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()

abi, bytcode = contract_abi(simple_storage_file, "SimpleStorage.sol", "SimpleStorage")

w3 = Web3(Web3.HTTPProvider(os.getenv("URL")))
chain_id = os.getenv("CHAIN_ID")
address = os.getenv("ADDRESS")

simple_storage = w3.eth.contract("0x86C0ca19A9356E11608aDf799e32aAC8C889A4C0", abi=abi)

print(f"stored value {simple_storage.functions.retrieve().call()}")
