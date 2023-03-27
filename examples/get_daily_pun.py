"""How to get the average price of electricity in Italy (PUN) for a specific date."""
import asyncio
from mercati_energetici import MGP
from datetime import date


async def main() -> None:
    """Show example on how to use the library."""
    async with MGP() as mgp:
        print("PUN avg: ", await mgp.daily_pun(date(2023, 3, 28)))


if __name__ == "__main__":
    asyncio.run(main())
