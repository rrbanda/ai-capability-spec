"""Capability 1: Workspace Management protocol."""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from spec.models.common import ResourceRequirements
from spec.models.platform.models import Workspace, WorkspaceList


@runtime_checkable
class WorkspaceProvider(Protocol):
    """Abstract contract for workspace lifecycle management.

    Providers implement this protocol to manage isolated project
    environments on their platform (e.g., K8s namespaces, cloud
    project spaces, etc.).
    """

    async def create_workspace(
        self,
        name: str,
        *,
        description: str | None = None,
        labels: dict[str, str] | None = None,
        resource_quotas: ResourceRequirements | None = None,
    ) -> Workspace: ...

    async def get_workspace(self, workspace_id: str) -> Workspace: ...

    async def list_workspaces(
        self,
        *,
        labels: str | None = None,
        page_token: str | None = None,
        page_size: int = 100,
    ) -> WorkspaceList: ...

    async def update_workspace(
        self,
        workspace_id: str,
        *,
        description: str | None = None,
        labels: dict[str, str] | None = None,
        resource_quotas: ResourceRequirements | None = None,
    ) -> Workspace: ...

    async def delete_workspace(self, workspace_id: str) -> None: ...
