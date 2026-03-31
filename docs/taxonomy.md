# Capability Taxonomy

This document defines the complete set of 18 capabilities, their operations,
and how existing platforms map to each capability.

---

## Layer 1: Platform / Infrastructure

Capabilities that manage the lifecycle of AI resources on a compute platform.

---

### 1. Workspace Management

Isolated project environments that scope resources, access control, and billing.

#### Operations

| Operation | Description | Inputs | Outputs |
|---|---|---|---|
| `create_workspace` | Create a new workspace | name, labels, resource_quotas | Workspace |
| `get_workspace` | Retrieve workspace details | workspace_id | Workspace |
| `list_workspaces` | List all accessible workspaces | filters, pagination | list[Workspace] |
| `update_workspace` | Modify workspace metadata or quotas | workspace_id, patches | Workspace |
| `delete_workspace` | Remove a workspace and its resources | workspace_id | None |

#### Provider Mapping

| Provider | Native Concept | Notes |
|---|---|---|
| RHOAI | OpenShift Project (Namespace + labels) | Uses `opendatahub.io/dashboard` label |
| Kubeflow | Kubernetes Namespace + Profile | Kubeflow Profile CRD |
| SageMaker | SageMaker Domain / Studio Space | AWS-managed environment |
| Vertex AI | Google Cloud Project | GCP project scoping |
| Azure ML | Azure ML Workspace | ARM resource |

---

### 2. Interactive Development

Notebook and IDE instances for interactive experimentation.

#### Operations

| Operation | Description | Inputs | Outputs |
|---|---|---|---|
| `create_notebook` | Launch a notebook instance | workspace_id, name, image, resources | Notebook |
| `get_notebook` | Retrieve notebook details | workspace_id, notebook_id | Notebook |
| `list_notebooks` | List notebooks in a workspace | workspace_id, filters | list[Notebook] |
| `start_notebook` | Start a stopped notebook | workspace_id, notebook_id | Notebook |
| `stop_notebook` | Stop a running notebook | workspace_id, notebook_id | Notebook |
| `delete_notebook` | Remove a notebook instance | workspace_id, notebook_id | None |

#### Provider Mapping

| Provider | Native Concept | Notes |
|---|---|---|
| RHOAI | Kubeflow Notebook CR | Custom images, PVC mounts |
| Kubeflow | Kubeflow Notebook CR | Same CRD, different labels |
| SageMaker | SageMaker Notebook Instance | Or Studio Notebook |
| Vertex AI | Vertex AI Workbench | Managed or user-managed |
| Google Colab | Colab Runtime | Cloud-hosted notebooks |

---

### 3. Model Deployment

Deploy trained models as inference endpoints.

#### Operations

| Operation | Description | Inputs | Outputs |
|---|---|---|---|
| `create_deployment` | Deploy a model to an endpoint | workspace_id, name, model_uri, runtime, resources | Deployment |
| `get_deployment` | Retrieve deployment details | workspace_id, deployment_id | Deployment |
| `list_deployments` | List deployments in a workspace | workspace_id, filters | list[Deployment] |
| `update_deployment` | Modify deployment config (scaling, model) | workspace_id, deployment_id, patches | Deployment |
| `delete_deployment` | Remove a deployment | workspace_id, deployment_id | None |
| `get_deployment_status` | Check readiness and health | workspace_id, deployment_id | DeploymentStatus |

#### Provider Mapping

| Provider | Native Concept | Notes |
|---|---|---|
| RHOAI | KServe InferenceService CR | Supports multiple runtimes |
| Kubeflow | KServe InferenceService CR | Same CRD |
| SageMaker | SageMaker Endpoint | Endpoint + EndpointConfig |
| Vertex AI | Vertex AI Endpoint | Model deployment to endpoint |
| Azure ML | Azure ML Online Endpoint | Managed or K8s |

---

### 4. Model Training

Submit, monitor, and manage distributed training jobs.

#### Operations

