lastDeposit: public(uint256)
depositContractAddress: public(address)


event FundsAdded:
    value: uint256


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

    # Commenting out the following lines will cause the test to pass.
    self.lastDeposit = msg.value
    log FundsAdded(msg.value)
