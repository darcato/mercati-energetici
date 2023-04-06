# Getting started

The library exposes three low level classes to access the GME API: ``MercatiElettrici``, ``MercatiGas`` and ``MercatiAmbientali``. A further class, ``MGP``, offers a higher level interface over the day-ahead electricity market. Those can be imported from the ``mercati_energetici`` module like this:

```python
from mercati_energetici import MercatiElettrici, MercatiGas, MercatiAmbientali, MGP
```

Since the library is asynchronous, it is required to use it within an ``async`` function. For example:

```python
import asyncio
from mercati_energetici import MGP

async def main():
    async with MGP() as mgp:

        # Get average PUN price
        print("PUN avg: ", await mgp.daily_pun(date(2023, 3, 28)))

if __name__ == "__main__":
    asyncio.run(main())
```

The dates are accepted as ``datetime.date`` objects or a ``str`` in the format ``YYYYMMDD`` like ``20230328`` for 28 March 2023. The default date is today.

## MGP

[What is the day-ahead market? (Mercato del Giorno Prima, MGP)](https://www.mercatoelettrico.org/en/Mercati/MercatoElettrico/MPE.aspx)

This class can be used to retrieve the average price of electricity in Italy (PUN) for a specific date. It also allows to retrieve hourly prices, volumes and liquidity of the day-ahead market. 

```python
async with MGP() as mgp:

    # By using this library, you agree to the terms of use of GME API
    # which can be obtained with:
    print(await mgp.get_general_conditions())

    # Also, be aware of the following disclaimer from GME
    print(await mgp.get_disclaimer())

    # Get average PUN price
    print("PUN avg: ", await mgp.daily_pun(date(2023, 3, 28)))

    # Get PUN hourly prices
    print(await mgp.get_prices(date(2023, 3, 28)))

    # Get hourly volumes
    print(await mgp.get_volumes(date(2023, 3, 28)))

    # Get market liquidity
    print(await mgp.get_liquidity('20230328'))
```

The last three methods return a dictionary like:

```python
{
    0: 131.77,
    1: 120.0,
    2: 114.63154,
    3: 102.11652,
    4: 95.8797,
    5: 109.69628,
    6: 132.8,
    7: 158.1019,
    8: 167.17296,
    9: 169.0,
    ...
}
```

with hours as keys and the price [EUR/MWh] / volume [MWh] / liquidity [%] as values.

By default, the prices and volumes refer to the whole Italy, but it is possible to specify a specific region (``CALA``, ``CNOR``, ``CSUD``, ``NORD``, ``PUN``, ``SARD``, ``SICI``, ``SUD``) like this:

```python
await mgp.get_prices(date(2023, 3, 28), zone="SUD")
```

## MercatiElettrici

This class wraps the API for the day-ahead electricity market. It allows to retrieve hourly prices, volumes and liquidity of the day-ahead market exactly as served by GME. For an explaination of the markets see [the GME website](https://www.mercatoelettrico.org/En/Mercati/MercatoElettrico/IlMercatoElettrico.aspx).

First of all you should accept the terms of use of GME API:

```python
async with MercatiElettrici() as mercati_elettrici:
    print(await mercati_elettrici.get_general_conditions())
    print(await mercati_elettrici.get_disclaimer())
```

After that, you can retrieve the available markets with:

```python
await mercati_elettrici.get_markets()
# Returns:
[
    {"data": 20230405, "mercato": "MGP", "volumi": 800121.431},
    {"data": 20230405, "mercato": "MI-A1", "volumi": 42020.197},
    {"data": 20230404, "mercato": "MI-A2", "volumi": 13223.441},
    {"data": 20230404, "mercato": "MI-A3", "volumi": 7079.061},
    {"data": 20230403, "mercato": "XBID", "volumi": 22164.1},
]
```

Next, choose a market (es: ``MI-A2``) and retrieve the hourly prices, volumes and liquidity:

```python
# Get hourly prices
print(await mercati_elettrici.get_prices("MI-A2"))

# Get hourly volumes
print(await mercati_elettrici.get_volumes("MI-A2"))

# Get market liquidity
print(await mercati_elettrici.get_liquidity())
```

Unlike ``MGP`` these methods return data as formatted by the API, for all the zones. For example:

```python
[
    {"data": 20230404, "ora": 1, "mercato": "MI-A2", "zona": "CALA", "prezzo": 112.0},
    {"data": 20230404, "ora": 1, "mercato": "MI-A2", "zona": "CNOR", "prezzo": 112.0},
    {"data": 20230404, "ora": 1, "mercato": "MI-A2", "zona": "CSUD", "prezzo": 112.0},
    {"data": 20230404, "ora": 1, "mercato": "MI-A2", "zona": "NORD", "prezzo": 112.0},
    {"data": 20230404, "ora": 1, "mercato": "MI-A2", "zona": "SARD", "prezzo": 112.0},
    {"data": 20230404, "ora": 1, "mercato": "MI-A2", "zona": "SICI", "prezzo": 112.0},
    {"data": 20230404, "ora": 1, "mercato": "MI-A2", "zona": "SUD", "prezzo": 112.0},
    {"data": 20230404, "ora": 2, "mercato": "MI-A2", "zona": "CALA", "prezzo": 112.0},
    {"data": 20230404, "ora": 2, "mercato": "MI-A2", "zona": "CNOR", "prezzo": 112.0},
    {"data": 20230404, "ora": 2, "mercato": "MI-A2", "zona": "CSUD", "prezzo": 112.0},
    ...
]
```

## MercatiGas

This class wraps the API for the gas markets. The gas markets are operated with a continuous trading mode and an auction mode, both a few days ahead and in the intraday market. Moreover, there is a market for the stored gas. See [the GME website](https://www.mercatoelettrico.org/en/Mercati/MGAS/MGas.aspx) for more details. The API allows to retrieve the hourly prices and volumes of the markets exactly as served by GME.

First of all you should accept the terms of use of GME API:

```python
async with MercatiGas() as mercati_gas:
    print(await mercati_gas.get_general_conditions())
    print(await mercati_gas.get_disclaimer())
```

After that, you can retrieve the available markets with:

```python
await mercati_gas.get_markets()
# Returns:
[
    {"data": 20230405, "prodotto": "MGP-2023-04-06", "volumi": 245208.0, "tipo": "C"},
    {"data": 20230405, "prodotto": "MGP-2023-04-07", "volumi": None, "tipo": "C"},
    {"data": 20230405, "prodotto": "MGP-2023-04-08", "volumi": None, "tipo": "C"},
    {"data": 20230405, "prodotto": "MI-2023-04-05", "volumi": 224688.0, "tipo": "C"},
    {"data": 20230405, "prodotto": "MGP-2023-04-06", "volumi": 90480.0, "tipo": "A"},
    {"data": 20230405, "prodotto": "MI-2023-04-05", "volumi": 0.0, "tipo": "A"},
    {"data": 20230405, "prodotto": "MGS-Edison Stoccaggio", "volumi": 0.0, "tipo": "A"},
    {"data": 20230405, "prodotto": "MGS-Stogit", "volumi": 12036.924, "tipo": "A"},
]
```

Where ``tipo`` is ``C`` for continuous trading and ``A`` for auction, whereas ``prodotto`` starts with ``MGP`` for day-ahead markets, ``MI`` for the intraday market and ``MI`` for the intraday market. As you can notice, on a single day (``20230405``) there are many open markets for different days.

Next, choose a product from the continuous trading ones (es: ``MGP-2023-04-06``) and retrieve the trading results:

```python
await mercati_gas.get_continuous_trading_results("MGP-2023-04-06", date(2023, 4, 5))
# Returns:
[{'data': 20230405,
  'mercato': 'MGP',
  'prezzoControllo': 51.995,
  'prezzoMassimo': 52.5,
  'prezzoMedio': 51.35733,
  'prezzoMinimo': 50.2,
  'primoPrezzo': 50.5,
  'prodotto': 'MGP-2023-04-06',
  'ultimoPrezzo': 51.151,
  'volumiMw': 10217.0,
  'volumiMwh': 245208.0}]
```

or a product from the auction ones (es: ``MI-2023-04-05``) and retrieve the auction results:

```python
await mercati_gas.get_auction_trading_results("MI-2023-04-05", date(2023, 4, 5))
# Returns:
[{'acquistiTso': 0.0,
  'data': 20230405,
  'mercato': 'MI',
  'prezzo': None,
  'prodotto': 'MI-2023-04-05',
  'venditeTso': 0.0,
  'volumiMw': 0.0,
  'volumiMwh': 0.0}]
```

or a stored gas product (es: ``MGS-Stogit``) and retrieve the stored gas results:

```python
await mercati_gas.get_stored_gas_trading_results("MGS-Stogit", date(2023, 4, 5))
# Returns:
[{'acquistiSrg': 2036.924,
  'data': 20230405,
  'dataFlusso': 20230405,
  'impresaStoccaggio': 'Stogit',
  'prezzo': 49.95,
  'tipologia': None,
  'venditeSrg': 0.0,
  'volumi': 12036.924}]
```

## MercatiAmbientali

This class wraps the API for the environmental markets. See [the GME website](https://www.mercatoelettrico.org/En/Mercati/TEE/CosaSonoTee.aspx) for an explaination of the environmental markets. The API allows to retrieve the hourly prices and volumes of the markets exactly as served by GME.

First of all you should accept the terms of use of GME API:

```python
async with MercatiAmbientali() as mercati_ambientali:
    print(await mercati_ambientali.get_general_conditions())
    print(await mercati_ambientali.get_disclaimer())
```

After that, you can retrieve the available markets with:

```python
await mercati_ambientali.get_markets()
# Returns:
[{'data': 20230323, 'mercato': 'GO', 'volumi': 136917.0},
 {'data': 20230328, 'mercato': 'TEE', 'volumi': 29209.0}]
```

Next, choose a market (es: ``GO``) and retrieve the trading results:

```python
await mercati_ambientali.get_trading_results("GO", date(2023, 3, 23))
# Returns:
[{'data': 20230323,
  'mercato': 'GO',
  'periodo': 'Altri Mesi 2022',
  'prezzoMassimo': 9.0,
  'prezzoMinimo': 6.1,
  'prezzoRiferimento': 6.833425,
  'tipologia': 'Altro',
  'volumi': 3115.0},
 {'data': 20230323,
  'mercato': 'GO',
  'periodo': 'Altri Mesi 2022',
  'prezzoMassimo': 8.0,
  'prezzoMinimo': 7.25,
  'prezzoRiferimento': 7.611801,
  'tipologia': 'Eolico',
  'volumi': 5567.0},
 {'data': 20230323,
  'mercato': 'GO',
  'periodo': 'Altri Mesi 2022',
  'prezzoMassimo': 8.0,
  'prezzoMinimo': 7.0,
  'prezzoRiferimento': 7.583506,
  'tipologia': 'Idroelettrico',
  'volumi': 112000.0},
 {'data': 20230323,
  'mercato': 'GO',
  'periodo': 'Altri Mesi 2022',
  'prezzoMassimo': 7.95,
  'prezzoMinimo': 6.0,
  'prezzoRiferimento': 7.400446,
  'tipologia': 'Solare',
  'volumi': 16235.0}]
```
