"""Capability 12: Evaluation protocol."""

from __future__ import annotations

from typing import Any, Protocol, runtime_checkable

from spec.models.runtime.models import (
    EvalJob,
    EvalJobList,
    ScoreResult,
    ScoringFunctionList,
)


@runtime_checkable
class EvaluationProvider(Protocol):
    """Abstract contract for model and agent evaluation."""

    async def create_eval_job(
        self,
        model: str,
        dataset_id: str,
        scoring_functions: list[str],
    ) -> EvalJob: ...

    async def get_eval_job(self, job_id: str) -> EvalJob: ...

    async def list_eval_jobs(
        self,
        *,
        page_token: str | None = None,
        page_size: int = 100,
    ) -> EvalJobList: ...

    async def list_scoring_functions(self) -> ScoringFunctionList: ...

    async def score(
        self,
        scoring_function_id: str,
        inputs: list[dict[str, Any]],
    ) -> ScoreResult: ...
