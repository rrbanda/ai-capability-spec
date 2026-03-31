# Contributing to the Unified AI Capability Spec

Thank you for your interest in contributing. This document provides guidelines
for contributing to the project.

## How to Contribute

### Reporting Issues

- Use GitHub Issues to report bugs or suggest enhancements.
- Check existing issues before creating a new one.
- Include as much context as possible: what you expected, what happened, and
  steps to reproduce.

### Proposing New Capabilities

The capability taxonomy is the heart of this spec. To propose a new capability
or modify an existing one:

1. Open a GitHub Issue with the `capability-proposal` label.
2. Include:
   - **Name** -- The capability name.
   - **Layer** -- Platform, Runtime, or Cross-cutting.
   - **Operations** -- What operations it would include.
   - **Provider examples** -- At least two different providers that could
     implement it, demonstrating vendor neutrality.
   - **Justification** -- Why this capability deserves its own abstraction
     rather than being part of an existing capability.
3. The maintainers will discuss the proposal and decide on acceptance.

### Modifying OpenAPI Specs

When changing `spec/openapi/*.yaml`:

- Follow OpenAPI 3.1.0 conventions.
- Use the spec's own neutral paths under `/capabilities/`.
- Do not copy paths or payload shapes from any vendor's API.
- Every endpoint must have corresponding Protocol methods and Pydantic models.
- Run the OpenAPI linter before submitting.

### Modifying Protocol Classes

When changing `spec/protocols/`:

- Use `typing.Protocol` with `@runtime_checkable`.
- All methods must be `async`.
- Use vendor-neutral parameter names and types.
- Reference canonical data models from `spec/models/`.
- Add type hints for all parameters and return types.

### Modifying Data Models

When changing `spec/models/`:

- Use Pydantic `BaseModel` classes.
- Use vendor-neutral field names.
- Document non-obvious fields with `Field(description=...)`.
- Keep models minimal -- only include fields that providers need for
  interoperability.

## Development Setup

```bash
# Clone the repository
git clone https://github.com/rrbanda/ai-capability-spec.git
cd ai-capability-spec

# Install dependencies (for validation and testing)
pip install pydantic pyyaml

# Validate OpenAPI specs
python -c "import yaml; yaml.safe_load(open('spec/openapi/platform.yaml'))"
python -c "import yaml; yaml.safe_load(open('spec/openapi/runtime.yaml'))"
python -c "import yaml; yaml.safe_load(open('spec/openapi/cross-cutting.yaml'))"
```

## Pull Request Process

1. Fork the repository and create a branch from `main`.
2. Make your changes following the guidelines above.
3. Ensure all specs are valid YAML and all Python files pass type checking.
4. Update documentation if your changes affect the capability taxonomy,
   composition model, or landscape analysis.
5. Submit a pull request with a clear description of the changes.
6. At least one maintainer must approve the PR before merging.

## Commit Messages

- Use imperative mood: "Add workspace capability" not "Added workspace
  capability".
- Keep the first line under 72 characters.
- Reference related issues with `#123`.

## Code of Conduct

This project follows the [Contributor Covenant Code of Conduct](CODE_OF_CONDUCT.md).
By participating, you are expected to uphold this code.

## License

By contributing, you agree that your contributions will be licensed under the
Apache License 2.0.
