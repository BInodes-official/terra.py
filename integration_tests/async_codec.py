import asyncio

import uvloop

from terra_classic_sdk.client.lcd import AsyncLCDClient
from terra_classic_sdk.client.lcd.api.tx import CreateTxOptions
from terra_classic_sdk.core import Coins
from terra_classic_sdk.core.bank import MsgSend
from terra_classic_sdk.key.mnemonic import MnemonicKey


async def with_sem(aw, sem):
    async with sem:
        print(sem)
        return await aw


async def main():
    terra = AsyncLCDClient(chain_id="columbus-5", url="https://terra-classic-lcd.publicnode.com/")
    mk = MnemonicKey(
        mnemonic="sport oppose usual cream task benefit canvas party sock century involve quality"
    )
    awallet = terra.wallet(mk)

    msg = MsgSend(
        "terra1drs4gul908c59638gu9s88mugdnujdprjhtu7n",
        "terra1s2xpff7mj6jpxfyhr7pe25vt8puvgj4wyq8lz4",
        Coins(uluna=20),
    )
    tx = await awallet.create_and_sign_tx(
        CreateTxOptions(
            msgs=[msg],
            gas_prices="0.15uluna",
            gas="63199",  # gas="auto", gas_adjustment=1.1
            fee_denoms=["uluna"],
        )
    )

    encoded = await terra.tx.encode(tx)
    print(f"encoded...{encoded}")

    print("=" * 64)

    decoded = await terra.tx.decode(encoded)
    print(f"decoded...{decoded}")

    await terra.session.close()


uvloop.install()
asyncio.run(main())
