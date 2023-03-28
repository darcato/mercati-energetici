"""MercatiEnergetici base class"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
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
    """Base class for handling connections with the GME APP API."""

    session: ClientSession | None = None

    async def _request(
        self,
        uri: str,
    ) -> Any:
        """Handle a request to the GME APP API.

        A generic method for sending/handling HTTP requests done against
        the GME APP API.

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
            raise MercatiEnergeticiRequestError("Not Found: " + await response.text())

        response.raise_for_status()

        content_type = response.headers.get("Content-Type", "")
        if "application/json" not in content_type:
            text = await response.text()
            raise MercatiEnergeticiError(
                "Unexpected response from the GME API",
                {"Content-Type": content_type, "response": text},
            )

        data = await response.json()
        if data is None or not data:
            raise MercatiEnergeticiRequestError("Requested data not found")

        return data

    def _handle_date(self, day: date | str) -> str:
        """Check and format a date to the YYYYMMDD format.

        Args:
            day: The date to handle.

        Returns:
            A string in the format YYYYMMDD.
        """

        if day is None:
            day = date.today()
        elif isinstance(day, str):
            day = datetime.strptime(day, "%Y%m%d").date()
        elif not isinstance(day, date):
            raise TypeError(
                "day must be a datetime.date or a string in the format YYYYMMDD"
            )
        return day.strftime("%Y%m%d")

    async def get_general_conditions(self, language="EN") -> dict:
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

    async def get_disclaimer(self, language="EN") -> dict:
        """Get disclaimer.

        Args:
            language: 'EN' or 'IT'

        Returns:
            A Python dictionary like: {id: ...,
                                       lingua: ...,
                                       testo: ...,
                                       ultimoAggiornamento: ...,
                                       tipo: 'DI'}
        """

        data = await self._request(
            "/GetDisclaimer/{lang}".format(lang=language.strip().upper())
        )
        return data

    async def close(self) -> None:
        """Close client session."""
        if self.session and self.close_session:
            await self.session.close()

    async def __aenter__(self) -> MercatiEnergetici:
        """Async enter.

        Returns:
            The MercatiEnergetici object.
        """
        return self

    async def __aexit__(self, *_exc_info) -> None:
        """Async exit.

        Args:
            _exc_info: Exec type.
        """
        await self.close()
