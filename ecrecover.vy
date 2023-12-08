# pragma version ^0.3.10

# TODO: In the future, implement EIP-712 v4:
# https://eips.ethereum.org/EIPS/eip-712
# https://soliditydeveloper.com/ecrecover
# https://medium.com/coinmonks/eip712-a-full-stack-example-e12185b03d54
# https://metamask.github.io/test-dapp/

# References:
# https://vyper.readthedocs.io/en/stable/built-in-functions.html#ecrecover

# Sign a message of the form `prefixedHashedMessage`:
# prefixedHashedMessage: A keccak-256 hash of an Ethereum Signed Message
# ```
# keccak256('\x19Ethereum Signed Message:\n{message length}{message}')
# ```

@external
@pure
def verify_signature(prefixedHashedMessage: bytes32, signature: Bytes[65]) -> address:

    # Split the signature into the r, s, and v components
    r: bytes32 = convert(slice(signature, 0, 32), bytes32)
    s: bytes32 = convert(slice(signature, 32, 32), bytes32)
    v: uint8 = convert(slice(signature, 64, 1), uint8)
    return ecrecover(prefixedHashedMessage, v, r, s)