| Operation | Description | Inputs | Outputs |
|---|---|---|---|
| `create_training_job` | Submit a training job | workspace_id, name, model, dataset, runtime, resources | TrainingJob |
| `get_training_job` | Retrieve job details | workspace_id, job_id | TrainingJob |
| `list_training_jobs` | List training jobs | workspace_id, filters | list[TrainingJob] |
| `cancel_training_job` | Cancel a running job | workspace_id, job_id | TrainingJob |
| `delete_training_job` | Remove a completed/failed job | workspace_id, job_id | None |
| `get_training_logs` | Stream or fetch job logs | workspace_id, job_id, container | LogStream |
| `list_training_runtimes` | List available training runtimes | filters | list[TrainingRuntime] |

#### Provider Mapping

| Provider | Native Concept | Notes |
|---|---|---|
| RHOAI | Kubeflow TrainJob CR + ClusterTrainingRuntime | Training Operator v2 |
| Kubeflow | Kubeflow TrainJob CR | Same operator |
| SageMaker | SageMaker Training Job | Managed training |
| Vertex AI | Vertex AI Custom Training Job | Custom or AutoML |
| Azure ML | Azure ML Training Job | Compute targets |
| Ray | RayJob CR | Ray-based distributed training |

---

### 5. Pipeline Orchestration

ML pipeline infrastructure for repeatable workflows.

#### Operations

| Operation | Description | Inputs | Outputs |
|---|---|---|---|
| `create_pipeline_server` | Deploy pipeline infrastructure | workspace_id, name, config | PipelineServer |
| `get_pipeline_server` | Retrieve server details | workspace_id, server_id | PipelineServer |
| `list_pipeline_servers` | List pipeline servers | workspace_id | list[PipelineServer] |
| `delete_pipeline_server` | Remove pipeline infrastructure | workspace_id, server_id | None |
| `get_pipeline_server_status` | Check server readiness | workspace_id, server_id | PipelineServerStatus |

#### Provider Mapping

| Provider | Native Concept | Notes |
|---|---|---|
| RHOAI | DataSciencePipelinesApplication CR | Deploys Argo + ML Metadata |
| Kubeflow | Kubeflow Pipelines deployment | Similar architecture |
| SageMaker | SageMaker Pipelines | Managed, no server concept |
| Vertex AI | Vertex AI Pipelines | Managed, no server concept |
| Azure ML | Azure ML Pipelines | Managed service |

---

### 6. Persistent Storage

Storage volumes and credential connections for AI workloads.

#### Operations

| Operation | Description | Inputs | Outputs |
|---|---|---|---|
| `create_storage` | Create a persistent storage volume | workspace_id, name, size, storage_class | StorageVolume |
| `get_storage` | Retrieve storage details | workspace_id, storage_id | StorageVolume |
| `list_storage` | List storage volumes | workspace_id, filters | list[StorageVolume] |
| `delete_storage` | Remove a storage volume | workspace_id, storage_id | None |
| `create_connection` | Create a data connection (credentials) | workspace_id, name, type, credentials | Connection |
| `get_connection` | Retrieve connection details | workspace_id, connection_id | Connection |
| `list_connections` | List connections | workspace_id, filters | list[Connection] |
| `delete_connection` | Remove a connection | workspace_id, connection_id | None |

#### Provider Mapping

| Provider | Native Concept | Notes |
|---|---|---|
| RHOAI | PVC + Secret (with `opendatahub.io` labels) | S3-compatible connections |
| Kubeflow | PVC + Secret | Standard K8s resources |
| SageMaker | S3 Bucket + IAM Role | AWS-native storage |
| Vertex AI | GCS Bucket + Service Account | GCP-native storage |
| Azure ML | Azure Blob + Managed Identity | Azure-native storage |

---

### 7. Cluster Resources

Query compute capacity available on the platform.

#### Operations

| Operation | Description | Inputs | Outputs |
|---|---|---|---|
| `list_compute_nodes` | List available compute nodes | filters | list[ComputeNode] |
| `get_cluster_summary` | Aggregate capacity summary | None | ClusterSummary |
| `list_accelerator_profiles` | List GPU/accelerator types | None | list[AcceleratorProfile] |
| `list_storage_classes` | List available storage classes | None | list[StorageClass] |

