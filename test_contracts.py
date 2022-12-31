import pytest

ZERO_ADDRESS = '0x'+(b'\0'*20).hex()  # ETH address length


@pytest.fixture
def contracts(w3, get_contract):
    admin = w3.eth.accounts[0]

    # Create the contract objects
    deposit = get_contract(open('deposit.vy').read(), ZERO_ADDRESS)
    withdraw = get_contract(open('withdraw.vy').read(), ZERO_ADDRESS)

    # Set the dependencies correctly
    deposit.set_withdraw_contract_address(withdraw.address, transact={'from': admin})
    withdraw.set_deposit_contract_address(deposit.address, transact={'from': admin})

    # Return everything we need
    return w3, deposit, withdraw


def test_initial_state(contracts):
    # The circular dependency should be set from the fixture. Test it.
    _, deposit, withdraw = contracts
    assert deposit.withdrawContractAddress() == withdraw.address
    assert withdraw.depositContractAddress() == deposit.address


def test_transfer_balance(contracts):
    w3, deposit, withdraw = contracts
    admin = w3.eth.accounts[0]

    # Send some ETH to the deposit contract
    sendValue = w3.toWei(1, 'ether')
    w3.eth.sendTransaction({
        'to': deposit.address,
        'from': admin,
        'value': sendValue,
    })

    # The balance in the deposit contract should be the amount sent
    assert w3.eth.get_balance(deposit.address) == sendValue

    # Transfer the balance to the withdraw contract
    deposit.transfer_balance(transact={'from': admin})

    # The balance in the deposit should have been transferred to the withdraw contract
    assert w3.eth.get_balance(deposit.address) == 0
    assert w3.eth.get_balance(withdraw.address) == sendValue
