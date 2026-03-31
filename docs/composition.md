# Provider Composition

This document explains how multiple providers combine to cover the full AI
capability stack. The spec supports **composed stacks** where different
providers handle different layers.

---

## Why Composition?

No single backend covers all 18 capabilities. A Kubernetes-based platform
excels at workspaces, training, and deployments but does not serve inference.
An inference backend like vLLM or Ollama handles chat completions but knows
nothing about training jobs or pipelines.

The spec solves this by letting you **compose** multiple providers, each
implementing the capabilities it supports:

```
┌─────────────────────────────────────────┐
│            AI Agent / App               │
├─────────────────────────────────────────┤
│         Capability Router               │
│                                         │
│  inference ──► Runtime Provider         │
│  agents    ──► Runtime Provider         │
│  safety    ──► Runtime Provider         │
│  training  ──► Platform Provider        │
│  workspaces──► Platform Provider        │
│  storage   ──► Platform Provider        │
│  registry  ──► Cross-cutting Provider   │
├─────────────────────────────────────────┤
│          Provider Layer                 │
│  ┌───────────┐  ┌──────────────────┐    │
│  │  Ollama   │  │  Kubeflow       │    │
│  │ Provider  │  │  Provider        │    │
│  └───────────┘  └──────────────────┘    │
└─────────────────────────────────────────┘
```

---

## Provider Manifests

Each provider declares a **manifest** listing the capabilities it supports:

```python
from spec.models.common import Capability, ProviderManifest

# A Kubernetes-based platform provider
kubeflow_manifest = ProviderManifest(
    name="kubeflow",
    version="0.1.0",
    description="Kubeflow on Kubernetes platform provider",
    capabilities={
        Capability.WORKSPACES,
        Capability.NOTEBOOKS,
        Capability.DEPLOYMENTS,
        Capability.TRAINING,
        Capability.PIPELINES,
        Capability.STORAGE,
        Capability.CLUSTER_RESOURCES,
        Capability.MODEL_REGISTRY,
    },
)

# A cloud-native platform provider
sagemaker_manifest = ProviderManifest(
    name="sagemaker",
    version="0.1.0",
    description="AWS SageMaker platform provider",
    capabilities={
        Capability.WORKSPACES,
        Capability.TRAINING,
        Capability.DEPLOYMENTS,
        Capability.STORAGE,
        Capability.DATASETS,
    },
)

# A local inference provider
ollama_manifest = ProviderManifest(
    name="ollama",
    version="0.1.0",
    description="Ollama local inference provider",
    capabilities={
        Capability.INFERENCE,
    },
)
```

---

## Capability Router

The **capability router** is the central component that dispatches operations
to the correct provider based on which capability the operation belongs to.

### Registration

```python
from spec.protocols.platform.workspace import WorkspaceProvider
from spec.protocols.runtime.inference import InferenceProvider

class CapabilityRouter:
    def __init__(self) -> None:
        self._providers: dict[str, object] = {}

    def register(self, capability: str, provider: object) -> None:
        self._providers[capability] = provider

    def get(self, capability: str) -> object:
        provider = self._providers.get(capability)
        if provider is None:
            raise ValueError(f"No provider registered for {capability}")
        return provider

router = CapabilityRouter()
router.register("workspaces", kubeflow_workspace_provider)
router.register("training", sagemaker_training_provider)
router.register("inference", ollama_inference_provider)
```

### Dispatch

When an agent needs to call an operation, the router resolves the provider:

```python
# Agent wants to create a workspace:
workspace_provider: WorkspaceProvider = router.get("workspaces")
workspace = await workspace_provider.create_workspace("my-project")

# Agent wants to run inference:
inference_provider: InferenceProvider = router.get("inference")
result = await inference_provider.chat_completion(
    model="llama3",
    messages=[Message(role="user", content="Hello")],
)
```

---

## Composition Patterns

### Pattern 1: Platform + Runtime

The most common composition. One provider handles infrastructure, another
handles inference and agentic execution.

```
Platform Provider (Kubeflow on K8s):
  workspaces, notebooks, deployments, training,
  pipelines, storage, cluster_resources, model_registry

Runtime Provider (Ollama):
  inference
```

