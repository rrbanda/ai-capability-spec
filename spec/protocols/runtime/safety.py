"""Capability 10: Safety and Guardrails protocol."""

from __future__ import annotations

from typing import Any, Protocol, runtime_checkable

from spec.models.runtime.models import Message, ModerationResult, Shield, ShieldList


@runtime_checkable
class SafetyProvider(Protocol):
    """Abstract contract for content moderation and safety shields."""

    async def moderate(
        self,
        content: str | list[Message],
        *,
        shields: list[str] | None = None,
    ) -> ModerationResult: ...

    async def create_shield(
        self,
        name: str,
        *,
        description: str | None = None,
        config: dict[str, Any] | None = None,
    ) -> Shield: ...

    async def list_shields(self) -> ShieldList: ...

    async def get_shield(self, shield_id: str) -> Shield: ...
