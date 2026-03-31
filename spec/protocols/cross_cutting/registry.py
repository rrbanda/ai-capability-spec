"""Capability 16: Model Registry protocol."""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from spec.models.cross_cutting.models import (
    ModelVersion,
    ModelVersionList,
    RegisteredModel,
    RegisteredModelList,
)


@runtime_checkable
class ModelRegistryProvider(Protocol):
    """Abstract contract for model metadata management."""

    async def register_model(
        self,
        name: str,
        *,
        description: str | None = None,
        owner: str | None = None,
        tags: list[str] | None = None,
        custom_properties: dict[str, str] | None = None,
    ) -> RegisteredModel: ...

    async def get_model(self, model_id: str) -> RegisteredModel: ...

    async def list_models(
        self,
        *,
        page_token: str | None = None,
        page_size: int = 100,
    ) -> RegisteredModelList: ...

    async def create_model_version(
        self,
        model_id: str,
        version: str,
        *,
        artifact_uri: str | None = None,
        state: str = "staged",
        description: str | None = None,
        custom_properties: dict[str, str] | None = None,
    ) -> ModelVersion: ...

    async def list_model_versions(
        self, model_id: str
    ) -> ModelVersionList: ...

    async def search_models(
        self,
        *,
        query: str | None = None,
        tags: list[str] | None = None,
        owner: str | None = None,
        page_token: str | None = None,
        page_size: int = 100,
    ) -> RegisteredModelList: ...
