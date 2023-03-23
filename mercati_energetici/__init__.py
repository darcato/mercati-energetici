"""Asynchronous Python client for the GME API."""
from __future__ import annotations

from collections.abc import Mapping
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
class MercatoEnergetico:
    """Base class for handling connections with the GME API."""

    session: ClientSession | None = None

    async def _request(
        self,
        uri: str,
        *,
        params: Mapping[str, str] | None = None,
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
            params=params,
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

    async def close(self) -> None:
        """Close open client session."""
        if self.session and self.close_session:
            await self.session.close()

    async def __aenter__(self) -> MercatoEnergetico:
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
class MercatoElettrico(MercatoEnergetico):
    """Main class for handling connections with the GME API."""

    market: str = "MGP"

    async def get_all_prices(self, day: date = None) -> dict:
        """Get prices for a specific day on all the market zones.

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

    async def get_prices(self, day: date = None, zone: str = "PUN") -> dict:
        """Get prices for a specific day and zone.

        Args:
            day: get prices of this date
            zone: one of ["NORD", "SUD", ...]

        Returns:
            A Python dictionary like: { hour : price_per_MWh }
        """

        prices = await self.get_all_prices(day)
        if zone not in prices.keys():
            raise KeyError(
                f"Zone '{zone}' not found. Available zones are: {list(prices.keys())}"
            )
        return prices[zone]