#### Provider Mapping

| Provider | Native Concept | Notes |
|---|---|---|
| RHOAI | K8s Nodes + AcceleratorProfile CR | OpenShift node queries |
| Kubeflow | K8s Nodes | Standard node listing |
| SageMaker | Instance Type catalog | AWS instance types |
| Vertex AI | Machine Type catalog | GCP machine types |
| Azure ML | VM Size catalog | Azure VM sizes |

---

## Layer 2: Runtime / Agentic

Capabilities that interact with running AI services.

---

### 8. Inference

Generate text, embeddings, and reranked results from language models.

#### Operations

| Operation | Description | Inputs | Outputs |
|---|---|---|---|
| `chat_completion` | Multi-turn chat generation | model, messages, params | CompletionResult |
| `completion` | Single-prompt text generation | model, prompt, params | CompletionResult |
| `embeddings` | Generate vector embeddings | model, inputs | EmbeddingsResult |
| `rerank` | Rerank documents by relevance | model, query, documents | RerankResult |

#### Provider Mapping

| Provider | Native API | Notes |
|---|---|---|
| OpenAI | `/v1/chat/completions`, `/v1/embeddings` | Proprietary paths |
| Anthropic | `/v1/messages` | Different message format |
| Google Gemini | `generateContent` | Proto-based |
| Ollama | `/api/chat`, `/api/embeddings` | Local inference |
| vLLM | OpenAI-compatible paths | Serving engine |
| Llama Stack | OpenAI-compatible paths | Provider-based |
| Bedrock | AWS SDK | AWS-native |

---

### 9. Agentic Runtime

Multi-turn agent execution with tool use and conversation management.

#### Operations

| Operation | Description | Inputs | Outputs |
|---|---|---|---|
| `create_agent_turn` | Execute one agent turn (reason + act) | session_id, messages, stream | AgentTurnResult |
| `create_session` | Start a new agent session | agent_config | Session |
| `get_session` | Retrieve session state | session_id | Session |
| `list_sessions` | List active sessions | filters | list[Session] |
| `delete_session` | End and clean up a session | session_id | None |

#### Provider Mapping

| Provider | Native Concept | Notes |
|---|---|---|
| OpenAI | Responses API (`/v1/responses`) | Built-in tool use |
| Anthropic | Messages API with tool_use blocks | Multi-turn tool use |
| Llama Stack | Agent turns + sessions | Provider pattern |
| LangGraph | Graph-based agent execution | Python SDK |
| Custom | Any agent framework | MCP tool connectors |

---

### 10. Safety and Guardrails

Content moderation and safety shield enforcement.

#### Operations

| Operation | Description | Inputs | Outputs |
|---|---|---|---|
| `moderate` | Check content against safety policies | content, policies | ModerationResult |
| `create_shield` | Register a safety shield | name, config | Shield |
| `list_shields` | List available shields | filters | list[Shield] |
| `get_shield` | Retrieve shield details | shield_id | Shield |

#### Provider Mapping

| Provider | Native Concept | Notes |
|---|---|---|
| Llama Stack | Shields API | Llama Guard integration |
| OpenAI | Moderations API | Content classification |
| Guardrails AI | Guard objects | Rule-based guardrails |
| Custom | Any moderation service | Pluggable |

---

### 11. Knowledge / RAG

Vector stores, document ingestion, and semantic search.

#### Operations

| Operation | Description | Inputs | Outputs |
|---|---|---|---|
| `create_vector_store` | Create a vector store | name, embedding_model, config | VectorStore |
| `get_vector_store` | Retrieve store details | store_id | VectorStore |
| `list_vector_stores` | List vector stores | filters | list[VectorStore] |
| `delete_vector_store` | Remove a vector store | store_id | None |
| `insert_documents` | Add documents to a store | store_id, documents, chunking_config | InsertResult |
| `query_documents` | Semantic search over a store | store_id, query, top_k | list[DocumentChunk] |

#### Provider Mapping

