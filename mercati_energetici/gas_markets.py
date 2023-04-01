"""Gas Markets"""
from __future__ import annotations
from datetime import date

from .energy_markets import MercatiEnergetici


class MercatiGas(MercatiEnergetici):
    """
    Gas markets low level API wrapper.
    See: https://www.mercatoelettrico.org/en/Mercati/MGAS/MGas.aspx
    for an explanation of the markets.
    """

    async def get_markets(self) -> list[dict]:
        """Get gas markets.

        Returns:
            A list of Python dictionaries like: ``[{data: ...,
                                                  mercato: ...,
                                                  volumi: ...,
                                                  tipo: ...}]``
        """

        data = await self._request("/GetMercatiGas")
        return data

    async def get_continuous_trading_results(
        self, product: str, day: date | str = None
    ) -> list[dict]:
        """Get gas market results on the continuous trading mode.

        Args:
            product: the market-day to get results from
            day: Date of the market negotiation. Default is today. A string in
                    the format "YYYYMMDD" or a ``datetime.date`` object.

        Returns:
            A list of Python dictionaries like: ``[{ "data": 20230322,
                                                   "mercato": "MGP",
                                                   "prodotto": "MGP-2023-03-23",
                                                   "primoPrezzo": 45,
                                                   "ultimoPrezzo": 43.85,
                                                   "prezzoMinimo": 43.75,
                                                   "prezzoMassimo": 45.5,
                                                   "prezzoMedio": 44.430046,
                                                   "prezzoControllo": 44.638,
                                                   "volumiMw": 11112,
                                                   "volumiMwh": 266688 }]``
        """

        data = await self._request(
            "/GetEsitiGasContinuo/{date}/{product}".format(
                date=self._handle_date(day), product=product
            )
        )
        return data

    async def get_auction_trading_results(
        self, product: str, day: date | str = None
    ) -> list[dict]:
        """Get gas market results on the auction mode.

        Args:
            product: the market-day to get results from.
            day: Date of the market negotiations. Default is today. A string in
                    the format "YYYYMMDD" or a ``datetime.date`` object.

        Returns:
            A list of Python dictionaries like: ``[{"data": 20230323,
                                                  "mercato": "MGP",
                                                  "prodotto": "MGP-2023-03-24",
                                                  "prezzo": 45.351,
                                                  "volumiMw": 9124,
                                                  "volumiMwh": 218976,
                                                  "acquistiTso": 0,
                                                  "venditeTso": 218976 }]``
        """

        data = await self._request(
            "/GetEsitiGasAsta/{date}/{product}".format(
                date=self._handle_date(day), product=product
            )
        )
        return data

    async def get_stored_gas_trading_results(
        self, company: str, day: date | str = None
    ) -> list[dict]:
        """Get gas market results for the stored gas.

        Args:
            company: the market-company to get results from.
            day: Date of the market negotiations. Default is today. A string in
                    the format "YYYYMMDD" or a ``datetime.date`` object.

        Returns:
            A list of Python dictionaries like: ``[{"data": 20230322,
                                                  "dataFlusso": 20230322,
                                                  "impresaStoccaggio": "Stogit",
                                                  "tipologia": null,
                                                  "prezzo": 43.5,
                                                  "volumi": 16613.903,
                                                  "acquistiSrg": 6237.903,
                                                  "venditeSrg": 0 }]``
        """

        data = await self._request(
            "/GetEsitiGasMGS/{date}/{company}".format(
                date=self._handle_date(day),
                company=company.replace("MGS-", ""),
            )
        )
        return data
