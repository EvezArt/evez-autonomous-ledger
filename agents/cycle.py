#!/usr/bin/env python3
"""
CIPHER CYCLE v3 — Master Launcher
Imports and runs all CIPHER sub-engines in sequence.
Called by unified_daily.yml at 08:00 UTC daily.
Manually dispatchable any time.
NO STOP. NO DELAY. ALL SYSTEMS FIRING.
"""
import os, sys, subprocess, datetime

def ts(): return datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")

ENGINES = [
    ("TRUNK",    "agents/cipher_trunk.py"),
    ("MANIFOLD", "agents/cipher_manifold.py"),
    ("FIX",      "agents/cipher_fix.py"),
    ("BUILD",    "agents/cipher_build.py"),
]

print(f"\n{'='*65}")
print(f"CIPHER CYCLE v3 — {ts()}")
print(f"NO STOP. NO DELAY. ALL SYSTEMS FIRING.")
print(f"{'='*65}\n")

results = {}
for name, script in ENGINES:
    if not os.path.exists(script):
        print(f"[{name:10s}] SKIP — {script} not found")
        continue
    print(f"\n[{name:10s}] LAUNCHING {script}...")
    try:
        r = subprocess.run(
            [sys.executable, script],
            capture_output=False,
            timeout=300,
            env={**os.environ}
        )
        results[name] = "OK" if r.returncode == 0 else f"EXIT_{r.returncode}"
        print(f"[{name:10s}] {'✓ DONE' if r.returncode==0 else f'⚠ EXIT {r.returncode}'}")
    except subprocess.TimeoutExpired:
        results[name] = "TIMEOUT"
        print(f"[{name:10s}] ⚠ TIMEOUT (300s)")
    except Exception as e:
        results[name] = f"ERROR: {e}"
        print(f"[{name:10s}] ✗ ERROR: {e}")

print(f"\n{'='*65}")
print("CYCLE SUMMARY:")
for name, status in results.items():
    print(f"  {name:10s}: {status}")
print(f"\npoly_c=τ×ω×topo/2√N | append-only | no edits | ever")
print("witnessed: XyferViperZephyr | cipher runs in us-phoenix-1")
print(f"{'='*65}")
