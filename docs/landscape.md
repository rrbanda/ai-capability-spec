# AI Interop -- Landscape

This document maps the current AI platform landscape and explains where the
AI Interop project fits. Every project listed here is treated as an
**equal potential provider** -- none is privileged or prescribed by the spec.

---

## The Problem

Today, building an end-to-end AI application requires stitching together
multiple, incompatible APIs:

- **Inference** -- OpenAI, Anthropic, Google, Ollama, vLLM each expose different
  HTTP paths, payload shapes, and streaming formats.
- **Agentic execution** -- OpenAI Responses API, Anthropic tool-use, LangGraph,
  Llama Stack agents each model multi-turn agent loops differently.
- **Platform infrastructure** -- RHOAI, Kubeflow, SageMaker, Vertex AI each
  manage training jobs, notebooks, model deployments, and pipelines through
  completely different APIs.

There is no vendor-neutral specification that defines **what** these capabilities
are, **what** their inputs and outputs look like, and **what** contract a backend
must fulfill -- independent of any single vendor's wire format.

---

## Landscape Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                    Runtime / Agentic Layer                          │
│                                                                     │
│   OpenAI API    Anthropic API    Google AI    Ollama    vLLM        │
│   Llama Stack   LangGraph        Bedrock     Cohere    Mistral     │
│                                                                     │
│   Capabilities: inference, agents, RAG, safety, evaluation,        │
│                 datasets, prompts, file management                  │
├─────────────────────────────────────────────────────────────────────┤
│                 Platform / Infrastructure Layer                     │
│                                                                     │
│   RHOAI         Kubeflow         SageMaker   Vertex AI   Azure ML  │
│   agent-sandbox  MLflow          Ray         Anyscale              │
│                                                                     │
│   Capabilities: workspaces, notebooks, training, deployment,       │
│                 pipelines, storage, cluster resources               │
├─────────────────────────────────────────────────────────────────────┤
│                      Cross-Cutting                                  │
│                                                                     │
│   Model registries, provider discovery, tool runtimes              │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘

                              ▲
                              │
                    ┌─────────┴──────────┐
                    │  AI Interop defines │
                    │  abstract contracts │
                    │  for ALL of the     │
                    │  above capabilities │
                    └────────────────────┘
