"""Canonical data models shared across all capabilities.

These models are vendor-neutral. Providers translate to/from their
native formats when implementing capability protocols.
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class ResourceMetadata(BaseModel):
    id: str
    name: str
    labels: dict[str, str] = Field(default_factory=dict)
    annotations: dict[str, str] = Field(default_factory=dict)
    created_at: datetime | None = None
    updated_at: datetime | None = None


class ResourceRequirements(BaseModel):
    cpu: str | None = None
    memory: str | None = None
    gpu: int | None = None
    gpu_type: str | None = None


class Pagination(BaseModel):
    next_page_token: str | None = None
    total_count: int | None = None


class HealthState(str, Enum):
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"


class HealthStatus(BaseModel):
    status: HealthState
    message: str | None = None
    checked_at: datetime | None = None


class Capability(str, Enum):
    WORKSPACES = "workspaces"
    NOTEBOOKS = "notebooks"
    DEPLOYMENTS = "deployments"
    TRAINING = "training"
    PIPELINES = "pipelines"
    STORAGE = "storage"
    CLUSTER_RESOURCES = "cluster_resources"
    INFERENCE = "inference"
    AGENTS = "agents"
    SAFETY = "safety"
    KNOWLEDGE = "knowledge"
    EVALUATION = "evaluation"
    DATASETS = "datasets"
    PROMPTS = "prompts"
    FILES = "files"
    MODEL_REGISTRY = "model_registry"
    PROVIDER_MANAGEMENT = "provider_management"
    TOOL_RUNTIME = "tool_runtime"


class ProviderManifest(BaseModel):
    """Declaration of which capabilities a provider supports."""

    name: str
    version: str
    description: str | None = None
    capabilities: set[Capability]
    config: dict[str, Any] = Field(default_factory=dict)


class Condition(BaseModel):
    type: str
    status: str
    reason: str | None = None
    message: str | None = None
    last_transition: datetime | None = None
