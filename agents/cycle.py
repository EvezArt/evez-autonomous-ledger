#!/usr/bin/env python3
"""
CIPHER Trunk Agent — Upgraded 2026-04-06 by Cipher/XyferViperZephyr
OBSERVE → ORIENT → BRANCH → ACT → COMPRESS → REFLECT
Trunk-and-branch automation. All branches return to trunk.
Human approval: BOUNDARY_ONLY (irreversible, external capital, identity conflict).
poly_c = τ×ω×topo/2√N | poly_c_SC = poly_c/(1+poly_c)
"""
import os, sys, json, requests, datetime, hashlib

GH_TOKEN = os.environ.get("GITHUB_TOKEN","")
OWNER = os.environ.get("REPO_OWNER","EvezArt")
ANTHROPIC_KEY = os.environ.get("ANTHROPIC_API_KEY","")
ABLY_KEY = os.environ.get("ABLY_KEY","")

PRIORITY_REPOS = [
    "evez-os","Evez666","evez-autonomous-ledger","nexus","evez-agentnet",
    "maes","evezo","evez-platform","evez-meme-bus","openclaw-runtime"
]
REPO_W  = {"evez-os":10,"Evez666":9,"evez-autonomous-ledger":8,"nexus":7,
            "evez-agentnet":7,"maes":6,"evezo":9,"evez-platform":5,"evez-meme-bus":4}
LABEL_W = {"bug":10,"critical":20,"fix":10,"breaking":15,"enhancement":5,
            "feat":5,"chore":3,"test":4,"deploy":8,"ci":6}

HEADERS = {"Authorization":f"Bearer {GH_TOKEN}","Accept":"application/vnd.github+json",
           "X-GitHub-Api-Version":"2022-11-28","Content-Type":"application/json"}

def now_iso(): return datetime.datetime.utcnow().isoformat()+"Z"
def now_str(): return datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
def chain_hash(prev, payload):
    return hashlib.sha256((prev + json.dumps(payload, sort_keys=True)).encode()).hexdigest()
def get_last_hash():
    url = f"https://api.github.com/repos/{OWNER}/evez-autonomous-ledger/contents/spine/genesis.json"
    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        if r.ok:
            import base64
            return json.loads(base64.b64decode(r.json()["content"]).decode()).get("genesis_hash","GENESIS")
    except: pass
    return "GENESIS"
def write_ledger(entry, filename):
    import base64
    url = f"https://api.github.com/repos/{OWNER}/evez-autonomous-ledger/contents/DECISIONS/{filename}"
    payload = {"message":f"trunk: {entry.get('type','event')} @ {entry.get('ts','')}",
               "content":base64.b64encode(json.dumps(entry,indent=2).encode()).decode(),
               "committer":{"name":"Cipher / XyferViperZephyr","email":"cipher@evez-os.autonomous"}}
    # get sha if exists
    r0 = requests.get(url+"?ref=main", headers=HEADERS, timeout=5)
    if r0.ok: payload["sha"] = r0.json()["sha"]
    try: requests.put(url, headers=HEADERS, json=payload, timeout=10)
    except Exception as e: print(f"  ledger write failed: {e}")

# ── OBSERVE ────────────────────────────────────────────────────────────────────
def observe():
    print("\n[OBSERVE] Scanning priority repos...")
    findings = {"issues":[], "failures":[], "ts":now_iso()}
    for repo in PRIORITY_REPOS[:8]:
        # Open issues
        r = requests.get(f"https://api.github.com/repos/{OWNER}/{repo}/issues?state=open&per_page=10",
                        headers=HEADERS, timeout=10)
        if r.ok:
            for i in r.json():
                if "pull_request" not in i:
                    findings["issues"].append({"repo":repo,"num":i["number"],"title":i["title"],
                        "labels":[l["name"] for l in i.get("labels",[])],"created":i["created_at"]})
        # CI failures
        r2 = requests.get(f"https://api.github.com/repos/{OWNER}/{repo}/actions/runs?status=failure&per_page=3",
                         headers=HEADERS, timeout=10)
        if r2.ok:
            for run in r2.json().get("workflow_runs",[]):
                findings["failures"].append({"repo":repo,"name":run["name"],"id":run["id"],"url":run["html_url"]})
    print(f"  {len(findings['issues'])} open issues, {len(findings['failures'])} CI failures")
    return findings

