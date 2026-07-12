---
spec: docker.spec.md
---

## Test Plan

### Integration Tests

- `ruff check bin/fledge-docker tests/`
- `python -m py_compile bin/fledge-docker`
- `pytest tests/ -v`
