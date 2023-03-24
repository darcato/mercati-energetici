"""Asynchronous Python client for the GME API."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Any

from aiohttp import ClientSession
from yarl import URL

from .exceptions import (
    MercatiEnergeticiError,
    MercatiEnergeticiConnectionError,
    MercatiEnergeticiRequestError,
)


@dataclass
class MercatiEnergetici:
    """Base class for handling connections with the GME API."""

    session: ClientSession | None = None

    async def _request(
        self,
        uri: str,
    ) -> dict[str, Any]:
        """Handle a request to the GME API.

        A generic method for sending/handling HTTP requests done against
        the GME API.

        Args:
            uri: Request URI, for example, '/GetMarkets'

        Returns:
            A Python dictionary (JSON decoded) with the response from
            the GME API.

        Raises:
            MercatiEnergeticiConnectionError: An error occurred while communicating
                with the GME API.
            MercatiEnergeticiError: Received an unexpected response from the
                GME API.
            MercatiEnergeticiRequestError: There is something wrong with the
                variables used in the request.
        """

        gme_app_host = "app.mercatienergetici.org"
        url = URL.build(scheme="https", host=gme_app_host)
        url = url.join(URL(uri))

        if self.session is None:
            self.session = ClientSession()
            self.close_session = True

        response = await self.session.request(
            "GET",
            url,
            headers={
                "Host": gme_app_host,
                "x-requested-with": "darcato/mercati-energetici",
            },
        )

        if response.status == 502:
            raise MercatiEnergeticiConnectionError("The GME API is unreachable, ")

        if response.status == 400:
            data = await response.json()
            raise MercatiEnergeticiRequestError(data["message"])

        response.raise_for_status()

        content_type = response.headers.get("Content-Type", "")
        if "application/json" not in content_type:
            text = await response.text()
            raise MercatiEnergeticiError(
                "Unexpected response from the GME API",
                {"Content-Type": content_type, "response": text},
            )

        return await response.json()

    async def general_conditions(self, language="EN") -> dict:
        """Get general usage conditions.

        Args:
            language: 'EN' or 'IT'

        Returns:
            A Python dictionary like: {id: ...,
                                       lingua: ...,
                                       testo: ...,
                                       ultimoAggiornamento: ...,
                                       tipo: 'CG'}
        """

        data = await self._request(
            "/GetCondizioniGenerali/{lang}".format(lang=language.strip().upper())
        )
        return data

    async def disclaimer(self, language="EN") -> dict:
        """Get disclaimer.

        Args:
            language: 'EN' or 'IT'

        Returns:
            A Python dictionary like: {id: ...,
                                       lingua: ...,
                                       testo: ...,
                                       ultimoAggiornamento: ...,
                                       tipo: 'CG'}
        """

        data = await self._request(
            "/GetDisclaimer/{lang}".format(lang=language.strip().upper())
        )
        return data

    async def electricity_markets(self) -> dict:
        """Get electricity markets.

        Returns:
            A list of Python dictionaries like: [{data: ...,
                                                  mercato: ...,
                                                  volumi: ...}]
        """

        data = await self._request("/GetMercatiElettrici")
        return data

    async def gas_markets(self) -> dict:
        """Get gas markets.

        Returns:
            A list of Python dictionaries like: [{data: ...,
                                                  mercato: ...,
                                                  volumi: ...,
                                                  tipo: ...}]
        """

        data = await self._request("/GetMercatiGas")
        return data
    
    async def environmental_markets(self) -> dict:
        """Get environmental markets.

        Returns:
            A list of Python dictionaries like: [{data: ...,
                                                  mercato: ...,
                                                  volumi: ...]
        """

        data = await self._request("/GetMercatiAmbientali")
        return data

    async def close(self) -> None:
        """Close client session."""
        if self.session and self.close_session:
            await self.session.close()

    async def __aenter__(self) -> MercatiEnergetici:
        """Async enter.

        Returns:
            The MercatoEnergetico object.
        """
        return self

    async def __aexit__(self, *_exc_info) -> None:
        """Async exit.

        Args:
            _exc_info: Exec type.
        """
        await self.close()


@dataclass
class MercatoElettrico(MercatiEnergetici):
    """Electricity Market."""

    market: str = "MGP"

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
