"""Environmental Markets"""
from __future__ import annotations
from datetime import date

from .energy_markets import MercatiEnergetici


class MercatiAmbientali(MercatiEnergetici):
    """
    Environmental market low level API wrapper.
    See: https://www.mercatoelettrico.org/En/Mercati/TEE/CosaSonoTee.aspx
    for an explanation of the markets.
    """

    async def get_markets(self) -> list[dict]:
        """Get environmental markets.

        Returns:
            A list of Python dictionaries like: [{"data": 20230323,
                                                  "mercato": "GO",
                                                  "volumi": 136917 }]
        """

        data = await self._request("/GetMercatiAmbientali")
        return data

    async def get_trading_results(
        self, market: str, day: date | str = None
    ) -> list[dict]:
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

        data = await self._request(
            "/GetEsitiAmbiente/{date}/{market}".format(
                date=self._handle_date(day), market=market
            )
        )
        return data
