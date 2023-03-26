"""Exceptions for mercati_energetici."""


class MercatiEnergeticiError(Exception):
    """Generic mercati_energetici exception."""


class MercatiEnergeticiConnectionError(MercatiEnergeticiError):
    """GME APP API connection exception."""


class MercatiEnergeticiZoneError(MercatiEnergeticiError):
    """Zone not found exception."""


class MercatiEnergeticiRequestError(MercatiEnergeticiError):
    """GME APP API wrong request input variables."""
