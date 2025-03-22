from terra_classic_sdk.client.lcd import LCDClient

terra = LCDClient(chain_id="columbus-5", url="https://api-lunc-lcd.binodes.com/")
res = terra.gov.deposits(proposal_id=12164)
print(res)
res,page= terra.gov.votes(proposal_id=12161)
print(res)
