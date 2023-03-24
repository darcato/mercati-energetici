from . import MercatiEnergetici
from dataclasses import dataclass
from datetime import date


@dataclass
class MercatoAmbientale(MercatiEnergetici):
    """Environmental market."""

    market: str = "GO"

    async def environmental_markets(self) -> dict:
        """Get environmental markets.

        Returns:
            A list of Python dictionaries like: [{data: ...,
                                                  mercato: ...,
                                                  volumi: ...]
        """

        data = await self._request("/GetMercatiAmbientali")
        return data
    
    async def results(self, day: date) -> dict:
        """Get environmental market results.

        Args:
            date: Date of the market.

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
                day=day.day, month=day.month, year=day.year, market=self.market
            )
        )
        return data
