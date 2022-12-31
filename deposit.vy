# @version ^0.3.0

withdrawContractAddress: public(address)


event BalanceTransferred:
    theCaller: address
    value: uint256

@external
@nonpayable
def __init__(withdrawContractAddress: address):
    self.withdrawContractAddress = withdrawContractAddress


@external
@nonpayable
def set_withdraw_contract_address(withdrawContractAddress: address):
    self.withdrawContractAddress = withdrawContractAddress


@external
@payable
def __default__():
    pass


@external
@nonpayable
def transfer_balance():
    oldBalance: uint256 = self.balance
    send(self.withdrawContractAddress, self.balance)
    log BalanceTransferred(msg.sender, oldBalance)
