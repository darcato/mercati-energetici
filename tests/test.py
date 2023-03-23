import asyncio
from mercati_energetici import MercatoElettrico
from datetime import date


async def main() -> None:
    """Show example on how to use the library."""
    async with MercatoElettrico() as mercato_elettrico:
        data = await mercato_elettrico.get_prices(date(2023, 3, 24))
        print(data)
        print("PUN avg: ", sum(list(data.values())) / 24)


if __name__ == "__main__":
    asyncio.run(main())
