from FTXwrapper.ftx import FTX


class FTXMethods(FTX):
    def __init__(self, account_name, api_file=None):
        super().__init__(account_name, api_file)

    async def authentication(self):
        res = await self.account_information(False)
        return res['success']

    async def get_price(self, market: str, side: str) -> float:
        res = await self.market()
        for _ in res:
            if _['name'] == market:
                if side == 'buy' or side == 'long':
                    return _['ask']
                elif side == 'sell' or side == 'short':
                    return _['bid']
                else:
                    raise ValueError('side is wrong')

    async def get_position(self, market: str):
        res = await self.positions()
        if type(res) == list:
            for _ in res:
                if _['future'] == market:
                    position_size = _['netSize']
                    liquidation_price = 0 if _['estimatedLiquidationPrice'] is None else _['estimatedLiquidationPrice']
                    return position_size, liquidation_price
        return 0, 0

    async def get_free_balance(self, market: str):
        balance = await self.balances()
        for _ in balance:
            if _['coin'] == market:
                return _['free'], _['usdValue']
        return 0, 0
