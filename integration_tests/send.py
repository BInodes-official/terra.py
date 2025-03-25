import asyncio
import base64
from pathlib import Path
from terra_classic_sdk.core.fee import Fee

from terra_classic_sdk.client.lcd import LCDClient
from terra_classic_sdk.client.lcd.api.tx import CreateTxOptions
from terra_classic_sdk.core import Coins
from terra_classic_sdk.core.bank import MsgSend
from terra_classic_sdk.core.tx import SignMode
from terra_classic_sdk.key.mnemonic import MnemonicKey


def main():
    terra = LCDClient(
        url="https://api-lunc-lcd.binodes.com/",
        chain_id="columbus-5",
    )
    key = MnemonicKey(mnemonic="sport oppose usual cream task benefit canvas party sock century involve quality")
    wallet = terra.wallet(key=key)


    tx = wallet.create_and_sign_tx(CreateTxOptions(
        msgs=[MsgSend(
            "terra1drs4gul908c59638gu9s88mugdnujdprjhtu7n",
            'terra1s2xpff7mj6jpxfyhr7pe25vt8puvgj4wyq8lz4',
            "1000000uluna"  # send 1 luna
        )],
        memo="test transaction!",
        gas_adjustment=1.2,  # Auto fee
        # fee=Fee(240324,'7023928uluna'),  # The fee designated by the user
    ))
    print(tx)

    result = terra.tx.broadcast(tx)
    print(result)


main()
