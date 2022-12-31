# @version ^0.3.0

depositContractAddress: public(address)


@external
@nonpayable
def __init__(depositContractAddress: address):
    self.depositContractAddress = depositContractAddress


@external
@nonpayable
def set_deposit_contract_address(depositContractAddress: address):
    self.depositContractAddress = depositContractAddress


@external
@payable
def __default__():
    assert msg.sender == self.depositContractAddress, 'You cannot send funds to this contract.'
    # We cannot have any log messages or anything that uses gas here or we will get a reversion.
