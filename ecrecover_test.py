import json

from web3 import Web3

# Create the web3 object
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545/'))

# Load the contracts
ecrecoverAddress = '0x95Cd966557C23504f824893bCc68e0e186365Af0'
ecrecoverABI = open('ecrecover.json').read()
ecrecoverContract = w3.eth.contract(address=w3.to_checksum_address(ecrecoverAddress),
                                       abi=json.loads(ecrecoverABI))

pubkey = '0x7917bdc011955e1b45195553d2aae6ab17422298'
message = '0x386ded3bb68b793a89f2ee202fda07824c6ed764f0ee88ebe48b8bd4baf702ec'
signature = '0x75557d500e5459cbb7c922fb91720c0707018ace391b0b1265ba38f59f8a294c029434efb733e5cafa923494c6efa8854d4cc61674d4a1ca4400388a03e813ff1b'

print('expected public key:', w3.to_checksum_address(pubkey))
print('ecrecover result:   ', ecrecoverContract.functions.verify_signature(message, signature).call())
