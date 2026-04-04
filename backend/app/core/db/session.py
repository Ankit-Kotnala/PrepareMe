from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from uuid import UUID

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine


class DatabaseSessionManager:
    def __init__(self, database_url: str, *, echo: bool = False) -> None:
        self.engine: AsyncEngine = create_async_engine(
            database_url,
            echo=echo,
            future=True,
            pool_pre_ping=True,
        )
        self.session_factory = async_sessionmaker(
            self.engine,
            expire_on_commit=False,
            autoflush=False,
            class_=AsyncSession,
        )

    @asynccontextmanager
    async def session(self, institution_id: UUID | None = None) -> AsyncIterator[AsyncSession]:
        async with self.session_factory() as session:
            if institution_id is not None:
                await apply_institution_context(session, institution_id)
            yield session

    async def dispose(self) -> None:
        await self.engine.dispose()


async def apply_institution_context(session: AsyncSession, institution_id: UUID) -> None:
    bind = session.get_bind()
    if bind.dialect.name != "postgresql":
        return

    await session.execute(
        text("select set_config('app.institution_id', :institution_id, true)"),
        {"institution_id": str(institution_id)},
    )

