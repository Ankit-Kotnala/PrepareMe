from dataclasses import dataclass
from typing import Protocol
from uuid import UUID


def _sanitize_relative_path(relative_path: str) -> str:
    sanitized = relative_path.strip().strip("/")
    return sanitized.replace("..", "")


@dataclass(slots=True, frozen=True)
class PresignedUpload:
    key: str
    url: str
    expires_in_seconds: int


@dataclass(slots=True, frozen=True)
class PresignedDownload:
    key: str
    url: str
    expires_in_seconds: int


class ObjectStorageProvider(Protocol):
    async def create_presigned_upload_url(
        self,
        *,
        key: str,
        content_type: str,
        expires_in_seconds: int,
    ) -> PresignedUpload: ...

    async def create_presigned_download_url(
        self,
        *,
        key: str,
        expires_in_seconds: int,
    ) -> PresignedDownload: ...


@dataclass(slots=True)
class LocalDebugStorageProvider:
    base_url: str = "http://localhost:9000"

    async def create_presigned_upload_url(
        self,
        *,
        key: str,
        content_type: str,
        expires_in_seconds: int,
    ) -> PresignedUpload:
        return PresignedUpload(
            key=key,
            url=f"{self.base_url}/upload/{key}?content_type={content_type}",
            expires_in_seconds=expires_in_seconds,
        )

    async def create_presigned_download_url(
        self,
        *,
        key: str,
        expires_in_seconds: int,
    ) -> PresignedDownload:
        return PresignedDownload(
            key=key,
            url=f"{self.base_url}/download/{key}",
            expires_in_seconds=expires_in_seconds,
        )


@dataclass(slots=True)
class TenantScopedStorage:
    provider: ObjectStorageProvider

    @staticmethod
    def build_tenant_key(*, institution_id: UUID, relative_path: str) -> str:
        sanitized = _sanitize_relative_path(relative_path)
        return f"{institution_id}/{sanitized}"

    async def create_presigned_upload_url(
        self,
        *,
        institution_id: UUID,
        relative_path: str,
        content_type: str,
        expires_in_seconds: int = 3600,
    ) -> PresignedUpload:
        key = self.build_tenant_key(institution_id=institution_id, relative_path=relative_path)
        return await self.provider.create_presigned_upload_url(
            key=key,
            content_type=content_type,
            expires_in_seconds=expires_in_seconds,
        )

    async def create_presigned_download_url(
        self,
        *,
        institution_id: UUID,
        relative_path: str,
        expires_in_seconds: int = 3600,
    ) -> PresignedDownload:
        key = self.build_tenant_key(institution_id=institution_id, relative_path=relative_path)
        return await self.provider.create_presigned_download_url(
            key=key,
            expires_in_seconds=expires_in_seconds,
        )