### Pattern 2: Full-Stack Runtime + Platform

A full-featured runtime provider (like Llama Stack) covers inference, agents,
safety, RAG, evaluation, datasets, and prompts. A platform provider covers
infrastructure.

```
Platform Provider (Kubeflow on K8s):
  workspaces, notebooks, deployments, training, pipelines, storage

Runtime Provider (Llama Stack):
  inference, agents, safety, knowledge, evaluation,
  datasets, prompts, files, tool_runtime
```

### Pattern 3: Multi-Provider Runtime

Different runtime capabilities served by different providers. For example,
inference from one backend, safety from another.

```
Platform Provider (SageMaker):
  workspaces, training, deployments, storage

Inference Provider (Anthropic):
  inference

Safety Provider (Guardrails AI):
  safety

Knowledge Provider (Pinecone):
  knowledge
```

### Pattern 4: Single Provider

A monolithic platform that covers everything. The composition model still
works -- you just register one provider for all capabilities.

```
Full-Stack Provider (hypothetical):
  all 18 capabilities
```

---

## Conflict Resolution

When two providers declare the same capability, the composition framework
must resolve the conflict. Strategies:

1. **First-registered wins** -- The first provider registered for a capability
   takes precedence. Simple but inflexible.

2. **Explicit priority** -- The configuration specifies which provider to prefer
   for each capability:

   ```python
   config = {
       "inference": {"provider": "ollama", "fallback": "openai"},
       "workspaces": {"provider": "kubeflow"},
       "training": {"provider": "sagemaker"},
   }
   ```

3. **Routing rules** -- Different requests route to different providers based
   on criteria (e.g., model name, workspace labels):

   ```python
   # Route inference based on model name
   if model.startswith("llama"):
       return ollama_provider
   elif model.startswith("claude"):
       return anthropic_provider
   ```

---

## Health and Discovery

The `ProviderManagement` capability (17) provides a unified view of all
registered providers, their health, and their capabilities:

```python
# List all providers
providers = await router.get("provider_management").list_providers()

# Check health of a specific provider
health = await router.get("provider_management").health_check("kubeflow")

# Discover what a provider supports
caps = await router.get("provider_management").get_provider_capabilities("sagemaker")
```

This enables agents to dynamically discover what operations are available
and adapt their behavior when a provider is unhealthy or missing.

---

## Data Flow Between Providers

Some workflows span multiple providers. For example, training a model
(platform) and then deploying it for inference (platform), then calling
it for chat completion (runtime). Data flows between providers through
the spec's canonical models:

```
1. Training Provider creates TrainingJob → outputs model artifact URI
2. Deployment Provider creates Deployment using the model URI
3. Inference Provider calls the deployed endpoint for chat_completion
```

The spec's vendor-neutral data models (Workspace, TrainingJob, Deployment,
CompletionResult, etc.) serve as the interchange format between providers.
Each provider translates these models to/from its native format internally.

---

## Configuration Example

YAML configurations for two different composed stacks:

```yaml
# Example 1: Kubeflow on K8s + Ollama (on-premise / self-hosted)
providers:
  - name: kubeflow
    type: kubeflow
    config:
      kubeconfig: ~/.kube/config
      context: my-cluster
    capabilities:
      - workspaces
      - notebooks
      - deployments
      - training
      - pipelines
      - storage
      - cluster_resources
      - model_registry

  - name: ollama
    type: ollama
    config:
      base_url: http://localhost:11434
    capabilities:
      - inference

routing:
  inference:
    provider: ollama
  workspaces:
    provider: kubeflow
  training:
    provider: kubeflow
```

```yaml
# Example 2: SageMaker + Anthropic (cloud-native)
providers:
  - name: sagemaker
    type: sagemaker
    config:
      region: us-east-1
      role_arn: arn:aws:iam::123456:role/ml-role
    capabilities:
      - workspaces
      - training
      - deployments
      - storage
      - datasets

  - name: anthropic
    type: anthropic
    config:
      api_key_env: ANTHROPIC_API_KEY
    capabilities:
      - inference
      - agents

routing:
  inference:
    provider: anthropic
  agents:
    provider: anthropic
  workspaces:
    provider: sagemaker
  training:
    provider: sagemaker
```
