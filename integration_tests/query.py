import asyncio
import base64
from pathlib import Path

from terra_classic_sdk.client.lcd import LCDClient
from terra_classic_sdk.core import Coins
from terra_classic_sdk.core.bank import MsgSend
from terra_classic_sdk.util.contract import get_code_id


def main():
    terra = LCDClient(
        url="https://api-lunc-lcd.binodes.com/",
        chain_id="columbus-5",
    )

    result = terra.tx.tx_infos_by_height(None)
    print(result)


main()
