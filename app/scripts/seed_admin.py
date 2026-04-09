import asyncio

from app.db.session import get_engine, get_session_factory
from app.services.users import seed_default_admin


async def _main() -> None:
    async with get_session_factory()() as session:
        await seed_default_admin(session)
    await get_engine().dispose()


def main() -> None:
    asyncio.run(_main())


if __name__ == "__main__":
    main()
