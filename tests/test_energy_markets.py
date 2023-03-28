"""Test the energy markets base class."""
import pytest, pytest_asyncio
from datetime import date
from mercati_energetici.energy_markets import MercatiEnergetici
from mercati_energetici.exceptions import (
    MercatiEnergeticiRequestError,
    MercatiEnergeticiError,
)


@pytest_asyncio.fixture
async def mercati_energetici():
    async with MercatiEnergetici() as me:
        yield me


@pytest.mark.asyncio
class TestMercatiEnergetici:
    async def test_request(self, mercati_energetici):
        data = await mercati_energetici._request("/GetMercatiElettrici")
        assert data is not None
        with pytest.raises(MercatiEnergeticiRequestError):
            await mercati_energetici._request("/nonexistent")
    
    async def test_handle_date(self, mercati_energetici):
        assert mercati_energetici._handle_date(date(2020, 1, 1)) == "20200101"
        assert mercati_energetici._handle_date("20210203") == "20210203"
        with pytest.raises(ValueError):
            mercati_energetici._handle_date("2020-01-01")
        with pytest.raises(ValueError):
            mercati_energetici._handle_date("2020/01/01")
        with pytest.raises(TypeError):
            mercati_energetici._handle_date(20200101)

    async def test_general_condtions(self, mercati_energetici):
        general_conditions = await mercati_energetici.get_general_conditions()
        assert general_conditions is not None
        assert type(general_conditions) is dict
        assert set(["id", "lingua", "testo", "ultimoAggiornamento", "tipo"]) == set(
            general_conditions.keys()
        )
        assert general_conditions["tipo"] == "CG"
        assert general_conditions["lingua"] == "EN"
        general_conditions = await mercati_energetici.get_general_conditions(
            language="en"
        )
        assert general_conditions["lingua"] == "EN"
        general_conditions = await mercati_energetici.get_general_conditions(
            language="IT"
        )
        assert general_conditions["lingua"] == "IT"
        general_conditions = await mercati_energetici.get_general_conditions(
            language="it"
        )
        assert general_conditions["lingua"] == "IT"
        with pytest.raises(MercatiEnergeticiError):
            await mercati_energetici.get_general_conditions(language="FR")

    async def test_disclaimer(self, mercati_energetici):
        disclaimer = await mercati_energetici.get_disclaimer()
        assert disclaimer is not None
        assert type(disclaimer) is dict
        assert set(["id", "lingua", "testo", "ultimoAggiornamento", "tipo"]) == set(
            disclaimer.keys()
        )
        assert disclaimer["tipo"] == "DI"
        assert disclaimer["lingua"] == "EN"
        disclaimer = await mercati_energetici.get_disclaimer(language="en")
        assert disclaimer["lingua"] == "EN"
        disclaimer = await mercati_energetici.get_disclaimer(language="IT")
        assert disclaimer["lingua"] == "IT"
        disclaimer = await mercati_energetici.get_disclaimer(language="it")
        assert disclaimer["lingua"] == "IT"
        with pytest.raises(MercatiEnergeticiError):
            await mercati_energetici.get_disclaimer(language="FR")
