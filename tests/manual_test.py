"""Run manually to test the library."""
import asyncio
from mercati_energetici import MercatiElettrici, MGP
from datetime import date


async def main() -> None:
    """Show example on how to use the library."""
    async with MGP() as mgp:
        print("PUN avg: ", await mgp.daily_pun(date(2023, 3, 28)))


if __name__ == "__main__":
    asyncio.run(main())
