from terra_classic_sdk.client.lcd import LCDClient

terra = LCDClient(chain_id="columbus-5", url="https://api-lunc-lcd.binodes.com")
print(
    terra.distribution.rewards(
        "terra1s2xpff7mj6jpxfyhr7pe25vt8puvgj4wyq8lz4"
    )
)
