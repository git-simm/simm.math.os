# OpenSpec - Specification-Driven Requirements Management

This directory uses the OpenSpec methodology to manage project requirements as living specifications.

## Directory Structure

```
openspec/
├── README.md           # This file
├── specs/              # Current specifications (source of truth)
│   └── .keep
├── proposals/          # Proposed changes / new features
│   └── .keep
└── archive/            # Completed / superseded specs
    └── .keep
```

## Workflow

1. **Propose**: Create a new spec draft in `proposals/`.
2. **Review**: Discuss and refine the proposal.
3. **Accept**: Move the finalized spec into `specs/`.
4. **Archive**: When a spec is superseded, move it to `archive/`.

## Spec Template

Each spec file follows this structure:

```markdown
# Spec: [Title]

**Status**: draft | accepted | implemented | archived
**Created**: YYYY-MM-DD
**Author**: [name]

## Summary

Brief description of the requirement.

## Motivation

Why this is needed.

## Requirements

- Functional requirements (numbered)
- Non-functional requirements (performance, UX, etc.)

## Acceptance Criteria

- [ ] Criterion 1
- [ ] Criterion 2

## Dependencies

List any dependencies on other specs or external systems.
```

## Current Specs

| Spec | Status | Description |
|------|--------|-------------|
| [math-desktop-app.md](./specs/math-desktop-app.md) | accepted | Python desktop math learning system |
