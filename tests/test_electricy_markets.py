"""Test the electricity markets module."""
import pytest, pytest_asyncio
from datetime import date
from mercati_energetici import MercatiElettrici, MGP
from mercati_energetici.exceptions import (
    MercatiEnergeticiZoneError,
    MercatiEnergeticiRequestError,
    MercatiEnergeticiError,
)


@pytest_asyncio.fixture
async def mercati_elettrici():
    async with MercatiElettrici() as me:
        yield me

@pytest_asyncio.fixture
async def mgp():
    async with MGP() as mgp:
        yield mgp


@pytest.mark.asyncio
class TestMercatiElettrici:
    async def test_general_condtions(self, mercati_elettrici):
        general_conditions = await mercati_elettrici.get_general_conditions()
        assert general_conditions is not None
        assert type(general_conditions) is dict
        assert set(["id", "lingua", "testo", "ultimoAggiornamento", "tipo"]) == set(
            general_conditions.keys()
        )
        assert general_conditions["tipo"] == "CG"
        assert general_conditions["lingua"] == "EN"
        general_conditions = await mercati_elettrici.get_general_conditions(language="en")
        assert general_conditions["lingua"] == "EN"
        general_conditions = await mercati_elettrici.get_general_conditions(language="IT")
        assert general_conditions["lingua"] == "IT"
        general_conditions = await mercati_elettrici.get_general_conditions(language="it")
        assert general_conditions["lingua"] == "IT"
        with pytest.raises(MercatiEnergeticiError):
            await mercati_elettrici.get_general_conditions(language="FR")

    async def test_disclaimer(self, mercati_elettrici):
        disclaimer = await mercati_elettrici.get_disclaimer()
        assert disclaimer is not None
        assert type(disclaimer) is dict
        assert set(["id", "lingua", "testo", "ultimoAggiornamento", "tipo"]) == set(
            disclaimer.keys()
        )
        assert disclaimer["tipo"] == "DI"
        assert disclaimer["lingua"] == "EN"
        disclaimer = await mercati_elettrici.get_disclaimer(language="en")
        assert disclaimer["lingua"] == "EN"
        disclaimer = await mercati_elettrici.get_disclaimer(language="IT")
        assert disclaimer["lingua"] == "IT"
        disclaimer = await mercati_elettrici.get_disclaimer(language="it")
        assert disclaimer["lingua"] == "IT"
        with pytest.raises(MercatiEnergeticiError):
            await mercati_elettrici.get_disclaimer(language="FR")

    async def test_markets(self, mercati_elettrici):
        markets = await mercati_elettrici.get_markets()
        assert markets is not None
        assert type(markets) is list
        assert len(markets) > 0
        for market in markets:
            assert type(market) is dict
            assert set(("data", "mercato", "volumi")) == set(market.keys())

    async def test_prices(self, mercati_elettrici):
        prices = await mercati_elettrici.get_prices("MGP")
        assert prices is not None
        assert type(prices) is list
        assert len(prices) > 0
        for price in prices:
            assert type(price) is dict
            assert set(("data", "ora", "mercato", "zona", "prezzo")) == set(price.keys())
            assert price["data"] == int(date.today().strftime("%Y%m%d"))
            assert price["mercato"] == "MGP"
        with pytest.raises(MercatiEnergeticiRequestError):
            await mercati_elettrici.get_prices("NONEXISTENT")
        # Older dates are not available from the API
        with pytest.raises(MercatiEnergeticiRequestError):
            await mercati_elettrici.get_prices("MGP", date(2020, 1, 1))

    async def test_volumes(self, mercati_elettrici):
        volumes = await mercati_elettrici.get_volumes("MGP")
        assert volumes is not None
        assert type(volumes) is list
        assert len(volumes) > 0
        for volume in volumes:
            assert type(volume) is dict
            assert set(("data", "ora", "mercato", "zona", "acquisti", "vendite")) == set(volume.keys())
            assert volume["data"] == int(date.today().strftime("%Y%m%d"))
            assert volume["mercato"] == "MGP"
        with pytest.raises(MercatiEnergeticiRequestError):
            await mercati_elettrici.get_volumes("NONEXISTENT")
        # Older dates are not available from the API
        with pytest.raises(MercatiEnergeticiRequestError):
            await mercati_elettrici.get_volumes("MGP", date(2020, 1, 1))

    async def test_liquidity(self, mercati_elettrici):
        liquidity = await mercati_elettrici.get_liquidity()
        assert liquidity is not None
        assert type(liquidity) is list
        # Day can be between 23 and 25 hours long, if there is a daylight saving time change
        assert len(liquidity) >= 23 and len(liquidity) <= 25
        for hour in liquidity:
            assert type(hour) is dict
            assert set(("data", "ora", "liquidita")) == set(hour.keys())
            assert hour["data"] == int(date.today().strftime("%Y%m%d"))
        # Older dates are not available from the API
        with pytest.raises(MercatiEnergeticiRequestError):
            await mercati_elettrici.get_liquidity(date(2020, 1, 1))

@pytest.mark.asyncio
class TestMGP:
    async def test_prices(self, mgp):
        prices = await mgp.get_prices()
        assert prices is not None
        assert type(prices) is dict
        keys = set(prices.keys())
        # Day can be between 23 and 25 hours long, if there is a daylight saving time change
        assert (
            keys == set(range(24)) or keys == set(range(23)) or keys == set(range(25))
        )
        # Older dates are not available from the API
        with pytest.raises(MercatiEnergeticiRequestError):
            await mgp.get_prices(date(2020, 1, 1))
        with pytest.raises(MercatiEnergeticiZoneError):
            await mgp.get_prices(zone="NONEXISTENT")

    async def test_volumes(self, mgp):
        volumes = await mgp.get_volumes()
        assert volumes is not None
        assert type(volumes) is tuple
        assert len(volumes) == 2
        bought, sold = volumes
        assert type(bought) is dict
        assert type(sold) is dict
        keys = set(bought.keys())
        # Day can be between 23 and 25 hours long, if there is a daylight saving time change
        assert (
            keys == set(range(24)) or keys == set(range(23)) or keys == set(range(25))
        )
        assert keys == set(sold.keys())
        # Older dates are not available from the API
        with pytest.raises(MercatiEnergeticiRequestError):
            await mgp.get_volumes(date(2020, 1, 1))
        with pytest.raises(MercatiEnergeticiZoneError):
            await mgp.get_volumes(zone="NONEXISTENT")

    async def test_liquidity(self, mgp):
        liquidity = await mgp.get_liquidity()
        assert liquidity is not None
        assert type(liquidity) is dict
        keys = set(liquidity.keys())
        # Day can be between 23 and 25 hours long, if there is a daylight saving time change
        assert (
            keys == set(range(24)) or keys == set(range(23)) or keys == set(range(25))
        )
        # Older dates are not available from the API
        with pytest.raises(MercatiEnergeticiRequestError):
            await mgp.get_liquidity(date(2020, 1, 1))