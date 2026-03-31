"""Canonical data models for cross-cutting capabilities (16-18)."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field

from spec.models.common import Pagination, ProviderManifest


# -- Capability 16: Model Registry --------------------------------------------

class RegisteredModel(BaseModel):
    id: str
    name: str
    description: str | None = None
    owner: str | None = None
    tags: list[str] = Field(default_factory=list)
    custom_properties: dict[str, str] = Field(default_factory=dict)
    created_at: datetime | None = None
    updated_at: datetime | None = None


class RegisteredModelList(BaseModel):
    items: list[RegisteredModel]
    pagination: Pagination | None = None


class ModelVersion(BaseModel):
    id: str
    version: str
    model_id: str | None = None
    artifact_uri: str | None = None
    state: str = "staged"
    description: str | None = None
    custom_properties: dict[str, str] = Field(default_factory=dict)
    created_at: datetime | None = None


class ModelVersionList(BaseModel):
    items: list[ModelVersion]


# -- Capability 17: Provider Management ---------------------------------------

class CapabilityInfo(BaseModel):
    name: str
    supported: bool
    operations: list[str] = Field(default_factory=list)


class CapabilityList(BaseModel):
    capabilities: list[CapabilityInfo]


class ProviderList(BaseModel):
    items: list[ProviderManifest]


# -- Capability 18: Tool Runtime -----------------------------------------------

class Tool(BaseModel):
    id: str
    name: str
    description: str | None = None
    parameters_schema: dict[str, Any] | None = None
    group_id: str | None = None


class ToolList(BaseModel):
    items: list[Tool]
    pagination: Pagination | None = None


class ToolResult(BaseModel):
    status: str
    output: Any = None
    error: str | None = None


class ToolGroup(BaseModel):
    id: str
    name: str
    description: str | None = None
    tools: list[str] = Field(default_factory=list)


class ToolGroupList(BaseModel):
    items: list[ToolGroup]
