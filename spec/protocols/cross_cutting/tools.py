"""Capability 18: Tool Runtime protocol."""

from __future__ import annotations

from typing import Any, Protocol, runtime_checkable

from spec.models.cross_cutting.models import (
    Tool,
    ToolGroup,
    ToolGroupList,
    ToolList,
    ToolResult,
)


@runtime_checkable
class ToolRuntimeProvider(Protocol):
    """Abstract contract for tool registration, discovery, and invocation."""

    async def register_tool(
        self,
        name: str,
        description: str,
        parameters_schema: dict[str, Any],
        *,
        group_id: str | None = None,
    ) -> Tool: ...

    async def list_tools(
        self,
        *,
        page_token: str | None = None,
        page_size: int = 100,
    ) -> ToolList: ...

    async def get_tool(self, tool_id: str) -> Tool: ...

    async def invoke_tool(
        self,
        tool_id: str,
        arguments: dict[str, Any],
    ) -> ToolResult: ...

    async def register_tool_group(
        self,
        name: str,
        tools: list[str],
        *,
        description: str | None = None,
    ) -> ToolGroup: ...

    async def list_tool_groups(self) -> ToolGroupList: ...
