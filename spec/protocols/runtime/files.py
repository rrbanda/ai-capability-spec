"""Capability 15: File Management protocol."""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from spec.models.runtime.models import File, FileList


@runtime_checkable
class FileProvider(Protocol):
    """Abstract contract for file upload, retrieval, and deletion."""

    async def upload_file(
        self,
        content: bytes,
        filename: str,
        *,
        purpose: str | None = None,
    ) -> File: ...

    async def get_file(self, file_id: str) -> File: ...

    async def list_files(
        self,
        *,
        purpose: str | None = None,
        page_token: str | None = None,
        page_size: int = 100,
    ) -> FileList: ...

    async def delete_file(self, file_id: str) -> None: ...

    async def get_file_content(self, file_id: str) -> bytes: ...
