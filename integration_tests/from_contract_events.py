from terra_classic_sdk.client.lcd import LCDClient
from terra_classic_sdk.util.contract import get_contract_events

tequila = LCDClient(url="https://api-lunc-lcd.binodes.com", chain_id="columbus-5")
tx_info = tequila.tx.tx_info(
    "44EB3B64FFE01A3839DBFD001ED6E03A29B5978011821BE4D95C8D7B498C8E2C"
)
print('tx_info',tx_info)
print(get_contract_events(tx_info))
