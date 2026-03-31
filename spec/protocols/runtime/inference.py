"""Capability 8: Inference protocol."""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from spec.models.runtime.models import (
    CompletionResult,
    EmbeddingsResult,
    Message,
    RerankResult,
    ToolDefinition,
)


@runtime_checkable
class InferenceProvider(Protocol):
    """Abstract contract for model inference.

    Providers implement this using their native API -- OpenAI, Anthropic,
    Ollama, vLLM, or any other inference backend. The spec does not
    prescribe which vendor's paths or payload format to use.
    """

    async def chat_completion(
        self,
        model: str,
        messages: list[Message],
        *,
        temperature: float | None = None,
        max_tokens: int | None = None,
        top_p: float | None = None,
        tools: list[ToolDefinition] | None = None,
        stream: bool = False,
    ) -> CompletionResult: ...

    async def completion(
        self,
        model: str,
        prompt: str,
        *,
        temperature: float | None = None,
        max_tokens: int | None = None,
        top_p: float | None = None,
        stream: bool = False,
    ) -> CompletionResult: ...

    async def embeddings(
        self,
        model: str,
        inputs: list[str],
    ) -> EmbeddingsResult: ...

    async def rerank(
        self,
        model: str,
        query: str,
        documents: list[str],
        *,
        top_k: int | None = None,
    ) -> RerankResult: ...
