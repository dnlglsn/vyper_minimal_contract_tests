import json

from web3 import Web3

# Create the web3 object
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545/'))

# Load the contracts
depositAddress = '0xAD2fB447D49Bbb739a314cb27166C3ABdc61301f'
depositABI = open('deposit.json').read()
depositContract = w3.eth.contract(address=w3.to_checksum_address(depositAddress),
                                       abi=json.loads(depositABI))
withdrawAddress = '0x7aCaA92b7bE0F6e6eD61D58e642cDA65B6FEacBE'
withdrawABI = open('withdraw.json').read()
withdrawContract = w3.eth.contract(address=w3.to_checksum_address(withdrawAddress),
                                    abi=json.loads(withdrawABI))

assert depositContract.functions.withdrawContractAddress().call() == withdrawAddress
assert withdrawContract.functions.depositContractAddress().call() == depositAddress

# The accounts on ganache
admin = '0x1687BD6E217cD3bD0C1F10bBd6C240bDF31FE4A2'  # Admin

print()
print('depositContract funds', w3.eth.get_balance(depositContract.address))
print('withdrawContract funds', w3.eth.get_balance(withdrawContract.address))

# Add some funds to the deposit contract
value = w3.to_wei(10, 'ether')
w3.eth.send_transaction({
    'to': depositContract.address,
    'from': admin,
    'value': value,
})

print()
print('depositContract funds', w3.eth.get_balance(depositContract.address))
print('withdrawContract funds', w3.eth.get_balance(withdrawContract.address))

# Transfer the funds to the other contract
transaction = depositContract.functions.transfer_balance().transact({'from': admin})
receipt = w3.eth.get_transaction_receipt(transaction)
logs = depositContract.events.BalanceTransferred().process_receipt(receipt)
print(logs)

print()
print('depositContract funds', w3.eth.get_balance(depositContract.address))
print('withdrawContract funds', w3.eth.get_balance(withdrawContract.address))
