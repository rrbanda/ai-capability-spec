"""Capability 11: Knowledge / RAG protocol."""

from __future__ import annotations

from typing import Any, Protocol, runtime_checkable

from spec.models.runtime.models import (
    ChunkingConfig,
    DocumentInput,
    InsertResult,
    QueryResult,
    VectorStore,
    VectorStoreList,
)


@runtime_checkable
class KnowledgeProvider(Protocol):
    """Abstract contract for vector stores and semantic search."""

    async def create_vector_store(
        self,
        name: str,
        embedding_model: str,
        *,
        dimensions: int | None = None,
        config: dict[str, Any] | None = None,
    ) -> VectorStore: ...

    async def get_vector_store(self, store_id: str) -> VectorStore: ...

    async def list_vector_stores(
        self,
        *,
        page_token: str | None = None,
        page_size: int = 100,
    ) -> VectorStoreList: ...

    async def delete_vector_store(self, store_id: str) -> None: ...

    async def insert_documents(
        self,
        store_id: str,
        documents: list[DocumentInput],
        *,
        chunking: ChunkingConfig | None = None,
    ) -> InsertResult: ...

    async def query_documents(
        self,
        store_id: str,
        query: str,
        *,
        top_k: int = 10,
        filters: dict[str, Any] | None = None,
    ) -> QueryResult: ...
