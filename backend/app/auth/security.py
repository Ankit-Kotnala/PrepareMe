from __future__ import annotations

import hashlib
import hmac
import secrets
from datetime import UTC, datetime, timedelta
from uuid import uuid4

import jwt

from app.core.config import Settings
from app.core.enums import UserRole
from app.core.types import JSONValue

PASSWORD_SCHEME = "pbkdf2_sha256"
PASSWORD_ITERATIONS = 600_000


def hash_password(password: str) -> str:
    salt = secrets.token_hex(16)
    derived_key = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt.encode("utf-8"),
        PASSWORD_ITERATIONS,
    )
    return (
        f"{PASSWORD_SCHEME}${PASSWORD_ITERATIONS}${salt}${derived_key.hex()}"
    )


def verify_password(password: str, encoded_hash: str) -> bool:
    try:
        scheme, raw_iterations, salt, stored_hash = encoded_hash.split("$", 3)
    except ValueError:
        return False

    if scheme != PASSWORD_SCHEME:
        return False

    try:
        iterations = int(raw_iterations)
    except ValueError:
        return False

    candidate_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt.encode("utf-8"),
        iterations,
    ).hex()
    return hmac.compare_digest(candidate_hash, stored_hash)


def create_access_token(
    *,
    settings: Settings,
    user_id: str,
    institution_id: str,
    institution_name: str,
    institution_slug: str,
    role: UserRole,
    email: str,
    display_name: str,
) -> tuple[str, int]:
    expires_in_seconds = settings.jwt_access_token_expires_minutes * 60
    issued_at = datetime.now(UTC)
    expires_at = issued_at + timedelta(seconds=expires_in_seconds)
    session_id = str(uuid4())

    payload: dict[str, JSONValue] = {
        settings.auth_user_id_claim: user_id,
        settings.auth_institution_id_claim: institution_id,
        settings.auth_institution_name_claim: institution_name,
        settings.auth_institution_slug_claim: institution_slug,
        settings.auth_role_claim: role.value,
        settings.auth_email_claim: email,
        settings.auth_display_name_claim: display_name,
        settings.auth_session_id_claim: session_id,
        "iss": settings.jwt_issuer,
        "iat": int(issued_at.timestamp()),
        "exp": int(expires_at.timestamp()),
    }
    if settings.auth_audience:
        payload["aud"] = settings.auth_audience

    token = jwt.encode(
        payload,
        settings.jwt_secret,
        algorithm=settings.jwt_algorithm,
    )
    return token, expires_in_seconds