| Provider | Native Concept | Notes |
|---|---|---|
| Llama Stack | Vector I/O API | Built-in chunking |
| OpenAI | Vector Stores API | File-based ingestion |
| Pinecone | Index + Namespace | Managed vector DB |
| Weaviate | Collection | Self-hosted or cloud |
| ChromaDB | Collection | Lightweight, local |
| Qdrant | Collection | High-performance |

---

### 12. Evaluation

Run benchmarks and scoring functions against models or agents.

#### Operations

| Operation | Description | Inputs | Outputs |
|---|---|---|---|
| `create_eval_job` | Run an evaluation benchmark | model, dataset, scoring_functions | EvalJob |
| `get_eval_job` | Retrieve job results | job_id | EvalJob |
| `list_eval_jobs` | List evaluation jobs | filters | list[EvalJob] |
| `list_scoring_functions` | List available scoring functions | None | list[ScoringFunction] |
| `score` | Run a scoring function on data | scoring_function_id, inputs | ScoreResult |

#### Provider Mapping

| Provider | Native Concept | Notes |
|---|---|---|
| Llama Stack | Eval benchmarks + scoring | Built-in eval framework |
| Ragas | Evaluation chains | RAG-focused evaluation |
| DeepEval | Test cases + metrics | Pytest-based |
| MLflow | Experiment tracking | Metric logging |
| Custom | Any evaluation framework | Pluggable |

---

### 13. Datasets

Register, manage, and iterate over datasets for training and evaluation.

#### Operations

| Operation | Description | Inputs | Outputs |
|---|---|---|---|
| `register_dataset` | Register a dataset | name, source, schema | Dataset |
| `get_dataset` | Retrieve dataset metadata | dataset_id | Dataset |
| `list_datasets` | List registered datasets | filters | list[Dataset] |
| `delete_dataset` | Unregister a dataset | dataset_id | None |
| `iterate_rows` | Iterate over dataset rows | dataset_id, pagination | list[Row] |

#### Provider Mapping

| Provider | Native Concept | Notes |
|---|---|---|
| Llama Stack | Datasets + DatasetIO | Provider-based iteration |
| HuggingFace Hub | Dataset repository | Hub API |
| SageMaker | SageMaker Data | S3-backed |
| Custom | Any data store | File, DB, API |

---

### 14. Prompt Management

Versioned prompt templates with variable substitution.

#### Operations

| Operation | Description | Inputs | Outputs |
|---|---|---|---|
| `create_prompt` | Create a prompt template | name, template, variables | Prompt |
| `get_prompt` | Retrieve a prompt | prompt_id | Prompt |
| `list_prompts` | List prompt templates | filters | list[Prompt] |
| `update_prompt` | Update a prompt template | prompt_id, template | Prompt |
| `delete_prompt` | Remove a prompt template | prompt_id | None |
| `render_prompt` | Render a prompt with variables | prompt_id, variable_values | RenderedPrompt |

#### Provider Mapping

| Provider | Native Concept | Notes |
|---|---|---|
| Llama Stack | Prompts API | Built-in versioning |
| LangSmith | Prompt Hub | Cloud-hosted |
| Custom | Any template store | File, DB, API |

---

### 15. File Management

Upload, retrieve, and delete files used by other capabilities.

#### Operations

| Operation | Description | Inputs | Outputs |
|---|---|---|---|
| `upload_file` | Upload a file | content, filename, purpose | File |
| `get_file` | Retrieve file metadata | file_id | File |
| `list_files` | List uploaded files | filters | list[File] |
| `delete_file` | Remove a file | file_id | None |
| `get_file_content` | Download file content | file_id | bytes |

#### Provider Mapping

| Provider | Native Concept | Notes |
|---|---|---|
| Llama Stack | Files API | Local or remote storage |
| OpenAI | Files API | Cloud storage |
| S3 | S3 Objects | AWS-native |
| GCS | GCS Objects | GCP-native |
| Local filesystem | File paths | Development use |

---

## Layer 3: Cross-Cutting

Capabilities that span both layers or provide meta-functionality.

---

### 16. Model Registry

Browse, search, and manage model metadata across sources.

#### Operations

