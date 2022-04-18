from solcx import compile_standard
import json


def contract_abi(contract, contract_filename, contract_name):
    compiled_sol = compile_standard(
        {
            "language": "Solidity",
            "sources": {contract_filename: {"content": contract}},
            "settings": {
                "outputSelection": {
                    "*": {
                        "*": [
                            "abi",
                            "metadata",
                            "evm.bytecode",
                            "evm.bytecode.sourceMap",
                        ]
                    }
                }
            },
        },
        solc_version="0.8.7",
    )

    with open("compiled_code.json", "w") as file:
        json.dump(compiled_sol, file)

    # get bytecode
    bytecode = compiled_sol["contracts"][contract_filename][contract_name]["evm"][
        "bytecode"
    ]["object"]

    # get abi
    abi = json.loads(
        compiled_sol["contracts"][contract_filename][contract_name]["metadata"]
    )["output"]["abi"]
    return (abi, bytecode)
