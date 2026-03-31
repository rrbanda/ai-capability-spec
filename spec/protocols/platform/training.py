"""Capability 4: Model Training protocol."""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from spec.models.common import ResourceRequirements
from spec.models.platform.models import (
    LogStream,
    TrainingJob,
    TrainingJobList,
    TrainingRuntimeList,
)


@runtime_checkable
class TrainingProvider(Protocol):
    """Abstract contract for distributed training job management."""

    async def create_training_job(
        self,
        workspace_id: str,
        name: str,
        *,
        model: str | None = None,
        dataset: str | None = None,
        runtime: str | None = None,
        resources: ResourceRequirements | None = None,
        hyperparameters: dict[str, str] | None = None,
        worker_count: int = 1,
        labels: dict[str, str] | None = None,
    ) -> TrainingJob: ...

    async def get_training_job(
        self, workspace_id: str, job_id: str
    ) -> TrainingJob: ...

    async def list_training_jobs(
        self,
        workspace_id: str,
        *,
        labels: str | None = None,
        page_token: str | None = None,
        page_size: int = 100,
    ) -> TrainingJobList: ...

    async def cancel_training_job(
        self, workspace_id: str, job_id: str
    ) -> TrainingJob: ...

    async def delete_training_job(
        self, workspace_id: str, job_id: str
    ) -> None: ...

    async def get_training_logs(
        self,
        workspace_id: str,
        job_id: str,
        *,
        container: str | None = None,
        tail_lines: int | None = None,
    ) -> LogStream: ...

    async def list_training_runtimes(
        self,
        *,
        labels: str | None = None,
    ) -> TrainingRuntimeList: ...
