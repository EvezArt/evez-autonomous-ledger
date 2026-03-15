#!/usr/bin/env python3
"""
EVEZ Autonomous Ledger — 24/7 Heartbeat Cycle
Observe → Orient → Decide → Act (OODA)
Writes every decision back to the ledger as a hash-chained record.
"""
import os, json, hashlib, datetime, sys
try:
    import requests
except ImportError:
    print("ERROR: 'requests' module not available. Exiting gracefully.")
    sys.exit(0)

GH_TOKEN = os.environ.get("GITHUB_TOKEN", "")
OWNER = os.environ.get("REPO_OWNER", "EvezArt")
ANTHROPIC_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
ABLY_KEY = os.environ.get("ABLY_KEY", "")

REPOS = [
    "evez-autonomous-ledger",
    "evez-os",
    "evez-agentnet",
    "agentvault",
    "evez-meme-bus",
    "Evez666",
]

HEADERS = {
    "Authorization": f"Bearer {GH_TOKEN}",
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28",
}


def now_iso():
    return datetime.datetime.utcnow().isoformat() + "Z"


def chain_hash(prev_hash: str, payload: dict) -> str:
    raw = prev_hash + json.dumps(payload, sort_keys=True)
    return hashlib.sha256(raw.encode()).hexdigest()


def get_open_issues(repo: str) -> list:
    url = f"https://api.github.com/repos/{OWNER}/{repo}/issues?state=open&per_page=20"
    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
        if r.status_code == 200:
            return [i for i in r.json() if "pull_request" not in i]
    except Exception as e:
        print(f"  ⚠ get_open_issues({repo}) failed: {e}")
    return []


def get_last_ledger_hash() -> str:
    """Read genesis/last hash from spine/genesis.json"""
    url = f"https://api.github.com/repos/{OWNER}/evez-autonomous-ledger/contents/spine/genesis.json"
    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
        if r.status_code == 200:
            import base64
            content = json.loads(base64.b64decode(r.json()["content"]).decode())
            return content.get("genesis_hash", "GENESIS")
    except Exception as e:
        print(f"  ⚠ get_last_ledger_hash failed: {e}")
    return "GENESIS"


def write_ledger_entry(entry: dict, filename: str):
    """Append a new ledger record to DECISIONS/"""
    import base64
    content = json.dumps(entry, indent=2)
    encoded = base64.b64encode(content.encode()).decode()
    url = f"https://api.github.com/repos/{OWNER}/evez-autonomous-ledger/contents/DECISIONS/{filename}"
    payload = {
        "message": f"🔗 ledger: {entry.get('type','event')} @ {entry.get('timestamp','')}",
        "content": encoded,
    }
    try:
        requests.put(url, headers=HEADERS, json=payload, timeout=15)
    except Exception as e:
        print(f"  ⚠ write_ledger_entry({filename}) failed: {e}")


def classify_issue(title: str, body: str) -> str:
    title_lower = title.lower()
    body_lower = (body or "").lower()
    if any(w in title_lower for w in ["bug", "fix", "error", "fail", "broken", "crash"]):
        return "fix"
    if any(w in title_lower for w in ["add", "implement", "feature", "support", "create", "build"]):
        return "build"
    if any(w in title_lower for w in ["refactor", "clean", "improve", "optimize", "update"]):
        return "improve"
    return "investigate"


def observe() -> dict:
    """Collect open issues across all repos."""
    state = {}
    for repo in REPOS:
        issues = get_open_issues(repo)
        state[repo] = [{"number": i["number"], "title": i["title"],
                        "body": (i.get("body") or "")[:300],
                        "class": classify_issue(i["title"], i.get("body") or "")
                        } for i in issues]
    return state


def orient(state: dict) -> list:
    """Score and prioritize work items."""
    work_queue = []
    priority = {"fix": 3, "improve": 2, "build": 1, "investigate": 0}
    for repo, issues in state.items():
        for issue in issues:
            work_queue.append({
                "repo": repo,
                "issue": issue,
                "priority": priority.get(issue["class"], 0),
            })
    work_queue.sort(key=lambda x: x["priority"], reverse=True)
    return work_queue[:5]  # top 5 per cycle


def decide(work_queue: list) -> list:
    """Generate review_queue entries — nothing executes without human gate."""
    plans = []
    for item in work_queue:
        plan = {
            "id": f"plan_{item['repo']}_{item['issue']['number']}",
            "repo": item["repo"],
            "issue_number": item["issue"]["number"],
            "issue_title": item["issue"]["title"],
            "action_class": item["issue"]["class"],
            "status": "PENDING_HUMAN_APPROVAL",
            "timestamp": now_iso(),
            "safe_to_auto": item["issue"]["class"] == "fix" and item["priority"] == 3,
        }
        plans.append(plan)
    return plans


def act(plans: list, prev_hash: str) -> str:
    """Write plans to ledger. Auto-act only on pre-approved fix class."""
    current_hash = prev_hash
    for plan in plans:
        current_hash = chain_hash(current_hash, plan)
        plan["chain_hash"] = current_hash
        ts = now_iso().replace(":", "-").replace(".", "-")
        filename = f"{ts}_{plan['id']}.json"
        write_ledger_entry(plan, filename)
        print(f"  📝 Ledger: {plan['id']} [{plan['action_class']}] hash={current_hash[:12]}")
    return current_hash


def publish_heartbeat(plans: list):
    """Publish cycle summary to Ably evez-ops channel."""
    if not ABLY_KEY:
        return
    try:
        key_id, key_secret = ABLY_KEY.split(":")
    except ValueError:
        print("  ⚠ ABLY_KEY format invalid (expected 'id:secret'), skipping heartbeat")
        return
    channel = "evez-ops"
    url = f"https://rest.ably.io/channels/{channel}/messages"
    payload = {
        "name": "autonomous_cycle",
        "data": json.dumps({
            "source": "evez-autonomous-ledger",
            "timestamp": now_iso(),
            "plans_count": len(plans),
            "plans": [{"id": p["id"], "class": p["action_class"],
                        "repo": p["repo"]} for p in plans],
        })
    }
    try:
        requests.post(url, json=payload, auth=(key_id, key_secret), timeout=15)
        print(f"  📡 Ably broadcast: {len(plans)} plans → evez-ops")
    except Exception as e:
        print(f"  ⚠ publish_heartbeat failed: {e}")


def main():
    print(f"\n🧠 EVEZ Autonomous Cycle — {now_iso()}")

    if not GH_TOKEN:
        print("  ⚠ GITHUB_TOKEN not set — running in degraded mode (API calls will likely fail)")

    try:
        print("  Phase 1: OBSERVE")
        state = observe()
        total = sum(len(v) for v in state.values())
        print(f"  → {total} open issues across {len(REPOS)} repos")

        print("  Phase 2: ORIENT")
        work_queue = orient(state)
        print(f"  → {len(work_queue)} items prioritized")

        print("  Phase 3: DECIDE")
        plans = decide(work_queue)
        print(f"  → {len(plans)} plans generated")

        print("  Phase 4: ACT (ledger + gate)")
        prev_hash = get_last_ledger_hash()
        final_hash = act(plans, prev_hash)
        print(f"  → Chain tip: {final_hash[:16]}")

        publish_heartbeat(plans)
        print("  ✅ Cycle complete.\n")
    except Exception as e:
        print(f"  ❌ Cycle failed: {e}")
        print("  ⚠ Exiting gracefully — will retry next scheduled run.\n")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"FATAL (caught at top level): {e}")
        sys.exit(0)
