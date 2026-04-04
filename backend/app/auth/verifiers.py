import asyncio
from uuid import UUID

import jwt
from fastapi import Request
from jwt import InvalidTokenError, PyJWKClient

from app.core.config import Settings
from app.core.enums import AuthMode, UserRole
from app.core.request_context import RequestContext
from app.core.types import JSONValue


class AuthenticationError(Exception):
    pass


class TestHeaderTokenVerifier:
    async def verify_request(self, request: Request) -> RequestContext:
        user_id = request.headers.get("X-PrepareMe-User-Id")
        institution_id = request.headers.get("X-PrepareMe-Institution-Id")
        role = request.headers.get("X-PrepareMe-Role")
        email = request.headers.get("X-PrepareMe-Email")
        session_id = request.headers.get("X-PrepareMe-Session-Id")

        if user_id is None or institution_id is None or role is None:
            raise AuthenticationError(
                "Missing authentication headers. Expected X-PrepareMe-User-Id, "
                "X-PrepareMe-Institution-Id, and X-PrepareMe-Role."
            )

        try:
            parsed_role = UserRole(role)
        except ValueError as exc:
            raise AuthenticationError(f"Unsupported role '{role}'.") from exc

        return RequestContext(
            institution_id=UUID(institution_id),
            user_id=UUID(user_id),
            role=parsed_role,
            email=email,
            session_id=session_id,
            raw_claims={
                "sub": user_id,
                "institution_id": institution_id,
                "role": role,
                "email": email,
                "sid": session_id,
            },
        )


class ClerkTokenVerifier:
    def __init__(self, settings: Settings) -> None:
        if settings.clerk_jwks_url is None or settings.clerk_issuer is None:
            raise RuntimeError("Clerk auth mode requires clerk_jwks_url and clerk_issuer.")
        self.settings = settings
        self.jwks_client = PyJWKClient(settings.clerk_jwks_url)

    async def verify_request(self, request: Request) -> RequestContext:
        authorization = request.headers.get("Authorization")
        if authorization is None or not authorization.startswith("Bearer "):
            raise AuthenticationError("Missing Bearer token.")

        token = authorization.removeprefix("Bearer ").strip()

        try:
            signing_key = await asyncio.to_thread(self.jwks_client.get_signing_key_from_jwt, token)
            claims: dict[str, JSONValue] = jwt.decode(
                token,
                signing_key.key,
                algorithms=["RS256"],
                audience=self.settings.auth_audience,
                issuer=self.settings.clerk_issuer,
                options={"require": [self.settings.auth_user_id_claim]},
            )
        except InvalidTokenError as exc:
            raise AuthenticationError("Invalid authentication token.") from exc

        return self._context_from_claims(claims)

    def _context_from_claims(self, claims: dict[str, JSONValue]) -> RequestContext:
        user_id_value = claims.get(self.settings.auth_user_id_claim)
        institution_id_value = claims.get(self.settings.auth_institution_id_claim)
        role_value = claims.get(self.settings.auth_role_claim)
        email_value = claims.get(self.settings.auth_email_claim)
        session_id_value = claims.get(self.settings.auth_session_id_claim)

        if not isinstance(user_id_value, str) or not isinstance(institution_id_value, str):
            raise AuthenticationError("Missing required user or institution claim.")
        if not isinstance(role_value, str):
            raise AuthenticationError("Missing required role claim.")
        if email_value is not None and not isinstance(email_value, str):
            raise AuthenticationError("Email claim must be a string.")
        if session_id_value is not None and not isinstance(session_id_value, str):
            raise AuthenticationError("Session claim must be a string.")

        try:
            role = UserRole(role_value)
        except ValueError as exc:
            raise AuthenticationError(f"Unsupported role '{role_value}'.") from exc

        return RequestContext(
            institution_id=UUID(institution_id_value),
            user_id=UUID(user_id_value),
            role=role,
            email=email_value,
            session_id=session_id_value,
            raw_claims=claims,
        )


def build_token_verifier(settings: Settings) -> TestHeaderTokenVerifier | ClerkTokenVerifier:
    if settings.auth_mode == AuthMode.CLERK:
        return ClerkTokenVerifier(settings)
    return TestHeaderTokenVerifier()

