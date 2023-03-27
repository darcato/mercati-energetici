"""Test the environmental markets module."""
import pytest, pytest_asyncio
from datetime import date
from mercati_energetici import MercatiAmbientali
from mercati_energetici.exceptions import (
    MercatiEnergeticiRequestError,
    MercatiEnergeticiError,
)


@pytest_asyncio.fixture
async def mercati_ambientali():
    async with MercatiAmbientali() as ma:
        yield ma


@pytest.mark.asyncio
class TestMercatiAmbientali:
    async def test_general_condtions(self, mercati_ambientali):
        general_conditions = await mercati_ambientali.get_general_conditions()
        assert general_conditions is not None
        assert type(general_conditions) is dict
        assert set(["id", "lingua", "testo", "ultimoAggiornamento", "tipo"]) == set(
            general_conditions.keys()
        )
        assert general_conditions["tipo"] == "CG"
        assert general_conditions["lingua"] == "EN"
        general_conditions = await mercati_ambientali.get_general_conditions(language="en")
        assert general_conditions["lingua"] == "EN"
        general_conditions = await mercati_ambientali.get_general_conditions(language="IT")
        assert general_conditions["lingua"] == "IT"
        general_conditions = await mercati_ambientali.get_general_conditions(language="it")
        assert general_conditions["lingua"] == "IT"
        with pytest.raises(MercatiEnergeticiError):
            await mercati_ambientali.get_general_conditions(language="FR")

    async def test_disclaimer(self, mercati_ambientali):
        disclaimer = await mercati_ambientali.get_disclaimer()
        assert disclaimer is not None
        assert type(disclaimer) is dict
        assert set(["id", "lingua", "testo", "ultimoAggiornamento", "tipo"]) == set(
            disclaimer.keys()
        )
        assert disclaimer["tipo"] == "DI"
        assert disclaimer["lingua"] == "EN"
        disclaimer = await mercati_ambientali.get_disclaimer(language="en")
        assert disclaimer["lingua"] == "EN"
        disclaimer = await mercati_ambientali.get_disclaimer(language="IT")
        assert disclaimer["lingua"] == "IT"
        disclaimer = await mercati_ambientali.get_disclaimer(language="it")
        assert disclaimer["lingua"] == "IT"
        with pytest.raises(MercatiEnergeticiError):
            await mercati_ambientali.get_disclaimer(language="FR")

    async def test_markets(self, mercati_ambientali):
        markets = await mercati_ambientali.get_markets()
        assert markets is not None
        assert type(markets) is list
        assert len(markets) > 0
        for market in markets:
            assert type(market) is dict
            assert set(["data", "mercato", "volumi"]) == set(market.keys())

    async def test_trading_results(self, mercati_ambientali):
        results = await mercati_ambientali.get_trading_results("GO", day=date(2023, 3, 23))
        assert results is not None
        assert type(results) is list
        assert len(results) > 0
        for res in results:
            assert type(res) is dict
            assert set(
                [
                    "data",
                    "mercato",
                    "tipologia",
                    "periodo",
                    "prezzoRiferimento",
                    "prezzoMinimo",
                    "prezzoMassimo",
                    "volumi",
                ]
            ) == set(res.keys())
        with pytest.raises(MercatiEnergeticiRequestError):
            await mercati_ambientali.get_trading_results("NONEXISTENT")
        with pytest.raises(MercatiEnergeticiRequestError):
            await mercati_ambientali.get_trading_results("GO", day=date(2023, 3, 24))
