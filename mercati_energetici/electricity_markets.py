"""Electricity Markets"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from .energy_markets import MercatiEnergetici
from .exceptions import MercatiEnergeticiZoneError


@dataclass
class MercatiElettrici(MercatiEnergetici):
    """
    Electricity Markets.
    See: https://www.mercatoelettrico.org/En/Mercati/MercatoElettrico/IlMercatoElettrico.aspx
    for an explanation of the markets.
    """

    async def markets(self) -> dict:
        """Get electricity markets.

        Returns:
            A list of Python dictionaries like: [{data: ...,
                                                  mercato: ...,
                                                  volumi: ...}]
        """

        data = await self._request("/GetMercatiElettrici")
        return data

    async def all_prices(self, market: str, day: date = None) -> dict:
        """Get electricity prices in €/MWh for a specific day on all the market zones.

        Args:
            market: The market to get prices from.
            day: Get prices of this date. Default is today.

        Returns:
            A Python dictionary like: {zone: { hour : price_per_MWh }}
        """

        if day is None:
            day = date.today()
        data = await self._request(
            "/GetPrezziME/{year:4d}{month:02d}{day:02d}/{market}".format(
                day=day.day, month=day.month, year=day.year, market=market
            )
        )
        prices = {record["zona"]: {} for record in data if "zona" in record}
        for record in data:
            prices[record["zona"]][record["ora"] - 1] = record["prezzo"]
        return prices

    async def prices(self, market: str, day: date = None, zone: str = "PUN") -> dict:
        """Get electricity prices in €/MWh for a specific day and zone.

        Args:
            market: The market to get prices from.
            day: Get prices of this date. Default is today.
            zone: One of ["CALA","CNOR","CSUD","NORD","PUN","SARD","SICI","SUD"].
                  Default is "PUN" (whole Italy).

        Returns:
            A Python dictionary like: { hour : price_per_MWh }
        """

        prices = await self.all_prices(market, day)
        if zone not in prices.keys():
            raise MercatiEnergeticiZoneError(
                f"Zone '{zone}' not found. Available zones are: {list(prices.keys())}"
            )
        return prices[zone]

    async def all_volumes(self, market: str, day: date = None) -> tuple[dict, dict]:
        """Get bought and sold volume for a specific day on all the market zones.

        Args:
            market: The market to get volumes from.
            day: Get volumes of this date. Default is today.

        Returns:
            A Python dictionary like: {zone: { hour : MWh }}
        """

        if day is None:
            day = date.today()
        data = await self._request(
            "/GetQuantitaME/{year:4d}{month:02d}{day:02d}/{market}".format(
                day=day.day, month=day.month, year=day.year, market=market
            )
        )
        bought = {record["zona"]: {} for record in data if "zona" in record}
        sold = bought.copy()
        for record in data:
            bought[record["zona"]][record["ora"] - 1] = record["acquisti"]
            sold[record["zona"]][record["ora"] - 1] = record["vendite"]
        return bought, sold

    async def volumes(
        self, market: str, day: date = None, zone: str = "Totale"
    ) -> tuple[dict, dict]:
        """Get bought and sold volume for a specific day and zone.

        Args:
            market: The market to get volumes from.
            day: Get volumes of this date. Default is today.
            zone: One of ["CALA","CNOR","CSUD","NORD","SARD","SICI","SUD","Totale"].
                  Default is "Totale" (whole Italy).

        Returns:
            A Python dictionary like: { hour : MWh }
        """

        bought, sold = await self.all_volumes(market, day)
        if zone not in bought.keys():
            raise KeyError(
                f"Zone '{zone}' not found. Available zones are: {list(bought.keys())}"
            )
        return bought[zone], sold[zone]

    async def liquidity(self, day: date = None) -> dict:
        """Get liquidity of electricity markets.

        Args:
            day: Get liquidity of this date. Default is today.

        Returns:
            A Python dictionary like: {hour: liquidity}.
        """

        if day is None:
            day = date.today()
        data = await self._request(
            "/GetLiquidita/{year:4d}{month:02d}{day:02d}".format(
                day=day.day, month=day.month, year=day.year
            )
        )
        liquidity = {x["ora"] - 1: x["liquidita"] for x in data}
        return liquidity
