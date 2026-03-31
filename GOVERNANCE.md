# Governance

This document describes the governance model for the Unified AI Capability Spec.

## Roles

### Contributors

Anyone who submits a pull request, opens an issue, or participates in
discussions. Contributors are expected to follow the Code of Conduct.

### Reviewers

Trusted contributors who can review and approve pull requests. Reviewers are
nominated by maintainers based on sustained, high-quality contributions.

### Maintainers

Maintainers have merge access and are responsible for the overall direction of
the project. They:

- Review and merge pull requests
- Triage issues
- Make decisions on capability taxonomy changes
- Manage releases

### Current Maintainers

| Name | GitHub |
|------|--------|
| Raghu Ram Banda | @rrbanda |

## Decision Making

### Consensus-Based

Most decisions are made through discussion on GitHub Issues and Pull Requests.
We aim for consensus among maintainers.

### Capability Taxonomy Changes

Changes to the 18-capability taxonomy (adding, removing, or restructuring
capabilities) require:

1. A formal proposal via GitHub Issue with the `capability-proposal` label.
2. At least 2 weeks of discussion.
3. Approval from at least two maintainers.

### Breaking Changes to Protocols or Models

Changes that break backward compatibility in Protocol classes or Pydantic
models require:

1. A deprecation notice in the current version.
2. A migration guide.
3. Approval from at least two maintainers.

## Adding Maintainers

New maintainers are nominated by existing maintainers and require approval
from a majority of current maintainers. Criteria:

- Sustained contributions over at least 3 months.
- Demonstrated understanding of the project architecture and philosophy.
- Positive interactions with the community.

## Removing Maintainers

Maintainers who are inactive for 6 months may be moved to emeritus status.
Maintainers who violate the Code of Conduct may be removed by a majority
vote of other maintainers.
