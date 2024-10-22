from xml.etree import ElementTree

from aiohttp import ClientSession

from exchange_rate_bot.usecases.protocols.currency import (
    CurrencyError,
    CurrencyInfo,
    CurrencyProtocol,
)


class CentralBankAdapter(CurrencyProtocol):
    def __init__(self, session: ClientSession):
        self.session = session

    async def get_actual_rates(self) -> list[CurrencyInfo]:
        async with self.session.get('/scripts/XML_daily.asp') as response:
            if response.status != 200:
                raise CurrencyError
            content = await response.text()
        tree = ElementTree.fromstring(content)
        return [
            CurrencyInfo.model_validate(
                {
                    'num_code': currency.find('NumCode').text,
                    'char_code': currency.find('CharCode').text,
                    'nominal': currency.find('Nominal').text,
                    'name': currency.find('Name').text,
                    'value': currency.find('Value').text.replace(',', '.'),
                    'vunit_rate': currency.find('VunitRate').text.replace(',', '.'),
                },
            )
            for currency in tree
        ]