| Operation | Description | Inputs | Outputs |
|---|---|---|---|
| `register_model` | Register a model in the registry | name, version, source, metadata | RegisteredModel |
| `get_model` | Retrieve model details | model_id | RegisteredModel |
| `list_models` | List registered models | filters, pagination | list[RegisteredModel] |
| `create_model_version` | Create a new version of a model | model_id, version_info | ModelVersion |
| `list_model_versions` | List versions of a model | model_id | list[ModelVersion] |
| `search_models` | Search models by criteria | query, filters | list[RegisteredModel] |

#### Provider Mapping

| Provider | Native Concept | Notes |
|---|---|---|
| RHOAI | Kubeflow Model Registry + Model Catalog | Dual registry |
| Kubeflow | Kubeflow Model Registry | REST API |
| MLflow | MLflow Model Registry | REST + SDK |
| HuggingFace Hub | Model repository | Hub API |
| SageMaker | SageMaker Model Registry | AWS-native |

---

### 17. Provider Management

Discover, inspect, and health-check capability providers.

#### Operations

| Operation | Description | Inputs | Outputs |
|---|---|---|---|
| `list_providers` | List registered providers | None | list[Provider] |
| `get_provider` | Retrieve provider details | provider_id | Provider |
| `health_check` | Check provider health | provider_id | HealthStatus |
| `get_provider_capabilities` | List capabilities a provider supports | provider_id | list[Capability] |

#### Provider Mapping

This capability is built into the framework itself and does not map to external
providers. It manages the registry of all other providers.

---

### 18. Tool Runtime

Register, discover, and invoke tools that agents can use.

#### Operations

| Operation | Description | Inputs | Outputs |
|---|---|---|---|
| `register_tool` | Register a tool | name, description, parameters_schema | Tool |
| `list_tools` | List available tools | filters | list[Tool] |
| `get_tool` | Retrieve tool details | tool_id | Tool |
| `invoke_tool` | Execute a tool | tool_id, arguments | ToolResult |
| `register_tool_group` | Register a group of related tools | name, tools | ToolGroup |
| `list_tool_groups` | List tool groups | filters | list[ToolGroup] |

#### Provider Mapping

| Provider | Native Concept | Notes |
|---|---|---|
| MCP Servers | MCP tool protocol | JSON-RPC transport |
| Llama Stack | Tool groups + tool runtime | Provider-based |
| LangChain | Tool classes | Python SDK |
| Custom | Any callable | HTTP, gRPC, etc. |

---

## Summary Table

| # | Capability | Layer | Operations | Key Models |
|---|---|---|---|---|
| 1 | Workspace Management | Platform | 5 | Workspace |
| 2 | Interactive Development | Platform | 6 | Notebook |
| 3 | Model Deployment | Platform | 6 | Deployment, DeploymentStatus |
| 4 | Model Training | Platform | 7 | TrainingJob, TrainingRuntime |
| 5 | Pipeline Orchestration | Platform | 5 | PipelineServer |
| 6 | Persistent Storage | Platform | 8 | StorageVolume, Connection |
| 7 | Cluster Resources | Platform | 4 | ComputeNode, ClusterSummary |
| 8 | Inference | Runtime | 4 | CompletionResult, EmbeddingsResult |
| 9 | Agentic Runtime | Runtime | 5 | AgentTurnResult, Session |
| 10 | Safety and Guardrails | Runtime | 4 | ModerationResult, Shield |
| 11 | Knowledge / RAG | Runtime | 6 | VectorStore, DocumentChunk |
| 12 | Evaluation | Runtime | 5 | EvalJob, ScoringFunction |
| 13 | Datasets | Runtime | 5 | Dataset |
| 14 | Prompt Management | Runtime | 6 | Prompt, RenderedPrompt |
| 15 | File Management | Runtime | 5 | File |
| 16 | Model Registry | Cross-cutting | 6 | RegisteredModel, ModelVersion |
| 17 | Provider Management | Cross-cutting | 4 | Provider, HealthStatus |
| 18 | Tool Runtime | Cross-cutting | 6 | Tool, ToolGroup, ToolResult |
| | **Total** | | **95** | |
