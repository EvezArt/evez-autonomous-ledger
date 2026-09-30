# EVEZ Evidence Maturity Framework

Every capability claim must carry one status label:

- **CLAIMED** — documented aspiration; no verified implementation required.
- **DESIGNED** — architecture or code exists; behavior is not yet proven.
- **TESTED** — automated tests pass for specified cases; include command, count, and coverage.
- **DEPLOYED** — running in a named environment with health evidence and rollback.
- **VALIDATED** — independent reproduction or review supports the narrowly defined claim.

## Rules

1. Claims must state their scope, evidence links, date, and limitations.
2. Consciousness, sentience, emergence, and self-awareness are experimental hypotheses; no metric alone proves them.
3. A passing self-test is not independent validation.
4. “Immutable” means tamper-evident and append-only by policy; cryptographic hashes do not prevent filesystem deletion or rewrite without external anchoring.
5. Quantum-related components must be labeled **probabilistic classical**, **quantum-inspired**, **simulator**, or **hardware-backed quantum** according to verified implementation.
6. Financial, credential, deployment, external-message, and destructive actions require explicit human approval.

## Required record

```yaml
name: capability-name
status: CLAIMED
scope: one narrowly defined behavior
code:
  - path/to/file.py
 tests:
  command: pytest tests/test_capability.py
  result: pending
external_validation: none
limitations:
  - self-reported metrics are not independent evidence
last_reviewed: YYYY-MM-DD
```

## Evidence handling

Preserve source files, commit IDs, hashes, timestamps, test fixtures, environment details, and reviewer identities. Never expose secrets in reports. Preserve raw evidence read-only and record transformations in the ledger.
