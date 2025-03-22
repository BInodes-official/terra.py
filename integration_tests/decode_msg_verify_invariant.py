from terra_classic_sdk.client.lcd import LCDClient


def main():
    terra = LCDClient(
        url="https://api-lunc-lcd.binodes.com",
        chain_id="columbus-5",
    )

    print(terra.tx.tx_infos_by_height(20440776))
    print(terra.tx.tx_infos_by_height(20440775))


main()
