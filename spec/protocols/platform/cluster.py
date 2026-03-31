"""Capability 7: Cluster Resources protocol."""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from spec.models.platform.models import (
    AcceleratorProfileList,
    ClusterSummary,
    ComputeNodeList,
    StorageClassList,
)


@runtime_checkable
class ClusterResourcesProvider(Protocol):
    """Abstract contract for querying compute platform capacity."""

    async def list_compute_nodes(
        self,
        *,
        labels: str | None = None,
    ) -> ComputeNodeList: ...

    async def get_cluster_summary(self) -> ClusterSummary: ...

    async def list_accelerator_profiles(self) -> AcceleratorProfileList: ...

    async def list_storage_classes(self) -> StorageClassList: ...