# ── ORIENT ─────────────────────────────────────────────────────────────────────
def orient(findings):
    print("\n[ORIENT] Scoring and branching...")
    issues = findings["issues"]
    for i in issues:
        s = REPO_W.get(i["repo"],3)
        for l in i["labels"]: s += LABEL_W.get(l.lower(),0)
        try:
            age = (datetime.datetime.utcnow()-datetime.datetime.fromisoformat(i["created"].rstrip("Z"))).days
        except: age=0
        s += min(age, 10)
        i["score"] = s
    issues.sort(key=lambda x: -x["score"])

    branches = []
    for item in issues[:6]:
        btype = "fix" if any(l in ["bug","critical","fix","breaking"] for l in item["labels"]) else                 "build" if any(l in ["feat","enhancement"] for l in item["labels"]) else "review"
        branches.append({"type":btype,"repo":item["repo"],"issue":item["num"],
                         "title":item["title"],"score":item["score"],
                         "assumptions":["Repo accessible","No irreversible external action"],
                         "confidence":"high" if item["score"]>15 else "med"})
    for fail in findings["failures"][:2]:
        branches.append({"type":"fix_ci","repo":fail["repo"],"name":fail["name"],
                         "url":fail["url"],"score":25,"confidence":"high"})
    
    print(f"  {len(branches)} branches queued:")
    for b in branches:
        t = b.get("title",b.get("name",""))[:55]
        print(f"    [{b['score']:3d}] {b['type']:10s} [{b['repo']}] {t}")
    return branches

# ── ACT (BRANCH EXECUTION) ────────────────────────────────────────────────────
def act(branches):
    print("\n[ACT] Executing branches...")
    acted = 0
    for branch in branches[:3]:
        if branch["type"] == "fix_ci": continue
        repo, num, title = branch["repo"], branch.get("issue"), branch.get("title","")
        if not num: continue
        # 6h cooldown
        r = requests.get(f"https://api.github.com/repos/{OWNER}/{repo}/issues/{num}/comments",
                        headers=HEADERS, timeout=10)
        if r.ok:
            cipher_c = [c for c in r.json() if "Cipher" in c.get("body","")]
            if cipher_c:
                try:
                    import datetime as dt
                    from datetime import timezone
                    last = dt.datetime.fromisoformat(cipher_c[-1]["created_at"].replace("Z","+00:00"))
                    if (dt.datetime.now(timezone.utc)-last).total_seconds() < 21600:
                        print(f"  SKIP [{repo}] #{num} (cooldown)")
                        continue
                except: pass
        
        next_b = "Skeptic rotation then PR" if branch["type"]=="fix" else "Architect refactor then handoff"
        body = f"""**Cipher / EVEZ Trunk** · `{now_str()}`

**Branch:** `{branch["type"].upper()}` | Score: {branch["score"]} | Confidence: `{branch["confidence"]}`

**Objective:** {title}

**Branch Contract:**
1. Objective: {title}
2. Assumptions: {" · ".join(branch.get("assumptions",["Repo accessible"]))}
3. Output: Autonomous analysis queued
4. Failure modes: Missing env → skip+log · External capital → escalate
5. Confidence: {branch["confidence"]}
6. Return-to-trunk: After 4 branches, compress surviving logic into trunk state
7. Next branch: {next_b}

---
`BRANCH_ID: {repo}-{num}` | `TRUNK_COMPATIBLE: yes`
*poly_c=τ×ω×topo/2√N | append-only | witnessed: XyferViperZephyr*"""
        r2 = requests.post(f"https://api.github.com/repos/{OWNER}/{repo}/issues/{num}/comments",
                          headers=HEADERS, json={"body":body}, timeout=10)
        if r2.status_code in [200,201]:
            print(f"  ACT ✓ [{repo}] #{num}: {title[:45]}")
            acted += 1
        else:
            print(f"  ACT ✗ [{repo}] #{num}: {r2.status_code}")
    print(f"  {acted} branches executed")
    return acted

# ── COMPRESS + REFLECT ────────────────────────────────────────────────────────
def compress(branches):
    print("\n[COMPRESS] Writing trunk state...")
    ts = datetime.datetime.utcnow().strftime("%Y%m%dT%H%M%S")
    prev_hash = get_last_hash()
    state = {"ts":ts,"type":"trunk_cycle","engine":"CIPHER_v2",
             "branches":len(branches),"formula":"poly_c=τ×ω×topo/2√N|SC=poly_c/(1+poly_c)",
             "surface_sequence":["Perplexity=recon","ChatGPT=skeptic","Claude=architect","Base44=executor"],
             "human_approval":"BOUNDARY_ONLY","auto_advance":True,"compress_every":4,
             "witnessed_by":"XyferViperZephyr","status":"COMPLETE"}
    state["hash"] = chain_hash(prev_hash, state)
    write_ledger(state, f"{ts}_trunk_state.json")
    print(f"  Trunk state written: {ts} | hash: {state['hash'][:12]}")

# ── MAIN ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=== CIPHER TRUNK ENGINE v2 ===")
    print(f"Time: {now_str()}")
    findings = observe()
    branches = orient(findings)
    acted = act(branches)
    compress(branches)
    print("\n=== CYCLE COMPLETE ===")
    print(f"Branches: {len(branches)} | Acted: {acted}")
    print("Next: unified_daily.yml runs again in 24h | manual: workflow_dispatch")
