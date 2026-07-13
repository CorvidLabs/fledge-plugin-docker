---
spec: docker.spec.md
---

## User Stories

- As a developer, I want consistent Docker build, push, and Compose commands wired to my fledge project.
- As an automation author, I want structured action results without scraping Docker output.

## Acceptance Criteria

### REQ-docker-001

The plugin SHALL support Docker build and registry push with project, tag, version, file, and context options.

### REQ-docker-002

The plugin SHALL support Compose up, down, and followed logs, with detached up as the default.

### REQ-docker-003

Every native operation SHALL execute through the granted fledge exec capability and propagate its exit code.

### REQ-docker-004

JSON mode SHALL report schema version, action, command, image when applicable, exit code, and success status.

## Constraints

- Requires Python, Docker, Docker Compose, and fledge exec capability.

## Out of Scope

- Buildx, registry authentication, multi-architecture orchestration, and cloud deployment.
