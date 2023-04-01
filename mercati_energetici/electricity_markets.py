"""Electricity Markets"""
from __future__ import annotations
from datetime import date

from .energy_markets import MercatiEnergetici
from .exceptions import MercatiEnergeticiZoneError


class MercatiElettrici(MercatiEnergetici):
    """
    Electricity Markets low level API wrapper.
    See: https://www.mercatoelettrico.org/En/Mercati/MercatoElettrico/IlMercatoElettrico.aspx
    for an explanation of the markets.
    """

    async def get_markets(self) -> dict:
        """Get electricity markets.

        Returns:
            A list of Python dictionaries like: ``[{data: ...,
                                                  mercato: ...,
                                                  volumi: ...}]``
        """

        data = await self._request("/GetMercatiElettrici")
        return data

    async def get_prices(self, market: str, day: date | str = None) -> list[dict]:
        """Get electricity prices in €/MWh for a specific day on all the market zones.

        Args:
            market: The market to get prices from.
            day: Get prices of this date. Default is today. A string in the format
                    "YYYYMMDD" or a ``datetime.date`` object.

        Returns:
            A Python dictionary like: ``[{"data": 20230323,
                                        "ora": 1,
                                        "mercato": "MGP",
                                        "zona": "CALA",
                                        "prezzo": 128.69 },]``
        """

        data = await self._request(
            "/GetPrezziME/{date}/{market}".format(
                date=self._handle_date(day), market=market
            )
        )
        return data

    async def get_volumes(self, market: str, day: date | str = None) -> list[dict]:
        """Get bought and sold volume for a specific day on all the market zones.

        Args:
            market: The market to get volumes from.
            day: Get volumes of this date. Default is today. A string in the format
                    "YYYYMMDD" or a ``datetime.date`` object.

        Returns:
            A Python dictionary like: ``[{ "data": 20230323,
                                         "ora": 1,
                                         "mercato": "MGP",
                                         "zona": "CALA",
                                         "acquisti": 482.198,
                                         "vendite": 1001.576 },]``
        """

        data = await self._request(
            "/GetQuantitaME/{date}/{market}".format(
                date=self._handle_date(day), market=market
            )
        )
        return data

    async def get_liquidity(self, day: date | str = None) -> dict:
        """Get liquidity of electricity markets.

        Args:
            day: Get liquidity of this date. Default is today. A string in the format
                    "YYYYMMDD" or a ``datetime.date`` object.

        Returns:
            A Python dictionary like: ``[{"data": 20230323,
                                        "ora": 1,
                                        "liquidita": 74.4741952239522 },]``
        """

        data = await self._request(
            "/GetLiquidita/{date}".format(date=self._handle_date(day))
        )
        return data


class MGP(MercatiElettrici):
    """
    Day-ahead Electricity Market.
    This is a higher level interface over MercatiElettrici for the MGP market and the PUN price.
    Hours are in [0 -> 23].
    """

    async def get_prices(self, day: date | str = None, zone: str = "PUN") -> dict:
        """Get electricity prices in €/MWh for a specific day and zone.

        Args:
            day: Get prices of this date. Default is today. A string in the format
                    "YYYYMMDD" or a ``datetime.date`` object.
            zone: One of ["CALA","CNOR","CSUD","NORD","PUN","SARD","SICI","SUD"].
                  Default is "PUN" (whole Italy).

        Returns:
            A Python dictionary like: ``{ hour : price_per_MWh }``
        """

        data = await super().get_prices("MGP", day)
        prices = {record["zona"]: {} for record in data if "zona" in record}
        for record in data:
            prices[record["zona"]][record["ora"] - 1] = record["prezzo"]
        if zone not in prices.keys():
            raise MercatiEnergeticiZoneError(
                f"Zone '{zone}' not found. Available zones are: {list(prices.keys())}"
            )
        return prices[zone]

    async def daily_pun(self, day: date | str = None) -> float:
        """Get the PUN price for a specific day.

        Args:
            day: Get prices of this date. Default is today. A string in the format
                    "YYYYMMDD" or a ``datetime.date`` object.

        Returns:
            The PUN price in €/MWh.
        """
        prices = await self.get_prices(day, zone="PUN")
        hourly_pun = list(prices.values())
        return sum(hourly_pun) / len(hourly_pun)

    async def get_volumes(
        self, day: date | str = None, zone: str = "Totale"
    ) -> tuple[dict, dict]:
        """Get bought and sold volume for a specific day and zone.

        Args:
            day: Get volumes of this date. Default is today. A string in the format
                    "YYYYMMDD" or a ``datetime.date`` object.
            zone: One of ["CALA","CNOR","CSUD","NORD","SARD","SICI","SUD","Totale"].
                  Default is "Totale" (whole Italy).

        Returns:
            Two Python dictionaries like: ``{ hour : MWh }``
        """

        data = await super().get_volumes("MGP", day)
        bought = {record["zona"]: {} for record in data if "zona" in record}
        sold = bought.copy()
        for record in data:
            bought[record["zona"]][record["ora"] - 1] = record["acquisti"]
            sold[record["zona"]][record["ora"] - 1] = record["vendite"]
        if zone not in bought.keys():
            raise MercatiEnergeticiZoneError(
                f"Zone '{zone}' not found. Available zones are: {list(bought.keys())}"
            )
        return bought[zone], sold[zone]

    async def get_liquidity(self, day: date | str = None) -> dict:
        """Get liquidity of electricity markets.

        Args:
            day: Get liquidity of this date. Default is today. A string in the format
                    "YYYYMMDD" or a ``datetime.date`` object.

        Returns:
            A Python dictionary like: ``{hour: liquidity}``.
        """
        data = await super().get_liquidity(day)
        liquidity = {x["ora"] - 1: x["liquidita"] for x in data}
        return liquidity
