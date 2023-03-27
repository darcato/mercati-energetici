"""Test the gas markets module."""
import pytest, pytest_asyncio
from datetime import date, datetime
from mercati_energetici import MercatiGas
from mercati_energetici.exceptions import (
    MercatiEnergeticiZoneError,
    MercatiEnergeticiRequestError,
    MercatiEnergeticiError,
)


@pytest_asyncio.fixture
async def mercati_gas():
    async with MercatiGas() as mg:
        yield mg


@pytest.mark.asyncio
class TestMercatiGas:
    async def test_general_condtions(self, mercati_gas):
        general_conditions = await mercati_gas.get_general_conditions()
        assert general_conditions is not None
        assert type(general_conditions) is dict
        assert set(["id", "lingua", "testo", "ultimoAggiornamento", "tipo"]) == set(
            general_conditions.keys()
        )
        assert general_conditions["tipo"] == "CG"
        assert general_conditions["lingua"] == "EN"
        general_conditions = await mercati_gas.get_general_conditions(language="en")
        assert general_conditions["lingua"] == "EN"
        general_conditions = await mercati_gas.get_general_conditions(language="IT")
        assert general_conditions["lingua"] == "IT"
        general_conditions = await mercati_gas.get_general_conditions(language="it")
        assert general_conditions["lingua"] == "IT"
        with pytest.raises(MercatiEnergeticiError):
            await mercati_gas.get_general_conditions(language="FR")

    async def test_disclaimer(self, mercati_gas):
        disclaimer = await mercati_gas.get_disclaimer()
        assert disclaimer is not None
        assert type(disclaimer) is dict
        assert set(["id", "lingua", "testo", "ultimoAggiornamento", "tipo"]) == set(
            disclaimer.keys()
        )
        assert disclaimer["tipo"] == "DI"
        assert disclaimer["lingua"] == "EN"
        disclaimer = await mercati_gas.get_disclaimer(language="en")
        assert disclaimer["lingua"] == "EN"
        disclaimer = await mercati_gas.get_disclaimer(language="IT")
        assert disclaimer["lingua"] == "IT"
        disclaimer = await mercati_gas.get_disclaimer(language="it")
        assert disclaimer["lingua"] == "IT"
        with pytest.raises(MercatiEnergeticiError):
            await mercati_gas.get_disclaimer(language="FR")

    async def test_markets(self, mercati_gas):
        markets = await mercati_gas.get_markets()
        assert markets is not None
        assert type(markets) is list
        assert len(markets) > 0
        for market in markets:
            assert type(market) is dict
            assert set(("data", "prodotto", "tipo", "volumi")) == set(market.keys())

    async def test_continuous_trading_results(self, mercati_gas):
        markets = await mercati_gas.get_markets()
        # Get the first continuous market (C)
        markets = filter(lambda m: m["tipo"] == "C", markets)
        for market in markets:
            results = await mercati_gas.get_continuous_trading_results(
                market["prodotto"],
                day=datetime.strptime(str(market["data"]), "%Y%m%d").date(),
            )
            assert results is not None
            assert type(results) is list
            assert len(results) > 0
            for result in results:
                assert type(result) is dict
                assert set(
                    (
                        "data",
                        "mercato",
                        "prodotto",
                        "primoPrezzo",
                        "ultimoPrezzo",
                        "prezzoMinimo",
                        "prezzoMassimo",
                        "prezzoMedio",
                        "prezzoControllo",
                        "volumiMw",
                        "volumiMwh",
                    )
                ) == set(result.keys())
                assert result["data"] == market["data"]
                assert result["prodotto"] == market["prodotto"]
        with pytest.raises(TypeError):
            await mercati_gas.get_continuous_trading_results()
        with pytest.raises(MercatiEnergeticiRequestError):
            await mercati_gas.get_continuous_trading_results("NONEXISTENT")

    async def test_auction_trading_results(self, mercati_gas):
        markets = await mercati_gas.get_markets()
        # Look for a market of type A (auction) and not MGS (gas storage)
        markets = filter(
                lambda m: m["tipo"] == "A" and not m["prodotto"].startswith("MGS"),
                markets,
            )
        for market in markets:
            results = await mercati_gas.get_auction_trading_results(
                market["prodotto"],
                day=datetime.strptime(str(market["data"]), "%Y%m%d").date(),
            )
            assert results is not None
            assert type(results) is list
            assert len(results) > 0
            for result in results:
                assert type(result) is dict
                assert set(
                    (
                        "data",
                        "mercato",
                        "prodotto",
                        "prezzo",
                        "volumiMw",
                        "volumiMwh",
                        "venditeTso",
                        "acquistiTso",
                    )
                ) == set(result.keys())
                assert result["data"] == market["data"]
                assert result["prodotto"] == market["prodotto"]
        with pytest.raises(TypeError):
            await mercati_gas.get_auction_trading_results()
        with pytest.raises(MercatiEnergeticiRequestError):
            await mercati_gas.get_auction_trading_results("NONEXISTENT")

    async def test_stored_gas_trading_results(self, mercati_gas):
        markets = await mercati_gas.get_markets()
        # Look for a market of type A (auction) on the MGS (gas storage)
        markets = filter(
            lambda m: m["tipo"] == "A" and m["prodotto"].startswith("MGS"), markets
        )
        for market in markets:
            results = await mercati_gas.get_stored_gas_trading_results(
                market["prodotto"],
                day=datetime.strptime(str(market["data"]), "%Y%m%d").date(),
            )
            assert results is not None
            assert type(results) is list
            assert len(results) > 0
            for result in results:
                assert type(result) is dict
                assert set(
                    (
                        "data",
                        "dataFlusso",
                        "impresaStoccaggio",
                        "tipologia",
                        "prezzo",
                        "volumi",
                        "acquistiSrg",
                        "venditeSrg",
                    )
                ) == set(result.keys())
                assert result["data"] == market["data"]
                assert result["impresaStoccaggio"] == market["prodotto"].replace("MGS-", "")
        with pytest.raises(TypeError):
            await mercati_gas.get_stored_gas_trading_results()
        with pytest.raises(MercatiEnergeticiRequestError):
            await mercati_gas.get_stored_gas_trading_results("NONEXISTENT")
