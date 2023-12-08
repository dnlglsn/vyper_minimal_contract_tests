#!/bin/env bash

# Fail on error, undefined variables, and pipefail
set -euo pipefail

# Deploy the deposit contract
# Args: The address of the withdraw contract on a new Ganache run
(python deploy.py deposit.vy 0x1687BD6E217cD3bD0C1F10bBd6C240bDF31FE4A2 --adminPrivateKey 0x0eadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeef \
--chain ganache --writeABI deposit.json --args \
0x7aCaA92b7bE0F6e6eD61D58e642cDA65B6FEacBE \
)

# Deploy the withdraw contract
# Args: The address of the deposit contract on a new Ganache run
(python deploy.py withdraw.vy 0x1687BD6E217cD3bD0C1F10bBd6C240bDF31FE4A2 --adminPrivateKey 0x0eadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeef \
--chain ganache --writeABI withdraw.json --args \
0xAD2fB447D49Bbb739a314cb27166C3ABdc61301f \
)

# Deploy the ecrecover testing contract
# Args: none
(python deploy.py ecrecover.vy 0x1687BD6E217cD3bD0C1F10bBd6C240bDF31FE4A2 --adminPrivateKey 0x0eadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeef \
--chain ganache --writeABI ecrecover.json \
)
