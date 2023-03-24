from . import MercatiEnergetici
from dataclasses import dataclass
from datetime import date


@dataclass
class MercatoElettrico(MercatiEnergetici):
    """Electricity Market."""

    market: str = "MGP"

    async def electricity_markets(self) -> dict:
        """Get electricity markets.

        Returns:
            A list of Python dictionaries like: [{data: ...,
                                                  mercato: ...,
                                                  volumi: ...}]
        """

        data = await self._request("/GetMercatiElettrici")
        return data

    async def all_prices(self, day: date = None) -> dict:
        """Get electricity prices for a specific day on all the market zones.

        Args:
            day: get prices of this date

        Returns:
            A Python dictionary like: {zone: { hour : price_per_MWh }}
        """

        if day is None:
            day = date.today()
        data = await self._request(
            "/GetPrezziME/{year:4d}{month:02d}{day:02d}/{market}".format(
                day=day.day, month=day.month, year=day.year, market=self.market
            )
        )
        prices = {record["zona"]: {} for record in data if "zona" in record}
        for record in data:
            prices[record["zona"]][record["ora"] - 1] = record["prezzo"]
        return prices

    async def prices(self, day: date = None, zone: str = "PUN") -> dict:
        """Get electricity prices for a specific day and zone.

        Args:
            day: get prices of this date
            zone: one of ["NORD", "SUD", ...]

        Returns:
            A Python dictionary like: { hour : price_per_MWh }
        """

        prices = await self.all_prices(day)
        if zone not in prices.keys():
            raise KeyError(
                f"Zone '{zone}' not found. Available zones are: {list(prices.keys())}"
            )
        return prices[zone]

    async def all_volumes(self, day: date = None) -> tuple[dict, dict]:
        """Get bought and sold volume for a specific day on all the market zones.

        Args:
            day: get volumes of this date

        Returns:
            A Python dictionary like: {zone: { hour : MWh }}
        """

        if day is None:
            day = date.today()
        data = await self._request(
            "/GetQuantitaME/{year:4d}{month:02d}{day:02d}/{market}".format(
                day=day.day, month=day.month, year=day.year, market=self.market
            )
        )
        bought = {record["zona"]: {} for record in data if "zona" in record}
        sold = bought.copy()
        for record in data:
            bought[record["zona"]][record["ora"] - 1] = record["acquisti"]
            sold[record["zona"]][record["ora"] - 1] = record["vendite"]
        return bought, sold

    async def volumes(
        self, day: date = None, zone: str = "Totale"
    ) -> tuple[dict, dict]:
        """Get bought and sold volume for a specific day and zone.

        Args:
            day: get volumes of this date
            zone: one of ["NORD", "SUD", ...]

        Returns:
            A Python dictionary like: { hour : MWh }
        """

        bought, sold = await self.all_quantities(day)
        if zone not in bought.keys():
            raise KeyError(
                f"Zone '{zone}' not found. Available zones are: {list(bought.keys())}"
            )
        return bought[zone], sold[zone]

    async def liquidity(self, day: date = None) -> dict:
        """Get liquidity of electricity markets.

        Args:
            day: get liquidity of this date

        Returns:
            A Python dictionary like: {ora: liquidity}.
        """

        if day is None:
            day = date.today()
        data = await self._request(
            "/GetLiquidita/{year:4d}{month:02d}{day:02d}".format(
                day=day.day, month=day.month, year=day.year
            )
        )
        liquidity = {x["ora"]: x["liquidita"] for x in data}
        return liquidity
