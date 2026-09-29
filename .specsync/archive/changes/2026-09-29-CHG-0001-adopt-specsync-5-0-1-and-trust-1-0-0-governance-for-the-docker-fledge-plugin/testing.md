---
change: CHG-0001-adopt-specsync-5-0-1-and-trust-1-0-0-governance-for-the-docker-fledge-plugin
artifact: testing
---

# Testing

- `ruff check bin/fledge-docker tests/`
- `python3 -m py_compile bin/fledge-docker`
- `pytest tests/ -v` (22 tests)
- `specsync check --strict --force` at advisory threshold 0
- `specsync agents status`
- `fledge trust doctor` and `fledge trust verify`