```

---

## Existing Projects

### Runtime / Agentic Layer

#### OpenAI API

- **Scope**: Inference (chat completions, embeddings, images, audio), agentic
  execution (Responses API), file management, vector stores, fine-tuning.
- **API style**: REST with proprietary paths (`/v1/chat/completions`,
  `/v1/responses`).
- **Limitations**: Proprietary, single-vendor. Many projects clone its paths as a
  de facto convention, but it is not a neutral standard and its schema changes
  are controlled by one company.
- **Relationship to this spec**: One possible provider for runtime capabilities
  (inference, agents, knowledge, files). Not the spec itself.

#### Anthropic API

- **Scope**: Inference (Messages API with tool use), streaming, prompt caching.
- **API style**: REST with its own paths and payload format (`/v1/messages`),
  distinct from OpenAI.
- **Limitations**: Proprietary, single-vendor. Different message format, tool-use
  model, and streaming protocol from OpenAI.
- **Relationship to this spec**: One possible provider for inference and agentic
  capabilities.

#### Google AI (Gemini / Vertex AI)

- **Scope**: Inference, multimodal, grounding, code execution.
- **API style**: REST with Google-specific paths and proto-based payloads.
- **Limitations**: Proprietary, tightly coupled to Google Cloud.
- **Relationship to this spec**: One possible provider for runtime capabilities.

#### Ollama

- **Scope**: Local model inference (chat, generate, embeddings).
- **API style**: REST with its own paths (`/api/chat`, `/api/generate`).
- **Limitations**: Inference-only, no agentic runtime, no safety, no RAG.
- **Relationship to this spec**: One possible provider for inference capability.

#### vLLM

- **Scope**: High-performance inference serving.
- **API style**: Happens to expose OpenAI-compatible paths, but is a separate
  project with its own extensions.
- **Limitations**: Inference-only serving engine.
- **Relationship to this spec**: One possible provider for inference capability.

#### Llama Stack

- **Scope**: Inference, agents, RAG (vector I/O), safety (shields), evaluation,
  datasets, prompts, file management, tool runtime, provider management.
- **API style**: REST, copies OpenAI-compatible paths for inference.
- **Provider pattern**: Yes -- pluggable backends for each capability.
- **Limitations**: Does not cover platform infrastructure (no training jobs,
  workspaces, notebooks, pipelines, or storage management). Tied to
  OpenAI-compatible paths for inference.
- **Relationship to this spec**: Prior art for the provider pattern and runtime
  capability taxonomy. One possible runtime provider.

#### LangGraph / LangChain

- **Scope**: Agent orchestration, tool execution, graph-based workflows.
- **API style**: Python SDK, not REST-first.
- **Limitations**: Framework, not a spec. Tightly coupled to LangChain ecosystem.
- **Relationship to this spec**: One possible provider for agentic runtime.

### Platform / Infrastructure Layer

#### Red Hat OpenShift AI (RHOAI)

- **Scope**: Data science projects, Kubeflow Notebooks, KServe model serving,
  Kubeflow Training Operator, Data Science Pipelines, PVC/Secret storage,
  model registry, model catalog, cluster resource queries.
- **API style**: Kubernetes CRDs + HTTP REST APIs for model registry/catalog.
- **Limitations**: Tied to OpenShift/Kubernetes. RHOAI-specific labels,
  annotations, and operator configurations.
- **Relationship to this spec**: Reference implementation for platform
  capabilities. One possible platform provider.

#### Kubeflow (Standalone)

- **Scope**: Notebooks, Training Operator, Pipelines, KServe, Model Registry.
- **API style**: Kubernetes CRDs.
- **Limitations**: Requires Kubernetes. Each sub-project has independent APIs.
- **Relationship to this spec**: One possible platform provider for training,
  notebooks, pipelines, and serving capabilities.

#### Amazon SageMaker

- **Scope**: Notebooks, training jobs, endpoints, pipelines, model registry,
  feature store, data labeling.
- **API style**: AWS REST APIs with IAM authentication.
- **Limitations**: Proprietary, AWS-only.
- **Relationship to this spec**: One possible cloud-native platform provider.

#### Google Vertex AI

- **Scope**: Notebooks, training, endpoints, pipelines, model registry,
  feature store, experiments.
- **API style**: Google Cloud REST APIs with service account auth.
- **Limitations**: Proprietary, GCP-only.
- **Relationship to this spec**: One possible cloud-native platform provider.

#### Azure Machine Learning

- **Scope**: Compute instances, training, endpoints, pipelines, model registry,
  data assets.
- **API style**: Azure REST APIs with AAD authentication.
- **Limitations**: Proprietary, Azure-only.
- **Relationship to this spec**: One possible cloud-native platform provider.

#### agent-sandbox (kubernetes-sigs)

- **Scope**: Isolated agent runtime environments via a Sandbox CRD.
- **API style**: Kubernetes CRD.
- **Limitations**: Narrow scope -- sandbox lifecycle only.
- **Relationship to this spec**: Complementary. Maps to a subset of the
  Workspace Management capability.

### Cross-Cutting

#### MLflow

- **Scope**: Experiment tracking, model registry, model deployment.
- **API style**: REST + Python SDK.
- **Relationship to this spec**: One possible provider for model registry and
  evaluation capabilities.

#### HuggingFace Hub

- **Scope**: Model hosting, dataset hosting, model cards.
- **API style**: REST + Python SDK.
- **Relationship to this spec**: One possible provider for model registry and
  dataset capabilities.

---

## Where AI Interop Fits

This spec does **not** compete with any of the projects listed above. Instead,
it defines a **neutral abstraction layer** that sits between AI agents/applications
and the backends they use:

```
┌──────────────────────────────┐
│      AI Agent / Application  │
├──────────────────────────────┤
│   Unified Capability Spec    │  <── abstract contracts
│   (protocols + data models)  │
├──────────────────────────────┤
│        Provider Layer        │
│  ┌────────┐  ┌────────────┐  │
│  │ Runtime │  │  Platform  │  │  <── concrete implementations
│  │Provider │  │  Provider  │  │
│  └────┬───┘  └─────┬──────┘  │
│       │            │         │
│  OpenAI /     RHOAI /        │
│  Anthropic /  Kubeflow /     │
│  Ollama /     SageMaker /    │
│  vLLM / ...   Vertex / ...   │
└──────────────────────────────┘
```

### What the spec provides

1. **Capability taxonomy** -- 18 named capabilities organized into platform,
   runtime, and cross-cutting layers.
2. **Abstract contracts** -- Python Protocol classes defining operations, inputs,
   and outputs for each capability.
3. **Canonical data models** -- Vendor-neutral Pydantic models (Message,
   CompletionResult, TrainingJob, Workspace, etc.) that providers translate
   to/from their native formats.
4. **OpenAPI surface** -- Optional REST gateway using the spec's own neutral
   paths (not copied from any vendor).
5. **Provider manifest** -- A declaration mechanism for providers to advertise
   which capabilities they support.
6. **Composition model** -- How multiple providers (e.g., one for runtime, one
   for platform) combine to cover the full AI stack.

### What the spec does NOT do

- Does **not** prescribe any vendor's HTTP paths or payload formats.
- Does **not** privilege OpenAI, Anthropic, Llama Stack, or any other project.
- Does **not** implement providers -- it defines the contracts they must fulfill.
- Does **not** replace MCP, gRPC, or other transport protocols -- providers can
  use any transport internally.

---

## Comparison Matrix

| Aspect | OpenAI | Anthropic | Llama Stack | RHOAI | Kubeflow | SageMaker | AI Interop |
|---|---|---|---|---|---|---|---|
| Vendor neutral | No | No | Partial | No | Yes | No | **Yes** |
| Platform infra | No | No | No | Yes | Yes | Yes | **Yes** |
| Runtime/agentic | Yes | Yes | Yes | No | No | Partial | **Yes** |
| Provider pattern | No | No | Yes | Partial | No | No | **Yes** |
| Abstract contracts | No | No | No | No | No | No | **Yes** |
| Covers full stack | No | No | No | No | No | Partial | **Yes** |

---

## Design Principles

1. **Capability-first** -- Define what operations exist, not how they are wired.
2. **Vendor-neutral** -- No vendor's API format is baked into the spec.
3. **Provider equality** -- Every backend is a first-class provider candidate.
4. **Composable** -- Mix providers across layers (runtime + platform).
5. **Minimal** -- Only define what is needed for interoperability.
6. **Extensible** -- Providers can expose additional vendor-specific features
   beyond the spec's contracts.
