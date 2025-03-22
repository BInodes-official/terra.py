from terra_classic_sdk.client.lcd import LCDClient
from terra_classic_sdk.client.lcd.params import PaginationOptions

terra = LCDClient(
    url="https://api-lunc-lcd.binodes.com",
    chain_id="columbus-5",
)

pagOpt = PaginationOptions(limit=2, count_total=True)


def test_tx_info():
    result = terra.tx.tx_info(
        "3826084ADC5AE7BD0BFE932E698C0CA45A43C2B6D9FCAD90D23891932E86DE28"
    )
    assert result is not None


def test_search():
    result = terra.tx.search(
        [
            ("tx.height", 22230767),
            ("message.sender", "terra1s2xpff7mj6jpxfyhr7pe25vt8puvgj4wyq8lz4"),
        ]
    )
    assert result is not None
    assert len(result) > 0


def test_tx_infos_by_height():
    result = terra.tx.tx_infos_by_height()
    assert result is not None


def test_tx_infos_by_height_with_height():
    result = terra.tx.tx_infos_by_height(22360259)
    assert result is not None
