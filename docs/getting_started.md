# Async python library for Italian energy markets

Unofficial wrapper of the GME ([Gestore dei Mercati Energetici S.p.A.](https://mercatoelettrico.org/It/Default.aspx)) APP API. It allows to retrieve prices and volumes traded on the Italian energy markets (electricity, gas and environmental) in a simple and asynchronous way.

## Installation

```bash
pip install mercati-energetici
```

## Usage

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

### MGP

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

### MercatiElettrici

This class wraps the API for the day-ahead electricity market. It allows to retrieve hourly prices, volumes and liquidity of the day-ahead market exactly as served by GME.

First of all you should accept the terms of use of GME API:

```python
async with MercatiElettrici() as mercati_elettrici:
    print(await mercati_elettrici.get_general_conditions())
    print(await mercati_elettrici.get_disclaimer())
```

After that, you can retrieve the hourly available markets with:

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

## Disclaimer

This library is not affiliated with GME ([Gestore dei Mercati Energetici S.p.A.](https://mercatoelettrico.org/It/Default.aspx)) in any way. It is provided as is, without any warranty. By using this library, you agree to the terms of use of GME API, which can be obtained with ``get_general_conditions()`` or can be found [here](https://www.mercatoelettrico.org/it/tools/AccessoDati.aspx). Please, be aware that all the data belongs to GME and can't be used for profit. Also, be aware of the disclaimer from GME retrivable with ``get_disclaimer()``.
