"""Gas Markets"""
from __future__ import annotations
from datetime import date

from .energy_markets import MercatiEnergetici


class MercatiGas(MercatiEnergetici):
    """
    Gas markets.
    See: https://www.mercatoelettrico.org/en/Mercati/MGAS/MGas.aspx
    for an explanation of the markets.
    """

    async def markets(self) -> list[dict]:
        """Get gas markets.

        Returns:
            A list of Python dictionaries like: [{data: ...,
                                                  mercato: ...,
                                                  volumi: ...,
                                                  tipo: ...}]
        """

        data = await self._request("/GetMercatiGas")
        return data

    async def continuous_trading_results(
        self, market: str, day: date = None
    ) -> list[dict]:
        """Get gas market results on the continuous trading mode.

        Args:
            market: the market to get results from
            day: Date of the market negotiation. Default is today.

        Returns:
            A list of Python dictionaries like: [{ "data": 20230322,
                                                   "mercato": "MGP",
                                                   "prodotto": "MGP-2023-03-23",
                                                   "primoPrezzo": 45,
                                                   "ultimoPrezzo": 43.85,
                                                   "prezzoMinimo": 43.75,
                                                   "prezzoMassimo": 45.5,
                                                   "prezzoMedio": 44.430046,
                                                   "prezzoControllo": 44.638,
                                                   "volumiMw": 11112,
                                                   "volumiMwh": 266688 }]
        """

        if day is None:
            day = date.today()
        data = await self._request(
            "/GetEsitiGasContinuo/{year:4d}{month:02d}{day:02d}/{market}".format(
                day=day.day, month=day.month, year=day.year, market=market
            )
        )
        return data

    async def auction_trading_results(
        self, market: str, day: date = None
    ) -> list[dict]:
        """Get gas market results on the auction mode.

        Args:
            market: the market to get results from.
            day: Date of the market negotiations. Default is today.

        Returns:
            A list of Python dictionaries like: [{"data": 20230323,
                                                  "mercato": "MGP",
                                                  "prodotto": "MGP-2023-03-24",
                                                  "prezzo": 45.351,
                                                  "volumiMw": 9124,
                                                  "volumiMwh": 218976,
                                                  "acquistiTso": 0,
                                                  "venditeTso": 218976 }]
        """

        if day is None:
            day = date.today()
        data = await self._request(
            "/GetEsitiGasAsta/{year:4d}{month:02d}{day:02d}/{market}".format(
                day=day.day, month=day.month, year=day.year, market=market
            )
        )
        return data

    async def stored_gas_trading_results(
        self, market: str, day: date = None
    ) -> list[dict]:
        """Get gas market results for the stored gas.

        Args:
            market: the market to get results from.
            day: Date of the market negotiations. Default is today.

        Returns:
            A list of Python dictionaries like: [{"data": 20230322,
                                                  "dataFlusso": 20230322,
                                                  "impresaStoccaggio": "Stogit",
                                                  "tipologia": null,
                                                  "prezzo": 43.5,
                                                  "volumi": 16613.903,
                                                  "acquistiSrg": 6237.903,
                                                  "venditeSrg": 0 }]
        """

        if day is None:
            day = date.today()
        data = await self._request(
            "/GetEsitiGasMGS/{year:4d}{month:02d}{day:02d}/{market}".format(
                day=day.day, month=day.month, year=day.year, market=market
            )
        )
        return data
