from __future__ import annotations

from dataclasses import dataclass
from uuid import uuid4

import httpx
import structlog

from app.core.config import Settings

logger = structlog.get_logger(__name__)

TURNSTILE_SITEVERIFY_URL = "https://challenges.cloudflare.com/turnstile/v0/siteverify"


@dataclass(frozen=True, slots=True)
class TurnstileVerificationResult:
    success: bool
    error_codes: tuple[str, ...] = ()
    hostname: str | None = None


class CloudflareTurnstileVerifier:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    async def verify(
        self,
        *,
        token: str,
        remote_ip: str | None = None,
    ) -> TurnstileVerificationResult:
        payload: dict[str, str] = {
            "secret": self.settings.turnstile_secret_key,
            "response": token,
            "idempotency_key": str(uuid4()),
        }
        if remote_ip is not None:
            payload["remoteip"] = remote_ip

        try:
            async with httpx.AsyncClient(timeout=self.settings.turnstile_timeout_seconds) as client:
                response = await client.post(TURNSTILE_SITEVERIFY_URL, json=payload)
                response.raise_for_status()
        except httpx.HTTPError as exc:
            logger.warning(
                "auth.turnstile.verification_http_error",
                detail=str(exc),
            )
            return TurnstileVerificationResult(
                success=False,
                error_codes=("internal-error",),
            )

        data = response.json()
        raw_error_codes = data.get("error-codes")
        error_codes = (
            tuple(code for code in raw_error_codes if isinstance(code, str))
            if isinstance(raw_error_codes, list)
            else ()
        )
        hostname = data.get("hostname") if isinstance(data.get("hostname"), str) else None

        if not bool(data.get("success")):
            logger.info(
                "auth.turnstile.verification_rejected",
                error_codes=error_codes,
                hostname=hostname,
            )
            return TurnstileVerificationResult(
                success=False,
                error_codes=error_codes,
                hostname=hostname,
            )

        expected_hostname = self.settings.turnstile_expected_hostname
        if expected_hostname is not None and hostname != expected_hostname:
            logger.warning(
                "auth.turnstile.hostname_mismatch",
                expected_hostname=expected_hostname,
                actual_hostname=hostname,
            )
            return TurnstileVerificationResult(
                success=False,
                error_codes=("hostname-mismatch",),
                hostname=hostname,
            )

        return TurnstileVerificationResult(
            success=True,
            error_codes=error_codes,
            hostname=hostname,
        )
