"""Canonical data models for runtime / agentic capabilities (8-15).

All models use vendor-neutral terminology. Providers translate to/from
their native formats (OpenAI, Anthropic, Ollama, etc.) internally.
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field

from spec.models.common import Pagination


# -- Shared runtime types -----------------------------------------------------

class ContentPart(BaseModel):
    type: str  # "text" | "image"
    text: str | None = None
    image_url: str | None = None


class ToolCallFunction(BaseModel):
    name: str
    arguments: str  # JSON-encoded


class ToolCall(BaseModel):
    id: str
    function: ToolCallFunction


class ToolDefinition(BaseModel):
    name: str
    description: str
    parameters: dict[str, Any] | None = None  # JSON Schema


class TokenUsage(BaseModel):
    prompt_tokens: int | None = None
    completion_tokens: int | None = None
    total_tokens: int | None = None


class Message(BaseModel):
    role: str  # "user" | "assistant" | "system" | "tool"
    content: str | list[ContentPart]
    tool_call_id: str | None = None
    tool_calls: list[ToolCall] | None = None


# -- Capability 8: Inference ---------------------------------------------------

class FinishReason(str, Enum):
    STOP = "stop"
    TOOL_USE = "tool_use"
    LENGTH = "length"
    CONTENT_FILTER = "content_filter"


class CompletionResult(BaseModel):
    id: str | None = None
    message: Message
    finish_reason: FinishReason
    usage: TokenUsage | None = None


class EmbeddingVector(BaseModel):
    index: int
    values: list[float]


class EmbeddingsResult(BaseModel):
    embeddings: list[EmbeddingVector]
    model: str | None = None
    usage: TokenUsage | None = None


class RankedDocument(BaseModel):
    index: int
    relevance_score: float
    document: str | None = None


class RerankResult(BaseModel):
    results: list[RankedDocument]


# -- Capability 9: Agentic Runtime --------------------------------------------

class AgentConfig(BaseModel):
    model: str | None = None
    instructions: str | None = None
    tools: list[ToolDefinition] = Field(default_factory=list)
    temperature: float | None = None
    max_turns: int | None = None


class AgentTurnStatus(str, Enum):
    COMPLETED = "completed"
    REQUIRES_ACTION = "requires_action"
    FAILED = "failed"


class AgentTurnResult(BaseModel):
    turn_id: str
    status: AgentTurnStatus
    output: Message
    tool_calls: list[ToolCall] | None = None
    usage: TokenUsage | None = None


class Session(BaseModel):
    id: str
    agent_config: AgentConfig | None = None
    turns: list[AgentTurnResult] = Field(default_factory=list)
    created_at: datetime | None = None
    updated_at: datetime | None = None


class SessionList(BaseModel):
    items: list[Session]
    pagination: Pagination | None = None


# -- Capability 10: Safety and Guardrails --------------------------------------

class Shield(BaseModel):
    id: str
    name: str
    description: str | None = None
    provider: str | None = None


class ShieldList(BaseModel):
    items: list[Shield]


class ShieldResult(BaseModel):
    shield_id: str
    flagged: bool
    violation: str | None = None


class ModerationResult(BaseModel):
    flagged: bool
    categories: dict[str, bool] = Field(default_factory=dict)
    scores: dict[str, float] = Field(default_factory=dict)
    shield_results: list[ShieldResult] = Field(default_factory=list)


# -- Capability 11: Knowledge / RAG --------------------------------------------

class VectorStore(BaseModel):
    id: str
    name: str
    embedding_model: str | None = None
    dimensions: int | None = None
    document_count: int | None = None
    created_at: datetime | None = None


class VectorStoreList(BaseModel):
    items: list[VectorStore]
    pagination: Pagination | None = None


class ChunkingConfig(BaseModel):
    strategy: str = "fixed_size"  # "fixed_size" | "sentence" | "paragraph"
    chunk_size: int | None = None
    overlap: int | None = None


class DocumentInput(BaseModel):
    id: str | None = None
    content: str
    metadata: dict[str, Any] = Field(default_factory=dict)


class InsertResult(BaseModel):
    inserted_count: int
    chunk_count: int | None = None


class DocumentChunk(BaseModel):
    id: str | None = None
    document_id: str | None = None
    content: str
    score: float
    metadata: dict[str, Any] = Field(default_factory=dict)


class QueryResult(BaseModel):
    chunks: list[DocumentChunk]


# -- Capability 12: Evaluation ------------------------------------------------

class EvalJobStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class EvalJob(BaseModel):
    id: str
    model: str | None = None
    dataset_id: str | None = None
    scoring_functions: list[str] = Field(default_factory=list)
    status: EvalJobStatus
    results: dict[str, float] = Field(default_factory=dict)
    created_at: datetime | None = None
    completed_at: datetime | None = None


class EvalJobList(BaseModel):
    items: list[EvalJob]
    pagination: Pagination | None = None


class ScoringReturnType(str, Enum):
    NUMERIC = "numeric"
    BOOLEAN = "boolean"
    CATEGORICAL = "categorical"


class ScoringFunction(BaseModel):
    id: str
    name: str
    description: str | None = None
    return_type: ScoringReturnType | None = None


class ScoringFunctionList(BaseModel):
    items: list[ScoringFunction]


class ScoreValue(BaseModel):
    value: float | bool | str
    metadata: dict[str, Any] = Field(default_factory=dict)


class ScoreResult(BaseModel):
    scores: list[ScoreValue]


# -- Capability 13: Datasets --------------------------------------------------

class DatasetSource(BaseModel):
    type: str  # "uri" | "inline" | "file"
    uri: str | None = None


class Dataset(BaseModel):
    id: str
    name: str
    description: str | None = None
    source: DatasetSource | None = None
    schema_: dict[str, Any] | None = Field(default=None, alias="schema")
    row_count: int | None = None
    created_at: datetime | None = None


class DatasetList(BaseModel):
    items: list[Dataset]
    pagination: Pagination | None = None


class DatasetRowList(BaseModel):
    rows: list[dict[str, Any]]
    pagination: Pagination | None = None


# -- Capability 14: Prompt Management ------------------------------------------

class PromptVariable(BaseModel):
    name: str
    description: str | None = None
    default: str | None = None


class Prompt(BaseModel):
    id: str
    name: str
    description: str | None = None
    template: str
    variables: list[PromptVariable] = Field(default_factory=list)
    version: int | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


class PromptList(BaseModel):
    items: list[Prompt]
    pagination: Pagination | None = None


class RenderedPrompt(BaseModel):
    content: str
    messages: list[Message] | None = None


# -- Capability 15: File Management --------------------------------------------

class File(BaseModel):
    id: str
    filename: str
    purpose: str | None = None
    size_bytes: int
    mime_type: str | None = None
    created_at: datetime | None = None


class FileList(BaseModel):
    items: list[File]
    pagination: Pagination | None = None
