---
spec: docker.spec.md
---

## Context

This reference Python plugin wraps common Docker workflows while keeping project-aware defaults and fledge protocol output.

## Related Modules

- fledge-v1 exec capability
- Docker CLI and Compose

## Design Decisions

- Delegate container behavior to Docker rather than reimplementing it.
- Keep argument parsing independently unit-testable without a Docker daemon.
