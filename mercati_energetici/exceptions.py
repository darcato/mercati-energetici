"""Exceptions for mercati_energetici."""


class MercatiEnergeticiError(Exception):
    """Generic mercati_energetici exception."""


class MercatiEnergeticiConnectionError(MercatiEnergeticiError):
    """GME API connection exception."""


class MercatiEnergeticiRequestError(MercatiEnergeticiError):
    """GME API wrong request input variables."""

    def __init__(self, data: dict) -> None:
        super().__init__(f'{data["text"]} (error {data["code"]})')
        self.code = data["code"]
