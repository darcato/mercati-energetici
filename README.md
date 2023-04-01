# Python library for Italian energy markets

## Example

```python
"""How to get the average price of electricity in Italy (PUN) for a specific date."""
import asyncio
from mercati_energetici import MGP
from datetime import date


async def main():
    async with MGP() as mgp:
        print("PUN avg: ", await mgp.daily_pun(date(2023, 3, 28)))


if __name__ == "__main__":
    asyncio.run(main())
```

## Disclaimer

## Usage

The library exposes three low level classes to access the GME API: ``MercatiElettrici``, ``MercatiGas`` and ``MercatiAmbientali``. A furhter class, ``MGP``, offers a higher level interface over the day-ahead electricity market.

