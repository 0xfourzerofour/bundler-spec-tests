"""
Test suite for `eip4337 bunlder` module.
See https://github.com/eth-infinitism/bundler
"""

from dataclasses import asdict
import pytest

from tests.types import RPCRequest
from tests.utils import assertRpcError, assertFieldsTypes


def test_eth_estimateUserOperationGas(cmd_args, badSigUserOp):
    response = RPCRequest(method="eth_estimateUserOperationGas",
                          params=[asdict(badSigUserOp), cmd_args.entry_point]).send(cmd_args.url)
    assertFieldsTypes(response.result, ['callGasLimit', 'preVerificationGas', 'verificationGas'], [int, int, int])


def test_eth_estimateUserOperationGas_revert(cmd_args, wallet_contract, badSigUserOp):
    badSigUserOp.callData = wallet_contract.encodeABI(fn_name='fail')
    response = RPCRequest(method="eth_estimateUserOperationGas",
                          params=[asdict(badSigUserOp), cmd_args.entry_point]).send(cmd_args.url)
    assertRpcError(response, "test fail", -32500)
