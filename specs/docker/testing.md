---
spec: docker.spec.md
---

## Test Plan

### Integration Tests

- `ruff check bin/fledge-docker tests/`
- `python3 -m py_compile bin/fledge-docker`
- `pytest tests/ -v`
