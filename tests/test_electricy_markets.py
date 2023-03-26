"""Test the electricity markets module."""
import pytest, pytest_asyncio
from datetime import date
from mercati_energetici import MercatiElettrici
from mercati_energetici.exceptions import (
    MercatiEnergeticiZoneError,
    MercatiEnergeticiRequestError,
    MercatiEnergeticiError,
)


@pytest_asyncio.fixture
async def mercati_elettrici():
    async with MercatiElettrici() as me:
        yield me


@pytest.mark.asyncio
class TestMercatiElettrici:
    async def test_general_condtions(self, mercati_elettrici):
        general_conditions = await mercati_elettrici.general_conditions()
        assert general_conditions is not None
        assert type(general_conditions) is dict
        assert set(["id", "lingua", "testo", "ultimoAggiornamento", "tipo"]) == set(
            general_conditions.keys()
        )
        assert general_conditions["tipo"] == "CG"
        assert general_conditions["lingua"] == "EN"
        general_conditions = await mercati_elettrici.general_conditions(language="en")
        assert general_conditions["lingua"] == "EN"
        general_conditions = await mercati_elettrici.general_conditions(language="IT")
        assert general_conditions["lingua"] == "IT"
        general_conditions = await mercati_elettrici.general_conditions(language="it")
        assert general_conditions["lingua"] == "IT"
        with pytest.raises(MercatiEnergeticiError):
            await mercati_elettrici.general_conditions(language="FR")

    async def test_disclaimer(self, mercati_elettrici):
        disclaimer = await mercati_elettrici.disclaimer()
        assert disclaimer is not None
        assert type(disclaimer) is dict
        assert set(["id", "lingua", "testo", "ultimoAggiornamento", "tipo"]) == set(
            disclaimer.keys()
        )
        assert disclaimer["tipo"] == "DI"
        assert disclaimer["lingua"] == "EN"
        disclaimer = await mercati_elettrici.disclaimer(language="en")
        assert disclaimer["lingua"] == "EN"
        disclaimer = await mercati_elettrici.disclaimer(language="IT")
        assert disclaimer["lingua"] == "IT"
        disclaimer = await mercati_elettrici.disclaimer(language="it")
        assert disclaimer["lingua"] == "IT"
        with pytest.raises(MercatiEnergeticiError):
            await mercati_elettrici.disclaimer(language="FR")

    async def test_markets(self, mercati_elettrici):
        markets = await mercati_elettrici.markets()
        assert markets is not None
        assert type(markets) is list
        assert len(markets) > 0
        for market in markets:
            assert type(market) is dict
            assert set(("data", "mercato", "volumi")) == set(market.keys())

    async def test_all_prices(self, mercati_elettrici):
        all_prices = await mercati_elettrici.all_prices("MGP")
        assert all_prices is not None
        assert type(all_prices) is dict
        assert set(
            ["CALA", "CNOR", "CSUD", "NORD", "PUN", "SARD", "SICI", "SUD"]
        ) == set(all_prices.keys())
        for price in all_prices.values():
            assert type(price) is dict
            keys = set(price.keys())
            # Day can be between 23 and 25 hours long, if there is a daylight saving time change
            assert (
                keys == set(range(24))
                or keys == set(range(23))
                or keys == set(range(25))
            )
        with pytest.raises(MercatiEnergeticiRequestError):
            await mercati_elettrici.all_prices("NONEXISTENT")
        # Older dates are not available from the API
        with pytest.raises(MercatiEnergeticiRequestError):
            await mercati_elettrici.all_prices("MGP", date(2020, 1, 1))

    async def test_prices(self, mercati_elettrici):
        prices = await mercati_elettrici.prices("MGP")
        assert prices is not None
        assert type(prices) is dict
        keys = set(prices.keys())
        # Day can be between 23 and 25 hours long, if there is a daylight saving time change
        assert (
            keys == set(range(24))
            or keys == set(range(23))
            or keys == set(range(25))
        )
        with pytest.raises(MercatiEnergeticiRequestError):
            await mercati_elettrici.prices("NONEXISTENT")
        # Older dates are not available from the API
        with pytest.raises(MercatiEnergeticiRequestError):
            await mercati_elettrici.prices("MGP", date(2020, 1, 1))
        with pytest.raises(MercatiEnergeticiZoneError):
            await mercati_elettrici.prices("MGP", zone="NONEXISTENT")

    async def test_all_volumes(self, mercati_elettrici):
        all_volumes = await mercati_elettrici.all_volumes("MGP")
        assert all_volumes is not None
        assert type(all_volumes) is tuple
        assert len(all_volumes) == 2
        bought, sold = all_volumes
        assert type(bought) is dict
        assert type(sold) is dict
        assert (
            set(["CALA", "CNOR", "CSUD", "NORD", "SARD", "SICI", "SUD", "Totale"])
            == set(bought.keys())
            == set(sold.keys())
        )
        for price in list(bought.values()) + list(sold.values()):
            assert type(price) is dict
            keys = set(price.keys())
            # Day can be between 23 and 25 hours long, if there is a daylight saving time change
            assert (
                keys == set(range(24))
                or keys == set(range(23))
                or keys == set(range(25))
            )
        with pytest.raises(MercatiEnergeticiRequestError):
            await mercati_elettrici.all_volumes("NONEXISTENT")
        # Older dates are not available from the API
        with pytest.raises(MercatiEnergeticiRequestError):
            await mercati_elettrici.all_volumes("MGP", date(2020, 1, 1))

    async def test_volumes(self, mercati_elettrici):
        volumes = await mercati_elettrici.volumes("MGP")
        assert volumes is not None
        assert type(volumes) is tuple
        assert len(volumes) == 2
        bought, sold = volumes
        assert type(bought) is dict
        assert type(sold) is dict
        keys = set(bought.keys())
        # Day can be between 23 and 25 hours long, if there is a daylight saving time change
        assert (
            keys == set(range(24))
            or keys == set(range(23))
            or keys == set(range(25))
        )
        assert keys == set(sold.keys())
        with pytest.raises(MercatiEnergeticiRequestError):
            await mercati_elettrici.volumes("NONEXISTENT")
        # Older dates are not available from the API
        with pytest.raises(MercatiEnergeticiRequestError):
            await mercati_elettrici.volumes("MGP", date(2020, 1, 1))
        with pytest.raises(MercatiEnergeticiZoneError):
            await mercati_elettrici.volumes("MGP", zone="NONEXISTENT")

    async def test_liquidity(self, mercati_elettrici):
        liquidity = await mercati_elettrici.liquidity()
        assert liquidity is not None
        assert type(liquidity) is dict
        keys = set(liquidity.keys())
        # Day can be between 23 and 25 hours long, if there is a daylight saving time change
        assert (
            keys == set(range(24))
            or keys == set(range(23))
            or keys == set(range(25))
        )
        # Older dates are not available from the API
        with pytest.raises(MercatiEnergeticiRequestError):
            await mercati_elettrici.liquidity(date(2020, 1, 1))
