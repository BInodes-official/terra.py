import base64

from terra_classic_sdk.client.lcd import LCDClient
from terra_classic_sdk.client.lcd.api.tx import CreateTxOptions
from terra_classic_sdk.core.gov.msgs import MsgVote
from terra_classic_sdk.key.mnemonic import MnemonicKey


def main():
    terra = LCDClient(
        chain_id="columbus-5",
        url="https://api-lunc-lcd.binodes.com"
    )
    wallet = terra.wallet(key=MnemonicKey(
        mnemonic="sport oppose usual cream task benefit canvas party sock century involve quality"
    ))

    msgVote=MsgVote(
        proposal_id=12163,
        voter='terra1drs4gul908c59638gu9s88mugdnujdprjhtu7n',
        option=3
    )


    tx = wallet.create_and_sign_tx(CreateTxOptions(msgs=[msgVote], gas_adjustment=2))  # vote need more gas_adjustment
    print(f"TX:{tx}")
    result = terra.tx.broadcast(tx)
    print(f"RESULT:{result}")



main()
