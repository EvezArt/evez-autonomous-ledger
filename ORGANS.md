# EVEZ Organ Topology

## Repo roles

- `evez`: constitutional root, schemas, invariants, parity
- `evez-os`: Python execution/runtime organ
- `evez-agentnet`: service and automation organ
- `evez-autonomous-ledger`: state and audit organ
- `evez-operator` / `openclaw-phone-pwa`: web presentation organ

## Deployment rule

Deploy each repo according to its native runtime role.

## Current mismatch

`evez-os` is a Python-oriented runtime repo and should not be treated by default as a Create React App web shell.

## Correction

- Keep web shells on Vercel-facing frontend repos
- Keep Python/package repos package-first unless a dedicated web wrapper exists
- Keep the ledger as the source of cross-repo state

## Next actions

1. Reclassify `evez-os` as execution organ
2. Use a dedicated web shell repo for the main frontend surface
3. Keep repo-role mappings recorded here in the ledger
