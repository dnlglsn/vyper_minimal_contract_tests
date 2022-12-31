# Why is this failing?

```
FAILED test_contracts.py::test_transfer_balance - eth_tester.exceptions.TransactionFailed: execution reverted: b''
```

If I comment out https://github.com/dnlglsn/vyper_minimal_contract_tests/blob/main/withdraw.vy#L27-L28, the tests pass. It seems to pass whenever the secondary contract's default method doesn't have any gas-guzzling functions. I am not sure if this is an artifact of `eth_tester` or not. I will deploy these onto Ganache and see what happens there.
