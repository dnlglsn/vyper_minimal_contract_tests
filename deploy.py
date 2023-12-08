import argparse
import getpass
import json

from vyper import compiler
from web3 import Web3, HTTPProvider
from web3.middleware import geth_poa_middleware


ARG_TYPES = {
    'address': str,
    'uint256': int,
}


def compile_contract(location, options=['abi', 'bytecode']):
    source = open(location).read()
    return compiler.compile_code(source, options)


def deploy(location, endpoint, constructorArgs, publicKey, privateKey, chain):

    """ This is a general function used to deploy a contract.
    Create specific contract deployment files and use this function to deploy them.
    We need to do this because we can't parse command line arguments in Jupyter. """

    # Connect to the web3 endpoint
    web3 = Web3(HTTPProvider(endpoint))
    web3.middleware_onion.inject(geth_poa_middleware, layer=0)

    chainId = {
        'ganache': 1337,
        'goerli': 5,
    }[chain]

    # Compile the a contract
    compiled = compile_contract(location)

    # Convert the constructor args to the correct type
    contractArgs = [f for f in compiled['abi'] if f['type'] == 'constructor']
    convertedArgs = []
    if len(contractArgs) > 0:
        convertedArgs = [ARG_TYPES[contractArgs[0]['inputs'][i]['type']](arg)
                         for i, arg in enumerate(constructorArgs)]

    # Create a web3 loaded contract
    contract = web3.eth.contract(abi=compiled['abi'], bytecode=compiled['bytecode'])

    # Create a construction transaction for the contract
    constructArgs = {
        'from': publicKey,
        'nonce': web3.eth.get_transaction_count(publicKey),
        'gasPrice': web3.eth.gas_price,
        'chainId': chainId
    }
    # For Ganache local deployment we need more stuff
    if chain == 'ganache':
        constructArgs['gas'] = 5000000
        constructArgs['gasPrice'] = 100000000000

    txConstruct = contract.constructor(*convertedArgs).build_transaction(constructArgs)

    # We need the ABI encoded constructor args for source code verification
    abiEncodedArgs = txConstruct['data'].split(compiled['bytecode'])[1]

    # Sign the transaction with the wallet's private key
    txCreate = web3.eth.account.sign_transaction(txConstruct, privateKey)

    # Send the transaction to our web3 endpoint
    txHash = web3.eth.send_raw_transaction(txCreate.rawTransaction)

    # Wait for the receipt
    txReceipt = web3.eth.wait_for_transaction_receipt(txHash)

    # return the deployed contract's address
    return txReceipt.contractAddress, json.dumps(compiled['abi'], indent=4), abiEncodedArgs


if __name__ == '__main__':

    # Parse some command line arguments
    parser = argparse.ArgumentParser(description='Deploy a contract')
    parser.add_argument('contractFilename', help='The filename of the contract to deploy. Must be absolute.')
    parser.add_argument('adminPublicKey', help='The public key of the wallet used to deploy the contract. Will be the admin.')
    parser.add_argument('--adminPrivateKey', help='We need the private key to sign the transaction which deploys the contract.')
    parser.add_argument('-a','--args', nargs='*', default=[], help="The contract's constructor arguments.")
    parser.add_argument('--endpoint', default='http://127.0.0.1:8545/', help='The web3 JSON RPC endpoint used to deploy.')
    parser.add_argument('--chain', default='ganache', choices=['ganache', 'goerli'], help='The chain used.')
    parser.add_argument('--writeABI', default='', help='Optionally write out the ABI to this filename.')
    args = parser.parse_args()

    # Get the private key of the wallet address as password input if it wasn't given on the CLI
    privateKey = args.adminPrivateKey or getpass.getpass("Please enter the admin wallet's private key: ")

    # Deploy!
    address, abi, abiEncodedArgs = deploy(
        args.contractFilename, args.endpoint, args.args, args.adminPublicKey, privateKey, args.chain
    )

    # Print the deployed contract's address
    print()
    print('Contract address: %s' % address)
    if args.writeABI == '':
        print('Contract ABI: %s' % abi)
    # Write out the ABI if requested
    else:
        open(args.writeABI, 'wt').write(abi)
        print('Contract ABI written to: %s' % args.writeABI)
    print('Contract ABI-encoded constructor args: %s' % abiEncodedArgs)
