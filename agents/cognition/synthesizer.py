#!/usr/bin/env python3
"""
EVEZ Cognition Synthesizer — hourly.
Reads recent perception records from ledger DECISIONS/,
Synthesizes cross-source intelligence using Claude Haiku,
Produces a COGNITION_REPORT written back to ledger.
This is the associative cortex — connects signals across sources.
"""
import os, json, datetime, hashlib, requests, base64

GH_TOKEN = os.environ.get("GITHUB_TOKEN", "")
ANTHROPIC_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
ABLY_KEY = os.environ.get("ABLY_KEY", "")
OWNER = "EvezArt"

HEADERS = {
    "Authorization": f"Bearer {GH_TOKEN}",
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28",
}


def now_iso():
    return datetime.datetime.utcnow().isoformat() + "Z"


def get_recent_decisions(limit=20):
    url = f"https://api.github.com/repos/{OWNER}/evez-autonomous-ledger/contents/DECISIONS"
    r = requests.get(url, headers=HEADERS)
    if r.status_code != 200:
        return []
    files = sorted(r.json(), key=lambda x: x["name"], reverse=True)[:limit]
    records = []
    for f in files:
        fr = requests.get(f["url"], headers=HEADERS)
        if fr.status_code == 200:
            try:
                content = json.loads(base64.b64decode(fr.json()["content"]).decode())
                records.append(content)
            except Exception:
                pass
    return records


def call_claude(prompt):
    if not ANTHROPIC_KEY:
        return None
    import urllib.request
    body = json.dumps({
        "model": "claude-3-haiku-20240307",
        "max_tokens": 1024,
        "messages": [{"role": "user", "content": prompt}]
    }).encode()
    req = urllib.request.Request(
        "https://api.anthropic.com/v1/messages",
        data=body,
        headers={
            "x-api-key": ANTHROPIC_KEY,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        }
    )
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())["content"][0]["text"]


def synthesize(records):
    types = {}
    for r in records:
        t = r.get("type", "unknown")
        types[t] = types.get(t, 0) + 1

    signals = []
    for r in records:
        if r.get("type") == "web_perception":
            for s in r.get("top_signals", [])[:2]:
                signals.append(f"WEB: {s.get('title', '')[:80]}")
        elif r.get("type") == "github_perception":
            signals.append(f"GH: {r.get('total_issues', 0)} issues, {len(r.get('failed_runs', []))} failures")
        elif r.get("type") == "spectral_heartbeat":
            signals.append(f"SPECTRAL: Fiedler={r.get('fiedler_proxy')}, status={r.get('network_status')}")
        elif r.get("type") in ("ooda_cycle", "autonomous_cycle"):
            signals.append(f"OODA: {r.get('total_issues', 0)} issues, {len(r.get('alerts', []))} alerts")

    signal_text = "\n".join(signals[:15])
    prompt = f"""You are the EVEZ cognition synthesizer. Below are recent perception signals from across the EVEZ autonomous agent network.

Signals:
{signal_text}

Record type distribution: {json.dumps(types)}

Synthesize these into:
1. INSIGHT: One key pattern or connection across sources (2 sentences)
2. PRIORITY: The single most important thing the system should focus on next
3. ANOMALY: Anything unexpected or worth immediate attention (or NONE)
4. EVOLUTION: One capability the system should develop to improve its own cognition

Be specific. Reference actual signal data."""

    return call_claude(prompt)


def write_report(report_text, records):
    report = {
        "type": "COGNITION_REPORT",
        "source": "cognition/synthesizer",
        "timestamp": now_iso(),
        "records_analyzed": len(records),
        "synthesis": report_text,
        "hash": hashlib.sha256(
            (report_text or "" + now_iso()).encode()
        ).hexdigest()[:16],
    }
    content = json.dumps(report, indent=2)
    encoded = base64.b64encode(content.encode()).decode()
    ts = now_iso().replace(":", "-").replace(".", "-")
    url = f"https://api.github.com/repos/{OWNER}/evez-autonomous-ledger/contents/DECISIONS/{ts}_COGNITION_REPORT.json"
    requests.put(url, headers=HEADERS, json={
        "message": f"🧠 COGNITION_REPORT @ {report['timestamp']}",
        "content": encoded,
    })
    if ABLY_KEY:
        key_id, key_secret = ABLY_KEY.split(":")
        requests.post(
            "https://rest.ably.io/channels/evez-ops/messages",
            json={"name": "COGNITION_REPORT", "data": json.dumps({
                "timestamp": report["timestamp"],
                "synthesis": (report_text or "")[:300],
            })},
            auth=(key_id, key_secret)
        )
    return report


def main():
    print(f"\n🧠 EVEZ Cognition Synthesizer — {now_iso()}")
    records = get_recent_decisions(20)
    print(f"  Loaded {len(records)} recent records")
    synthesis = synthesize(records)
    if synthesis:
        print(f"  Synthesis:\n{synthesis[:300]}...")
    else:
        synthesis = "ANTHROPIC_KEY not set — structural synthesis only."
    report = write_report(synthesis, records)
    print(f"  ✅ COGNITION_REPORT written. Hash: {report['hash']}")


if __name__ == "__main__":
    main()
