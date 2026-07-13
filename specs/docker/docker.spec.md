---
module: docker
version: 1
status: active
files:
  - bin/fledge-docker

db_tables: []
depends_on: []
---

# Docker

## Purpose

Translate fledge project metadata and CLI options into Docker build, push, Compose up/down/logs commands, execute them through the fledge-v1 exec capability, and optionally emit a stable JSON result envelope.

## Public API

| Action | Behavior |
|--------|----------|
| build | Build an image using project/default tag, version, Dockerfile, and context. |
| push | Prefix the image with a required registry and push it. |
| up | Start Docker Compose detached unless foreground is requested. |
| down | Stop the Docker Compose project. |
| logs | Follow recent Docker Compose logs. |
| JSON | Emit schema-versioned action, command, image, exit, and status fields. |

## Invariants

1. Every Docker or Compose operation requires the fledge exec capability.
2. The image tag defaults to the fledge project name and version defaults to latest.
3. Push requires a registry and constructs the same image identity used by build.
4. Compose up is detached by default and attached only when foreground is explicit.
5. JSON output reports the actual command exit code and success status.
6. User-controlled command arguments are represented as discrete argv values rather than evaluated shell fragments.

## Behavioral Examples

```
Given project `myapp`, version `v1.2.3`, and Dockerfile `Dockerfile.prod`
When build is requested
Then the plugin executes Docker build for image `myapp:v1.2.3` using that Dockerfile and the project context
```

## Error Cases

| Error | When | Behavior |
|-------|------|----------|
| Missing exec capability | Any action is requested | Report denial and exit 126. |
| Missing registry | Push has no registry | Report required option and exit non-zero. |
| Unknown action or option | CLI input is unsupported | Print usage/error and exit non-zero. |
| Docker failure | Native command returns non-zero | Propagate the exit status and mark JSON status false. |
| Missing Docker/Compose | Required executable is unavailable | Surface native execution failure. |

## Dependencies

- Python 3.10 or later
- fledge-v1 exec capability
- Docker CLI and Docker Compose plugin

## Change Log

| Version | Date | Changes |
|---------|------|---------|
| 1 | 2026-07-12 | Document existing Docker and Compose wrapper behavior for SpecSync 5 adoption. |
