"""Capability 9: Agentic Runtime protocol."""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from spec.models.runtime.models import (
    AgentConfig,
    AgentTurnResult,
    Message,
    Session,
    SessionList,
)


@runtime_checkable
class AgentProvider(Protocol):
    """Abstract contract for multi-turn agent execution with tool use."""

    async def create_session(
        self,
        *,
        agent_config: AgentConfig | None = None,
    ) -> Session: ...

    async def get_session(self, session_id: str) -> Session: ...

    async def list_sessions(
        self,
        *,
        page_token: str | None = None,
        page_size: int = 100,
    ) -> SessionList: ...

    async def delete_session(self, session_id: str) -> None: ...

    async def create_agent_turn(
        self,
        session_id: str,
        messages: list[Message],
        *,
        stream: bool = False,
    ) -> AgentTurnResult: ...
