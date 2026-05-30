# 11. Output Validator

## Purpose

The Output Validator checks agent output before it is shown to the user or saved as a completed artifact.

It protects the product from malformed, incomplete, unsupported, or unsafe agent responses.

```text
Agent Executor
-> Output Validator
-> Request Orchestrator
```

## Diagram

```mermaid
flowchart TD
    Executor[Agent Executor] --> Validator[Output Validator]
    Validator --> Shape[Validate Structure]
    Validator --> Safety[Validate Policy and Scope]
    Validator --> Sources[Validate Source Metadata]
    Shape --> Decision{Valid?}
    Safety --> Decision
    Sources --> Decision
    Decision -->|Yes| Accepted[Accepted Output]
    Decision -->|No| Rejected[Structured Validation Failure]
```

## Responsibilities

- Validate expected response structure
- Validate required fields for completed research
- Validate source metadata when evidence is required
- Validate allowed status values
- Detect unsupported or unsafe output
- Return structured validation failures
- Prevent invalid outputs from being saved as completed artifacts

## Non-Responsibilities

- Investment reasoning
- Task planning
- Agent execution
- Chat rendering
- Artifact persistence
- Research tool access
- User memory writes

## Interfaces

Input:

- structured executor result
- expected output contract
- task constraints

Output:

- accepted output
- validation failure with reason and diagnostics

## Key Policies

- Completed research must include a user-facing brief
- Completed research must include source metadata when sources are required
- Invalid output must not be saved as a completed artifact
- Validator should fail closed when required structure is missing
- Validator should not rewrite substantive recommendations
- User-facing fallback messages should be produced by the orchestrator

## Acceptance Criteria

- Executor output is validated before persistence
- Missing required fields produce structured validation failures
- Unsupported status values are rejected
- Missing source metadata is rejected when evidence is required
- Invalid outputs are not saved as completed artifacts
- Validator does not perform investment reasoning

