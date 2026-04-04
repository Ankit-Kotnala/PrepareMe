from collections.abc import AsyncIterator, Callable
from typing import Annotated

from fastapi import Depends, HTTPException, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db.session import DatabaseSessionManager
from app.core.enums import UserRole
from app.core.request_context import RequestContext


def get_request_context(request: Request) -> RequestContext:
    context = getattr(request.state, "request_context", None)
    if context is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required.",
        )
    return context


async def get_db_session(
    request: Request,
    context: Annotated[RequestContext, Depends(get_request_context)],
) -> AsyncIterator[AsyncSession]:
    db_manager: DatabaseSessionManager = request.app.state.db_session_manager
    async with db_manager.session(context.institution_id) as session:
        yield session


def require_roles(*allowed_roles: UserRole) -> Callable[[RequestContext], RequestContext]:
    def dependency(
        context: Annotated[RequestContext, Depends(get_request_context)],
    ) -> RequestContext:
        if context.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to access this resource.",
            )
        return context

    return dependency


RequestContextDep = Annotated[RequestContext, Depends(get_request_context)]
DbSessionDep = Annotated[AsyncSession, Depends(get_db_session)]

