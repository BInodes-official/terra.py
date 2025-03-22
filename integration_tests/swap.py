import asyncio
import base64
from pathlib import Path

from terra_classic_sdk.client.lcd import LCDClient
from terra_classic_sdk.client.lcd.api.tx import CreateTxOptions
from terra_classic_sdk.client.localterra import LocalTerra
from terra_classic_sdk.core import Coins
from terra_classic_sdk.core.market import MsgSwap
from terra_classic_sdk.key.mnemonic import MnemonicKey


def main():
    terra = LCDClient(
        url="https://api-lunc-lcd.binodes.com/",
        chain_id="columbus-5",
    )
    key = MnemonicKey(
        mnemonic="sport oppose usual cream task benefit canvas party sock century involve quality"
    )
    wallet = terra.wallet(key=key)

    print(wallet)

    msg = MsgSwap(
        trader="terra1drs4gul908c59638gu9s88mugdnujdprjhtu7n",
        offer_coin="1000000uluna",
        ask_denom="uusd",
    )
    print(msg)
    tx = wallet.create_and_sign_tx(
        CreateTxOptions(msgs=[msg],  gas_adjustment="1.4")
    )
    print(tx)

    # result = terra.tx.broadcast(tx)
    # print(result)


main()
