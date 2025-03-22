from terra_classic_sdk.client.lcd import LCDClient

terra = LCDClient(
    chain_id="columbus-5",
    url="https://api-lunc-lcd.binodes.com/",
)
res = terra.tendermint.node_info()
print(res)
