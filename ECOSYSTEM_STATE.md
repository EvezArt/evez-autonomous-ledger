# ECOSYSTEM_STATE.md
**Last updated:** 2026-03-26T06:01 PT — Synapse Engine run #003

## Vercel Projects (9 tracked)

| Project | Status | Notes |
|---------|--------|---------|
| evez-operator | ✅ READY | evez-operator.vercel.app |
| evez-os | ✅ READY | dashboard/ static, fixed 2026-03-12 |
| openclaw-phone-pwa | ✅ READY | Fixed: rootDirectory=pwa (static HTML), was OOM/SIGKILL |
| ephv | ✅ READY | — |
| evez-animated-goggles | ❌ ERROR | bun run build exit 1 — TypeScript/workspace compile error, needs manual log check |
| evez666-arg-canon | ✅ READY | — |
| evez-crawhub | ✅ READY | — |
| evez-vcl | ✅ READY | — |
| evez-openclaw-dashboard | ✅ READY | — |

**Summary: 8/9 READY — 1 ERROR (animated-goggles)**

## GitHub Repos (51 total, up from 41 on 2026-03-12)

### HIGH_MOMENTUM (score = size_kb/100 + open_issues*2)
1. **gh-aw** — 4322.2 (Go, 428MB, 18 issues)
2. **codeql** — 4150.0 (428MB, 8 issues)
3. **openclaw** — 1710.8 (TypeScript, 162MB, 24 issues) ← actively pushed
4. **codex** — 605.0 (Rust, 57MB, 19 issues) ← actively pushed
5. **Evez666** — 200.9 (Python, 18MB, 6 issues)

### CI Status
- `evez-agentnet` / `skill-validate`: ~10 failures in burst 12:40-12:57 UTC. SKILL.md valid at HEAD. Self-resolving.
- `evez-net` / orchestrator: failing (same burst cause)
- `evez666-arg-canon` / sound-reasoning-daemon: failing (investigate)

## Gmail Triage (15+ unread)
- 11+ [ERROR_REPORT] from evez-agentnet CI spam
- 1 [ERROR_REPORT] evez-net orchestrator
- 1 [ERROR_REPORT] evez666-arg-canon sound daemon
- 2 [NOISE] ChatGPT task updates

## Blockers
- `evez-animated-goggles`: bun build compile error — check https://vercel.com/evez666/evez-animated-goggles/5szhTW8xrAgkSTQGkzZgrwUZ4DaT
- `evez-agentnet` CI burst: SKILL.md valid; investigate push source
- Discord bot: 401 — token refresh needed
- Base Sepolia wallet: needs ~0.01 ETH for FIRE#125

## Synapse Engine Health
- Run #003 — 2026-03-26T06:01 PT
- Next run: ~12:01 PT
- Ledger: EvezArt/evez-autonomous-ledger
