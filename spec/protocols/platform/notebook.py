"""Capability 2: Interactive Development protocol."""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from spec.models.common import ResourceRequirements
from spec.models.platform.models import Notebook, NotebookList


@runtime_checkable
class NotebookProvider(Protocol):
    """Abstract contract for notebook/IDE lifecycle management."""

    async def create_notebook(
        self,
        workspace_id: str,
        name: str,
        image: str,
        *,
        resources: ResourceRequirements | None = None,
        storage_volumes: list[str] | None = None,
        labels: dict[str, str] | None = None,
        environment_variables: dict[str, str] | None = None,
    ) -> Notebook: ...

    async def get_notebook(
        self, workspace_id: str, notebook_id: str
    ) -> Notebook: ...

    async def list_notebooks(
        self,
        workspace_id: str,
        *,
        labels: str | None = None,
        page_token: str | None = None,
        page_size: int = 100,
    ) -> NotebookList: ...

    async def start_notebook(
        self, workspace_id: str, notebook_id: str
    ) -> Notebook: ...

    async def stop_notebook(
        self, workspace_id: str, notebook_id: str
    ) -> Notebook: ...

    async def delete_notebook(
        self, workspace_id: str, notebook_id: str
    ) -> None: ...
