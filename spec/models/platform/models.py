"""Canonical data models for platform / infrastructure capabilities (1-7)."""

from __future__ import annotations

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field

from spec.models.common import Condition, Pagination, ResourceMetadata, ResourceRequirements


# -- Capability 1: Workspaces -------------------------------------------------

class WorkspaceStatus(str, Enum):
    ACTIVE = "active"
    TERMINATING = "terminating"
    PENDING = "pending"


class Workspace(BaseModel):
    metadata: ResourceMetadata
    description: str | None = None
    resource_quotas: ResourceRequirements | None = None
    status: WorkspaceStatus


class WorkspaceList(BaseModel):
    items: list[Workspace]
    pagination: Pagination | None = None


# -- Capability 2: Notebooks --------------------------------------------------

class NotebookStatus(str, Enum):
    STARTING = "starting"
    RUNNING = "running"
    STOPPING = "stopping"
    STOPPED = "stopped"
    FAILED = "failed"


class Notebook(BaseModel):
    metadata: ResourceMetadata
    image: str | None = None
    resources: ResourceRequirements | None = None
    storage_volumes: list[str] = Field(default_factory=list)
    status: NotebookStatus
    url: str | None = None


class NotebookList(BaseModel):
    items: list[Notebook]
    pagination: Pagination | None = None


# -- Capability 3: Deployments ------------------------------------------------

class DeploymentState(str, Enum):
    PENDING = "pending"
    PROVISIONING = "provisioning"
    READY = "ready"
    FAILED = "failed"
    UNKNOWN = "unknown"


class Deployment(BaseModel):
    metadata: ResourceMetadata
    model_uri: str
    runtime: str | None = None
    resources: ResourceRequirements | None = None
    replicas: int | None = None
    min_replicas: int | None = None
    max_replicas: int | None = None
    status: DeploymentState
    endpoint_url: str | None = None


class DeploymentStatus(BaseModel):
    state: DeploymentState
    ready_replicas: int | None = None
    total_replicas: int | None = None
    conditions: list[Condition] = Field(default_factory=list)
    endpoint_url: str | None = None


class DeploymentList(BaseModel):
    items: list[Deployment]
    pagination: Pagination | None = None


# -- Capability 4: Training ---------------------------------------------------

class TrainingJobStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    CANCELLED = "cancelled"


class TrainingJob(BaseModel):
    metadata: ResourceMetadata
    model: str | None = None
    dataset: str | None = None
    runtime: str | None = None
    resources: ResourceRequirements | None = None
    hyperparameters: dict[str, str] = Field(default_factory=dict)
    status: TrainingJobStatus
    start_time: datetime | None = None
    completion_time: datetime | None = None
    worker_count: int | None = None


class TrainingJobList(BaseModel):
    items: list[TrainingJob]
    pagination: Pagination | None = None


class TrainingRuntimeScope(str, Enum):
    CLUSTER = "cluster"
    WORKSPACE = "workspace"


class TrainingRuntime(BaseModel):
    metadata: ResourceMetadata
    description: str | None = None
    framework: str | None = None
    scope: TrainingRuntimeScope | None = None


class TrainingRuntimeList(BaseModel):
    items: list[TrainingRuntime]


class LogLine(BaseModel):
    timestamp: datetime | None = None
    message: str
    source: str | None = None


class LogStream(BaseModel):
    lines: list[LogLine] = Field(default_factory=list)


# -- Capability 5: Pipelines --------------------------------------------------

class PipelineServerState(str, Enum):
    PROVISIONING = "provisioning"
    READY = "ready"
    FAILED = "failed"
    UNKNOWN = "unknown"


class PipelineServerConfig(BaseModel):
    object_store: str | None = None
    database: str | None = None


class PipelineServer(BaseModel):
    metadata: ResourceMetadata
    config: PipelineServerConfig | None = None
    status: PipelineServerState


class PipelineServerStatus(BaseModel):
    state: PipelineServerState
    conditions: list[Condition] = Field(default_factory=list)


class PipelineServerList(BaseModel):
    items: list[PipelineServer]


# -- Capability 6: Storage ----------------------------------------------------

class AccessMode(str, Enum):
    READ_WRITE_ONCE = "read_write_once"
    READ_WRITE_MANY = "read_write_many"
    READ_ONLY_MANY = "read_only_many"


class StorageVolumeStatus(str, Enum):
    PENDING = "pending"
    BOUND = "bound"
    RELEASED = "released"
    FAILED = "failed"


class StorageVolume(BaseModel):
    metadata: ResourceMetadata
    size: str
    storage_class: str | None = None
    access_mode: AccessMode = AccessMode.READ_WRITE_ONCE
    status: StorageVolumeStatus


class StorageVolumeList(BaseModel):
    items: list[StorageVolume]
    pagination: Pagination | None = None


class Connection(BaseModel):
    metadata: ResourceMetadata
    type: str
    credentials: dict[str, str] = Field(default_factory=dict)


class ConnectionList(BaseModel):
    items: list[Connection]
    pagination: Pagination | None = None


# -- Capability 7: Cluster Resources ------------------------------------------

class NodeStatus(str, Enum):
    READY = "ready"
    NOT_READY = "not_ready"
    UNKNOWN = "unknown"


class Accelerator(BaseModel):
    type: str
    count: int


class ComputeNode(BaseModel):
    id: str
    hostname: str | None = None
    status: NodeStatus
    capacity: ResourceRequirements | None = None
    allocatable: ResourceRequirements | None = None
    labels: dict[str, str] = Field(default_factory=dict)
    accelerators: list[Accelerator] = Field(default_factory=list)


class ComputeNodeList(BaseModel):
    items: list[ComputeNode]


class AcceleratorSummary(BaseModel):
    type: str
    total: int
    available: int


class ClusterSummary(BaseModel):
    total_nodes: int | None = None
    ready_nodes: int | None = None
    total_capacity: ResourceRequirements | None = None
    total_allocatable: ResourceRequirements | None = None
    accelerator_summary: list[AcceleratorSummary] = Field(default_factory=list)


class AcceleratorProfile(BaseModel):
    id: str
    name: str
    description: str | None = None
    identifier: str | None = None
    enabled: bool = True


class AcceleratorProfileList(BaseModel):
    items: list[AcceleratorProfile]


class StorageClass(BaseModel):
    name: str
    provisioner: str | None = None
    is_default: bool = False
    volume_binding_mode: str | None = None


class StorageClassList(BaseModel):
    items: list[StorageClass]
