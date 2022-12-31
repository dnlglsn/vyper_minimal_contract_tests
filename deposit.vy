lastDeposit: public(uint256)
withdrawContractAddress: public(address)


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
    self.lastDeposit = msg.value


@external
@nonpayable
def transfer_balance():
    send(self.withdrawContractAddress, self.balance)
