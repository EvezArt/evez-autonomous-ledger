# EVEZ n8n Workflow Suite — v3 FREE STACK

All 7 workflows. Zero cost. 24/7 autonomous intelligence.

## Stack
| WF | Name | Interval | Provider | Purpose |
|----|------|----------|----------|---------|
| WF1 | Groq Engine | 10 min | groq/llama-3.3-70b | DeFi + agentic research |
| WF2 | Gemini Analyst | 15 min | gemini-2.0-flash | Analysis + DeFi simulation |
| WF3 | OpenRouter Agent | 30 min | llama:free, deepseek-r1:free | Strategic rotation |
| WF4 | Pure-Code Spine | 5 min | none ($0.00) | Heartbeat + env audit |
| WF5 | Multi-Model Rotator | 20 min | groq+gemini+OR cascade | Redundant intelligence |
| WF6 | Cipher Synthesis | 60 min | groq/gemini | Trunk compression + FIRE events |
| WF7 | Unified Router | on-demand | groq/gemini | Single /evez entry point |

## Daily Budget
- Groq: ~528 calls/day — 3.7% of 14,400/day free limit
- Gemini: ~168 calls/day — 11.2% of 1,500/day free limit
- OpenRouter: unlimited :free models
- **Total cost: $0.00**

## Shared Architecture
All workflows share:
- `H(d)` — deterministic hash function
- `log(type, payload)` → `evez-ledger` webhook (append-only spine)
- PID 335 — Guardian Charter anchor
- JSON-only AI responses (parseable, falsifiable)

## Setup
1. Import all 7 JSON files into n8n
2. Add env vars in n8n Settings → Environment Variables:
   - `GROQ_API_KEY` — free: console.groq.com
   - `GEMINI_API_KEY` — free: aistudio.google.com
   - `OPENROUTER_API_KEY` — free: openrouter.ai
3. Activate all workflows
4. WF7 exposes: `POST /webhook/evez` with `{"action": "status|fire|defi|chat|spine"}`

## WF6 Webhook Endpoints
- `POST /webhook/evez-fire-event` — record a FIRE event (tau, omega, N, topo, falsifier)
- `POST /webhook/evez-synthesis-status` — get current phi + system status

## WF7 Unified Router (single entry point)
```
POST /webhook/evez
{"action": "status"}
{"action": "fire", "title": "...", "tau": 7, "omega": 0.99, "N": 5, "topo": "2.1", "falsifier": "..."}
{"action": "defi", "seed": 100, "ltv": 0.65, "depth": 5, "apy": 0.28}
{"action": "chat", "message": "What should I do today?"}
{"action": "spine"}
```

## FIRE Event Formula
```
poly_c = tau * omega * topo / (2 * sqrt(N))
status = poly_c >= 0.9 ? "CANONICAL" : "PENDING"
```

---
*append-only | no edits | ever | witnessed: XyferViperZephyr*
