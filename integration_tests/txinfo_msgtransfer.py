from terra_classic_sdk.client.lcd import LCDClient

if __name__ == "__main__":
    client = LCDClient(url="https://api-lunc-lcd.binodes.com", chain_id="columbus-5")

    res=client.tx.tx_info(
        "70D0FBF179D5FBEAFF892DEEA5090D7DE04077F22103F12B91B718087E44D425"
    )
    print(res.logs[0].events)
