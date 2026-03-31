"""Capability 14: Prompt Management protocol."""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from spec.models.runtime.models import (
    Prompt,
    PromptList,
    PromptVariable,
    RenderedPrompt,
)


@runtime_checkable
class PromptProvider(Protocol):
    """Abstract contract for versioned prompt template management."""

    async def create_prompt(
        self,
        name: str,
        template: str,
        *,
        description: str | None = None,
        variables: list[PromptVariable] | None = None,
    ) -> Prompt: ...

    async def get_prompt(self, prompt_id: str) -> Prompt: ...

    async def list_prompts(
        self,
        *,
        page_token: str | None = None,
        page_size: int = 100,
    ) -> PromptList: ...

    async def update_prompt(
        self,
        prompt_id: str,
        *,
        template: str | None = None,
        description: str | None = None,
        variables: list[PromptVariable] | None = None,
    ) -> Prompt: ...

    async def delete_prompt(self, prompt_id: str) -> None: ...

    async def render_prompt(
        self,
        prompt_id: str,
        variables: dict[str, str],
    ) -> RenderedPrompt: ...
