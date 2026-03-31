"""Capability 17: Provider Management protocol."""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from spec.models.common import HealthStatus, ProviderManifest
from spec.models.cross_cutting.models import CapabilityList, ProviderList


@runtime_checkable
class ProviderManagementProvider(Protocol):
    """Abstract contract for discovering and inspecting providers."""

    async def list_providers(self) -> ProviderList: ...

    async def get_provider(self, provider_id: str) -> ProviderManifest: ...

    async def health_check(self, provider_id: str) -> HealthStatus: ...

    async def get_provider_capabilities(
        self, provider_id: str
    ) -> CapabilityList: ...
