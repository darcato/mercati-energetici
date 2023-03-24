from . import MercatiEnergetici
from dataclasses import dataclass
from datetime import date


@dataclass
class MercatoGas(MercatiEnergetici):
    """Gas market."""

    market: str = "MGP"

    async def results(self, day: date) -> dict:
        """Get gas market results.

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
            "/GetEsitiGas/{year:4d}{month:02d}{day:02d}".format(
                day=day.day, month=day.month, year=day.year
            )
        )
        return data