"""Capability 5: Pipeline Orchestration protocol."""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from spec.models.platform.models import (
    PipelineServer,
    PipelineServerList,
    PipelineServerStatus,
)


@runtime_checkable
class PipelineProvider(Protocol):
    """Abstract contract for ML pipeline infrastructure management."""

    async def create_pipeline_server(
        self,
        workspace_id: str,
        name: str,
        *,
        object_store: str | None = None,
        database: str | None = None,
        labels: dict[str, str] | None = None,
    ) -> PipelineServer: ...

    async def get_pipeline_server(
        self, workspace_id: str, server_id: str
    ) -> PipelineServer: ...

    async def list_pipeline_servers(
        self, workspace_id: str
    ) -> PipelineServerList: ...

    async def delete_pipeline_server(
        self, workspace_id: str, server_id: str
    ) -> None: ...

    async def get_pipeline_server_status(
        self, workspace_id: str, server_id: str
    ) -> PipelineServerStatus: ...
