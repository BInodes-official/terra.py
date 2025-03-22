from terra_classic_sdk.client.lcd import LCDClient

terra = LCDClient(chain_id="columbus-5", url="https://api-lunc-lcd.binodes.com/")

res = terra.auth.account_info(address="terra1x46rqay4d3cssq8gxxvqz8xt6nwlz4td20k38v")
print(res)

res = terra.auth.account_info(address="terra1s2xpff7mj6jpxfyhr7pe25vt8puvgj4wyq8lz4")
print(res)
