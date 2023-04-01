# mercati-energetici

## Async python library for Italian energy markets

Unofficial wrapper of the GME ([Gestore dei Mercati Energetici S.p.A.](https://mercatoelettrico.org/It/Default.aspx)) APP API. It allows to retrieve prices and volumes traded on the Italian energy markets (electricity, gas and environmental) in a simple and asynchronous way.

### Disclaimer

This library is not affiliated with GME ([Gestore dei Mercati Energetici S.p.A.](https://mercatoelettrico.org/It/Default.aspx)) in any way. It is provided as is, without any warranty. By using this library, you agree to the terms of use of GME API, which can be obtained with ``get_general_conditions()`` or can be found [here](https://www.mercatoelettrico.org/it/tools/AccessoDati.aspx). Please, be aware that all the data belongs to GME and can't be used for profit. Also, be aware of the disclaimer from GME retrivable with ``get_disclaimer()``.

### Example

```python
"""How to get the average price of electricity in Italy (PUN) for a specific date."""
import asyncio
from mercati_energetici import MGP
from datetime import date


async def main():
    async with MGP() as mgp:

        # By using this library, you agree to the terms of use of GME API
        # which can be obtained with:
        print(mgp.get_general_conditions())

        # Also, be aware of the following disclaimer from GME
        print(mgp.get_disclaimer())

        # Get PUN price
        print("PUN avg: ", await mgp.daily_pun(date(2023, 3, 28)))


if __name__ == "__main__":
    asyncio.run(main())
```

## Documentation

The library exposes three low level classes to access the GME API: ``MercatiElettrici``, ``MercatiGas`` and ``MercatiAmbientali``. A further class, ``MGP``, offers a higher level interface over the day-ahead electricity market.

### Installation

```bash
pip install mercati-energetici
```

### Usage

See the [documentation](https://mercati-energetici.readthedocs.io/en/latest/) for more details.
