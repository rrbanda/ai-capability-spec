"""Capability 13: Datasets protocol."""

from __future__ import annotations

from typing import Any, Protocol, runtime_checkable

from spec.models.runtime.models import Dataset, DatasetList, DatasetRowList, DatasetSource


@runtime_checkable
class DatasetProvider(Protocol):
    """Abstract contract for dataset registration and access."""

    async def register_dataset(
        self,
        name: str,
        source: DatasetSource,
        *,
        description: str | None = None,
        schema: dict[str, Any] | None = None,
    ) -> Dataset: ...

    async def get_dataset(self, dataset_id: str) -> Dataset: ...

    async def list_datasets(
        self,
        *,
        page_token: str | None = None,
        page_size: int = 100,
    ) -> DatasetList: ...

    async def delete_dataset(self, dataset_id: str) -> None: ...

    async def iterate_rows(
        self,
        dataset_id: str,
        *,
        page_token: str | None = None,
        page_size: int = 100,
    ) -> DatasetRowList: ...
