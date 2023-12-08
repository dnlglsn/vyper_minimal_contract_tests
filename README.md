# Minimal Vyper Contracts

Here are example contracts, tests, and Ganache integration tests for two simple Vyper contracts. I originally wrote them to debug some issues I was having and decided to open source them for others to use and enjoy.

## Installation

```bash
pip install -r requirements.txt
```

## Unit Tests (CURRENTLY BROKEN)

We have written unit tests using `eth_tester`. It can test the basic functions contained within a
Vyper contract.

```bash
$ pytest
================================================= test session starts =================================================
platform linux -- Python 3.10.4, pytest-7.1.2, pluggy-1.0.0
rootdir: /home/dgleason/git/mev_sharing, configfile: pytest.ini
plugins: web3-5.31.3
collected 2 items

test_contracts.py ..                                                                                            [100%]

================================================== 2 passed in 0.68s ==================================================
```

## Integration Tests

We run integration tests in order to test contract interactions. We use Ganache since it's closer to
a real chain than `eth_tester`.

### Start Ganache

We need to start Ganache first before we do anything.

```bash
$ ./start_ganache.sh 
ganache v7.9.1 (@ganache/cli: 0.10.1, @ganache/core: 0.10.1)
Starting RPC server

Available Accounts
==================
(0) 0x1687BD6E217cD3bD0C1F10bBd6C240bDF31FE4A2 (100 ETH)
(1) 0x06BAfF84dC5c7FC181CD0d43530dA2cD0dAd0C6b (100 ETH)
(2) 0x2195Bc659Acd4dBd575C3Efa9E214468890837Ec (100 ETH)
(3) 0xbFc4b1D6c8c2bc4e94EbBF596bc6425b93a03a68 (100 ETH)
(4) 0x9b87871A5641a118Fc57af072556aa65810Cce38 (100 ETH)
(5) 0x3bD1F3EFD8e5a73540bEe18f1Fc1BD459bB2b81d (100 ETH)

Private Keys
==================
(0) 0x0eadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeef
(1) 0x1eadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeef
(2) 0x2eadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeef
(3) 0x3eadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeef
(4) 0x4eadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeef
(5) 0x5eadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeef

Default Gas Price
==================
2000000000

BlockGas Limit
==================
30000000

Call Gas Limit
==================
50000000

Chain
==================
Hardfork: shanghai
Id:       1337

RPC Listening on 127.0.0.1:8545

```

### Deploy the Contracts

First, deploy the contracts onto Ganache. The script also fixes the contract pointers.

```bash
$ ./deploy.sh

Contract address: 0xAD2fB447D49Bbb739a314cb27166C3ABdc61301f
Contract ABI written to: deposit.json
Contract ABI-encoded constructor args: 0000000000000000000000007acaa92b7be0f6e6ed61d58e642cda65b6feacbe

Contract address: 0x7aCaA92b7bE0F6e6eD61D58e642cDA65B6FEacBE
Contract ABI written to: withdraw.json
Contract ABI-encoded constructor args: 000000000000000000000000ad2fb447d49bbb739a314cb27166c3abdc61301f

Contract address: 0x95Cd966557C23504f824893bCc68e0e186365Af0
Contract ABI written to: ecrecover.json
Contract ABI-encoded constructor args: 
```

### Test

```bash
$ python deposit_and_withdraw_test.py

depositContract funds 0
withdrawContract funds 0

depositContract funds 10000000000000000000
withdrawContract funds 0
(AttributeDict({'args': AttributeDict({'theCaller': '0x1687BD6E217cD3bD0C1F10bBd6C240bDF31FE4A2', 'value': 10000000000000000000}), 'event': 'BalanceTransferred', 'logIndex': 0, 'transactionIndex': 0, 'transactionHash': HexBytes('0x96a9acc0b664252f192c6008babff96aeb6e63afe79d964666a478ffe5ece855'), 'address': '0xAD2fB447D49Bbb739a314cb27166C3ABdc61301f', 'blockHash': HexBytes('0x4dea1822cdcdf0fb63bdb8f76e34b410ebf3f5e266f2cebad15f6c94ba39ae91'), 'blockNumber': 4}),)

depositContract funds 0
withdrawContract funds 10000000000000000000
```

```bash
$ python ecrecover_test.py
expected public key: 0x7917bDC011955E1B45195553D2AAE6AB17422298
ecrecover result:    0x7917bDC011955E1B45195553D2AAE6AB17422298
```
