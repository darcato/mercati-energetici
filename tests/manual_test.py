"""Run manually to test the library."""
import asyncio
from mercati_energetici import MercatiElettrici
from datetime import date


async def main() -> None:
    """Show example on how to use the library."""
    async with MercatiElettrici() as me:
        print(await me.markets())
        print(await me.liquidity(date(2023, 3, 24)))
        prices = await me.prices("MGP", zone="PUN")
        print("PUN avg: ", sum(list(prices.values())) / 24)


if __name__ == "__main__":
    asyncio.run(main())
