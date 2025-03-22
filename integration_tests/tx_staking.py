import base64

from terra_classic_sdk.client.lcd import LCDClient
from terra_classic_sdk.client.lcd.api.tx import CreateTxOptions
from terra_classic_sdk.client.localterra import LocalTerra
from terra_classic_sdk.core import Coin, Coins, ValConsPubKey
from terra_classic_sdk.core.staking import (
    CommissionRates,
    Description,
    MsgBeginRedelegate,
    MsgCreateValidator,
    MsgDelegate,
    MsgEditValidator,
    MsgUndelegate,
)
from terra_classic_sdk.key.mnemonic import MnemonicKey


def main():
    terra = LCDClient(
        chain_id="columbus-5",
        url="https://api-lunc-lcd.binodes.com"
    )
    wallet = terra.wallet(key=MnemonicKey(
        mnemonic="sport oppose usual cream task benefit canvas party sock century involve quality"
    ))

    msgDel = MsgDelegate(
        validator_address="terravaloper1s2xpff7mj6jpxfyhr7pe25vt8puvgj4wy0tzjx",
        delegator_address="terra1drs4gul908c59638gu9s88mugdnujdprjhtu7n",
        amount="10000000uluna",
    )
    msgRedel = MsgBeginRedelegate(
        validator_dst_address="terravaloper16x9dcx9pm9j8ykl0td4hptwule706ysjel6500",
        validator_src_address="terravaloper1s2xpff7mj6jpxfyhr7pe25vt8puvgj4wy0tzjx",
        delegator_address="terra1drs4gul908c59638gu9s88mugdnujdprjhtu7n",
        amount=Coin.parse("10000000uluna"),
    )

    msgUndel = MsgUndelegate(
        validator_address="terravaloper16x9dcx9pm9j8ykl0td4hptwule706ysjel6500",
        delegator_address="terra1drs4gul908c59638gu9s88mugdnujdprjhtu7n",
        amount=Coin.parse("9000000uluna"),
    )

    tx = wallet.create_and_sign_tx(CreateTxOptions(msgs=[msgDel], gas_adjustment=1.2))
    result = terra.tx.broadcast(tx)
    print(f"RESULT:{result}")

    tx = wallet.create_and_sign_tx(CreateTxOptions(msgs=[msgRedel], gas_adjustment=1.2))
    result = terra.tx.broadcast(tx)
    print(f"RESULT:{result}")

    tx = wallet.create_and_sign_tx(CreateTxOptions(msgs=[msgUndel], gas_adjustment=1.2))
    print(tx)
    result = terra.tx.broadcast(tx)
    print(f"RESULT:{result}")


main()
