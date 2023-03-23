import asyncio
from mercati_energetici import MercatiEnergetici


async def main() -> None:
    """Show example on how to use the library."""
    async with MercatiEnergetici() as mercati_energetici:
        data = await mercati_energetici.get_prices()
        print(data)


if __name__ == "__main__":
    asyncio.run(main())
