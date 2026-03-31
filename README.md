# Unified AI Capability Spec

A vendor-neutral specification defining abstract capability contracts for the
full AI stack -- from platform infrastructure through agentic runtime.

## The Problem

Building end-to-end AI applications today requires integrating multiple
incompatible APIs across inference providers, agent frameworks, and platform
infrastructure. There is no neutral standard that defines **what** these
capabilities are and **what** contracts a backend must fulfill.

## What This Spec Provides

- **18 capability definitions** across platform, runtime, and cross-cutting
  layers
- **Python Protocol classes** defining abstract operation contracts
- **Vendor-neutral data models** (Pydantic) for interchange between providers
- **OpenAPI surface** with the spec's own neutral paths
- **Provider composition model** for combining multiple backends

## Vendor Neutrality

This spec does **not** prescribe any vendor's HTTP paths, payload formats, or
wire protocols. OpenAI, Anthropic, Llama Stack, RHOAI, Kubeflow, SageMaker --
all are treated as equal potential provider implementations.

## Capability Taxonomy

### Platform / Infrastructure (1-7)

| # | Capability | Description |
|---|---|---|
| 1 | Workspace Management | Isolated project environments |
| 2 | Interactive Development | Notebook/IDE lifecycle |
| 3 | Model Deployment | Deploy models as endpoints |
| 4 | Model Training | Distributed training jobs |
| 5 | Pipeline Orchestration | ML pipeline infrastructure |
| 6 | Persistent Storage | Volumes and data connections |
| 7 | Cluster Resources | Compute capacity queries |

### Runtime / Agentic (8-15)

| # | Capability | Description |
|---|---|---|
| 8 | Inference | Chat, completions, embeddings, reranking |
| 9 | Agentic Runtime | Multi-turn agent execution |
| 10 | Safety and Guardrails | Content moderation, shields |
| 11 | Knowledge / RAG | Vector stores, semantic search |
| 12 | Evaluation | Benchmarks, scoring |
| 13 | Datasets | Dataset registration and access |
| 14 | Prompt Management | Versioned prompt templates |
| 15 | File Management | File upload and retrieval |

### Cross-Cutting (16-18)

| # | Capability | Description |
|---|---|---|
| 16 | Model Registry | Model metadata management |
| 17 | Provider Management | Provider discovery and health |
| 18 | Tool Runtime | Tool registration and invocation |

## Project Structure

```
spec/
  openapi/
    platform.yaml        # Platform capabilities (1-7)
    runtime.yaml         # Runtime capabilities (8-15)
    cross-cutting.yaml   # Cross-cutting capabilities (16-18)
  protocols/             # Python Protocol classes
    platform/            # Capabilities 1-7
    runtime/             # Capabilities 8-15
    cross_cutting/       # Capabilities 16-18
  models/                # Pydantic data models
    common.py            # Shared types
    platform/            # Platform models
    runtime/             # Runtime models
docs/
  landscape.md           # How this spec relates to existing projects
  taxonomy.md            # Complete capability taxonomy
  composition.md         # Provider composition model
```

## How It Works

1. **Define capabilities** -- Each capability has a Python Protocol with typed
   operations:

   ```python
   class InferenceProvider(Protocol):
       async def chat_completion(
           self, model: str, messages: list[Message], **kwargs
       ) -> CompletionResult: ...
   ```

2. **Implement providers** -- Providers translate abstract operations to their
   native API:

   ```python
   class OllamaInferenceProvider:
       async def chat_completion(self, model, messages, **kwargs):
           # Translates to Ollama's /api/chat endpoint
           ...
   ```

3. **Compose providers** -- Mix providers from different vendors to cover
   the full stack:

   ```python
   router.register("inference", OllamaInferenceProvider(...))
   router.register("workspaces", KubeflowWorkspaceProvider(...))
   router.register("training", SageMakerTrainingProvider(...))
   ```

## Documentation

- [Landscape Analysis](docs/landscape.md) -- Where this spec fits
- [Capability Taxonomy](docs/taxonomy.md) -- All 18 capabilities in detail
- [Provider Composition](docs/composition.md) -- How providers combine

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for development guidelines.

## License

This project is licensed under the Apache License 2.0. See [LICENSE](LICENSE)
for details.
