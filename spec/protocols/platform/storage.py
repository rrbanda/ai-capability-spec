"""Capability 6: Persistent Storage protocol."""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from spec.models.platform.models import (
    AccessMode,
    Connection,
    ConnectionList,
    StorageVolume,
    StorageVolumeList,
)


@runtime_checkable
class StorageProvider(Protocol):
    """Abstract contract for storage volumes and data connections."""

    async def create_storage(
        self,
        workspace_id: str,
        name: str,
        size: str,
        *,
        storage_class: str | None = None,
        access_mode: AccessMode = AccessMode.READ_WRITE_ONCE,
        labels: dict[str, str] | None = None,
    ) -> StorageVolume: ...

    async def get_storage(
        self, workspace_id: str, storage_id: str
    ) -> StorageVolume: ...

    async def list_storage(
        self,
        workspace_id: str,
        *,
        labels: str | None = None,
        page_token: str | None = None,
        page_size: int = 100,
    ) -> StorageVolumeList: ...

    async def delete_storage(
        self, workspace_id: str, storage_id: str
    ) -> None: ...

    async def create_connection(
        self,
        workspace_id: str,
        name: str,
        type: str,
        credentials: dict[str, str],
        *,
        labels: dict[str, str] | None = None,
    ) -> Connection: ...

    async def get_connection(
        self, workspace_id: str, connection_id: str
    ) -> Connection: ...

    async def list_connections(
        self,
        workspace_id: str,
        *,
        labels: str | None = None,
        page_token: str | None = None,
        page_size: int = 100,
    ) -> ConnectionList: ...

    async def delete_connection(
        self, workspace_id: str, connection_id: str
    ) -> None: ...
