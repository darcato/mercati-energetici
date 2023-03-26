"""Environmental Markets"""
from __future__ import annotations
from datetime import date

from .energy_markets import MercatiEnergetici


class MercatiAmbientali(MercatiEnergetici):
    """
    Environmental market.
    See: https://www.mercatoelettrico.org/En/Mercati/TEE/CosaSonoTee.aspx
    for an explanation of the markets.
    """

    async def markets(self) -> list[dict]:
        """Get environmental markets.

        Returns:
            A list of Python dictionaries like: [{"data": 20230323,
                                                  "mercato": "GO",
                                                  "volumi": 136917 }]
        """

        data = await self._request("/GetMercatiAmbientali")
        return data

    async def trading_results(self, market: str, day: date = None) -> list[dict]:
        """Get environmental market results.

        Args:
            market: The market to get results from.
            day: Date of the market. Default is today.

        Returns:
            A list of Python dictionaries like: [{"data": 20230323,
                                                  "mercato": "GO",
                                                  "tipologia": "Altro",
                                                  "periodo": "Altri Mesi 2022",
                                                  "prezzoRiferimento": 6.833425,
                                                  "prezzoMinimo": 6.1,
                                                  "prezzoMassimo": 9,
                                                  "volumi": 3115 },]
        """

        if day is None:
            day = date.today()
        data = await self._request(
            "/GetEsitiAmbiente/{year:4d}{month:02d}{day:02d}/{market}".format(
                day=day.day, month=day.month, year=day.year, market=market
            )
        )
        return data
