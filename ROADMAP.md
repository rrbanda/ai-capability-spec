# Roadmap

This document outlines the planned development phases for the Unified AI
Capability Spec.

## Phase 0 -- Landscape and Positioning (Current)

- [x] Publish landscape analysis mapping existing projects
- [x] Define the 18-capability taxonomy
- [x] Document the vendor-neutral philosophy
- [x] Define the provider composition model
- [x] Write OpenAPI specs for all three layers
- [x] Write Python Protocol classes for all 18 capabilities
- [x] Write canonical Pydantic data models
- [ ] Community feedback on scope and taxonomy

## Phase 1 -- Platform Spec Validation (Next)

- [ ] RHOAI provider mapping example (K8s API calls to abstract operations)
- [ ] Kubeflow provider mapping example (validates portability)
- [ ] Conformance test suite for platform capabilities
- [ ] Provider implementation guide with code examples
- [ ] Refine platform models based on real-world usage

## Phase 2 -- Runtime Spec Validation

- [ ] Ollama provider example (local inference)
- [ ] Anthropic provider example (cloud inference)
- [ ] Llama Stack provider example (full runtime)
- [ ] Conformance test suite for runtime capabilities
- [ ] Refine runtime models based on real-world usage

## Phase 3 -- Cross-Cutting and Composition

- [ ] Provider management reference implementation
- [ ] Tool runtime with MCP integration example
- [ ] Model registry provider examples (MLflow, HuggingFace Hub)
- [ ] End-to-end composition example (platform + runtime)
- [ ] Routing and conflict resolution framework

## Phase 4 -- Second Provider Per Layer

- [ ] Vanilla Kubeflow platform provider (validates spec beyond RHOAI)
- [ ] Second runtime provider (validates spec beyond single LLM vendor)
- [ ] Cross-provider integration tests
- [ ] Performance benchmarks for provider composition overhead

## Future Considerations

- gRPC / protobuf spec alongside OpenAPI (for high-performance providers)
- SDK generation from OpenAPI specs (Python, Go, TypeScript)
- Certification program for compliant providers
- Streaming protocol standardization for inference and agent turns
- Multi-cluster / multi-cloud composition patterns
