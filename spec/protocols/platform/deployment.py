"""Capability 3: Model Deployment protocol."""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from spec.models.common import ResourceRequirements
from spec.models.platform.models import Deployment, DeploymentList, DeploymentStatus


@runtime_checkable
class DeploymentProvider(Protocol):
    """Abstract contract for deploying models as inference endpoints."""

    async def create_deployment(
        self,
        workspace_id: str,
        name: str,
        model_uri: str,
        *,
        runtime: str | None = None,
        resources: ResourceRequirements | None = None,
        min_replicas: int = 1,
        max_replicas: int | None = None,
        labels: dict[str, str] | None = None,
    ) -> Deployment: ...

    async def get_deployment(
        self, workspace_id: str, deployment_id: str
    ) -> Deployment: ...

    async def list_deployments(
        self,
        workspace_id: str,
        *,
        labels: str | None = None,
        page_token: str | None = None,
        page_size: int = 100,
    ) -> DeploymentList: ...

    async def update_deployment(
        self,
        workspace_id: str,
        deployment_id: str,
        *,
        model_uri: str | None = None,
        runtime: str | None = None,
        resources: ResourceRequirements | None = None,
        min_replicas: int | None = None,
        max_replicas: int | None = None,
    ) -> Deployment: ...

    async def delete_deployment(
        self, workspace_id: str, deployment_id: str
    ) -> None: ...

    async def get_deployment_status(
        self, workspace_id: str, deployment_id: str
    ) -> DeploymentStatus: ...
