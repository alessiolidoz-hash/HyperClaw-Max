## Summary

Describe the change in a few lines.

## Scope

- [ ] public core
- [ ] optional adapter
- [ ] docs only
- [ ] tests only

## Validation

- [ ] `python3 -m unittest discover -s tests -q`
- [ ] `PYTHONPATH=src python3 -m hyperclaw_max.doctor --repo .`
- [ ] `PYTHONPATH=src python3 -m hyperclaw_max.privacy_check --repo .`
- [ ] `PYTHONPATH=src python3 -m hyperclaw_max.runtime_validate config/openclaw.public.example.jsonc`

## Boundary Check

- [ ] no secrets
- [ ] no private runtime state
- [ ] no private-only routing doctrine
- [ ] no host-specific paths required for the feature

## Notes

Anything reviewers should pay attention to.
