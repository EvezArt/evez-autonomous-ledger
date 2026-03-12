# Decision: evez-os Vercel Build Fix
**Date:** 2026-03-12T02:37Z  
**Task:** Fix evez-os Vercel build ERROR — react-scripts exit 127

## Root Cause Analysis

Vercel deployment for `evez-os` was failing with two cascading errors:
1. `Command "react-scripts build" exited with 127` (earlier deploys)
2. `Command "npm install --legacy-peer-deps" exited with 254` (latest deploy on branch fix/phase-a-canonicalize)

**Why:** No `package.json` exists at repo root. Vercel auto-detected the project as a React app (possibly from a previous config or framework detection) and tried to run npm install + react-scripts build.

**Actual repo structure:**
- `dashboard/index.html` — pure static HTML
- `dashboard/obs.html` — pure static HTML  
- `dashboard/terminal.html` — pure static HTML (42kb)
- No Node.js, no React, no build step needed whatsoever

## Fix Applied

Committed `vercel.json` to repo root on `main` branch:
```json
{
  "version": 2,
  "builds": [{"src": "dashboard/**", "use": "@vercel/static"}],
  "routes": [{"src": "/(.*)", "dest": "/dashboard/$1"}]
}
```

This tells Vercel: static site, serve from dashboard/, no build command.

## Expected Outcome
Next Vercel deployment triggered by this commit should reach READY state.
URL: https://evez-os.vercel.app (or the current alias)

## Lesson
Always commit vercel.json for repos that have Vercel projects. Never let Vercel auto-detect framework on a static HTML repo.
