#!/usr/bin/env python3
"""Refresh the combined coding-stats card (assets/codolio.svg).

Reads data/codolio.json. For every platform that has a handle filled in, it fetches live numbers
and merges them over the saved ones. A platform that cannot be reached keeps its saved numbers,
and the card is always written, so it never breaks.

Sources
    LeetCode     public GraphQL endpoint (solved count, contests attended, activity calendar)
    Codeforces   official public API (solved, contests, submission days)
    CodeChef     no official API, so this reads the public profile page (best effort, solved count only)

Usage
    python scripts/generate_codolio.py
Standard library only. Set handles in data/codolio.json.
"""
from __future__ import annotations

import datetime as dt
import json
import re
import time
import urllib.request
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "codolio.json"
CARD = ROOT / "assets" / "codolio.svg"
IMPACT = ROOT / "assets" / "impact.svg"

TEMPLATE = """<svg xmlns="http://www.w3.org/2000/svg" width="640" height="270" viewBox="0 0 640 270" role="img" aria-labelledby="t">
  <title id="t">@@TITLE@@</title>
  <style>
    .sans { font-family: -apple-system, "Segoe UI", Helvetica, Arial, sans-serif; }
    .mono { font-family: "JetBrains Mono", "SFMono-Regular", Consolas, "Liberation Mono", monospace; }
    .ring { stroke-dasharray: 0 302; animation: fill 1.6s .3s cubic-bezier(.3,.7,.2,1) forwards; }
    @keyframes fill { to { stroke-dasharray: 302 302; } }
    .row { animation: in .7s ease both; }
    @keyframes in { from { opacity: 0; transform: translateX(10px); } to { opacity: 1; transform: none; } }
    @media (prefers-reduced-motion: reduce) { .ring { animation: none; stroke-dasharray: 302 302; } .row { animation: none; } }
  </style>
  <defs>
    <linearGradient id="card" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#151A33" /><stop offset="1" stop-color="#0F1220" />
    </linearGradient>
    <linearGradient id="arc" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#8B5CF6" /><stop offset="1" stop-color="#22D3EE" />
    </linearGradient>
  </defs>
  <rect x="1" y="1" width="638" height="268" rx="18" fill="url(#card)" stroke="#2A2F4A" stroke-width="2" />

  <rect x="28" y="24" width="32" height="32" rx="8" fill="#8B5CF6" />
  <path d="m39 34-6 6 6 6M49 34l6 6-6 6" fill="none" stroke="#FFFFFF" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" />
  <text x="72" y="46" class="sans" font-size="20" font-weight="700" fill="#F3F4F6">Aaditya Mittal</text>
  <text x="612" y="46" class="mono" font-size="12" fill="#9CA3AF" text-anchor="end">all platforms, combined</text>
  <path d="M28 72H612" stroke="#2A2F4A" stroke-width="2" />

  <circle cx="112" cy="156" r="48" fill="none" stroke="#232A45" stroke-width="10" />
  <circle class="ring" cx="112" cy="156" r="48" fill="none" stroke="url(#arc)" stroke-width="10" stroke-linecap="round" transform="rotate(-90 112 156)" />
  <text x="112" y="158" class="sans" font-size="30" font-weight="800" fill="#F3F4F6" text-anchor="middle">@@STREAK@@</text>
  <text x="112" y="176" class="sans" font-size="12" fill="#9CA3AF" text-anchor="middle">days</text>
  <text x="112" y="234" class="mono" font-size="12" fill="#A78BFA" text-anchor="middle">LONGEST STREAK</text>

  <g class="row" style="animation-delay:.2s">
    <text x="236" y="118" class="sans" font-size="16" font-weight="600" fill="#D1D5DB">Problems solved</text>
    <text x="604" y="118" class="sans" font-size="22" font-weight="800" fill="#F3F4F6" text-anchor="end">@@SOLVED@@</text>
    <path d="M236 132H604" stroke="#232A45" stroke-width="1.5" />
  </g>
  <g class="row" style="animation-delay:.35s">
    <text x="236" y="166" class="sans" font-size="16" font-weight="600" fill="#D1D5DB">Contests played</text>
    <text x="604" y="166" class="sans" font-size="22" font-weight="800" fill="#F3F4F6" text-anchor="end">@@CONTESTS@@</text>
    <path d="M236 180H604" stroke="#232A45" stroke-width="1.5" />
  </g>
  <g class="row" style="animation-delay:.5s">
    <text x="236" y="214" class="sans" font-size="16" font-weight="600" fill="#D1D5DB">Streak badges</text>
    <text x="604" y="214" class="sans" font-size="18" font-weight="800" fill="#F3F4F6" text-anchor="end">@@BADGES@@</text>
  </g>

  <text x="612" y="254" class="mono" font-size="11" fill="#6B7280" text-anchor="end">@@FOOTER@@</text>
</svg>
"""


def http(url: str, body: bytes | None = None, headers: dict | None = None) -> str:
    req = urllib.request.Request(
        url,
        data=body,
        headers={"User-Agent": "Mozilla/5.0 (profile card refresh)", **(headers or {})},
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read().decode("utf-8", "replace")


def day_of(ts: int) -> dt.date:
    return dt.datetime.fromtimestamp(int(ts), dt.timezone.utc).date()


def leetcode(handle: str) -> dict:
    query = (
        "query($u:String!){matchedUser(username:$u){"
        "submitStatsGlobal{acSubmissionNum{difficulty count}} userCalendar{submissionCalendar}}"
        " userContestRanking(username:$u){attendedContestsCount}}"
    )
    raw = http(
        "https://leetcode.com/graphql",
        json.dumps({"query": query, "variables": {"u": handle}}).encode(),
        {"Content-Type": "application/json", "Referer": "https://leetcode.com"},
    )
    data = json.loads(raw)["data"]
    user = data.get("matchedUser")
    if not user:
        raise ValueError("handle not found")
    solved = next(x["count"] for x in user["submitStatsGlobal"]["acSubmissionNum"] if x["difficulty"] == "All")
    ranking = data.get("userContestRanking") or {}
    calendar = json.loads((user.get("userCalendar") or {}).get("submissionCalendar") or "{}")
    return {
        "solved": solved,
        "contests": ranking.get("attendedContestsCount"),
        "days": {day_of(ts) for ts, n in calendar.items() if n},
    }


def codeforces(handle: str) -> dict:
    status = json.loads(http(f"https://codeforces.com/api/user.status?handle={handle}"))
    if status.get("status") != "OK":
        raise ValueError(status.get("comment", "api error"))
    subs = status["result"]
    solved = {(s["problem"].get("contestId"), s["problem"]["index"]) for s in subs if s.get("verdict") == "OK"}
    time.sleep(2)  # the official API asks for at most one call every two seconds
    rating = json.loads(http(f"https://codeforces.com/api/user.rating?handle={handle}"))
    contests = len(rating["result"]) if rating.get("status") == "OK" else None
    return {"solved": len(solved), "contests": contests, "days": {day_of(s["creationTimeSeconds"]) for s in subs}}


def codechef(handle: str) -> dict:
    html = http(f"https://www.codechef.com/users/{handle}")
    match = re.search(r"Total Problems Solved:\s*(\d+)", html)
    if not match:
        raise ValueError("solved count not found on the profile page")
    return {"solved": int(match.group(1)), "contests": None, "days": set()}


def longest_run(days: set[dt.date]) -> int:
    best = run = 0
    prev = None
    for d in sorted(days):
        run = run + 1 if prev and (d - prev).days == 1 else 1
        best = max(best, run)
        prev = d
    return best


def render(cfg: dict, live: list[str], today: str) -> str:
    solved = sum(cfg[p]["solved"] for p in ("leetcode", "codechef", "codeforces"))
    contests = sum(cfg[p]["contests"] for p in ("leetcode", "codechef", "codeforces"))
    footer = f"live from {', '.join(live)}, updated {today}" if live else f"saved numbers, as of {cfg['as_of']}"
    title = f"Combined coding stats: {solved} problems solved, {contests} contests played, longest streak {cfg['longest_streak']} days"
    values = {
        "@@TITLE@@": title, "@@STREAK@@": cfg["longest_streak"], "@@SOLVED@@": solved,
        "@@CONTESTS@@": contests, "@@BADGES@@": cfg["badges"], "@@FOOTER@@": footer,
    }
    svg = TEMPLATE
    for token, value in values.items():
        svg = svg.replace(token, escape(str(value)))
    return svg


def patch_impact(solved: int) -> None:
    """Keep the fifth card of the top strip in step with the combined total, shown as N+."""
    if not IMPACT.exists():
        return
    svg = IMPACT.read_text(encoding="utf-8")
    svg = re.sub(r'(x="1088" y="86"[^>]*>)\d+\+?(</text>)', rf"\g<1>{solved}+\g<2>", svg)
    svg = re.sub(r"\d+\+? coding problems solved", f"{solved}+ coding problems solved", svg)
    IMPACT.write_text(svg, encoding="utf-8")


def main() -> None:
    cfg = json.loads(DATA.read_text(encoding="utf-8"))
    today = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d")
    days: set[dt.date] = set()
    live: list[str] = []

    for name, fetch in (("leetcode", leetcode), ("codeforces", codeforces), ("codechef", codechef)):
        platform = cfg[name]
        if not platform.get("handle"):
            print(f"{name}: no handle set, using saved numbers")
            continue
        try:
            result = fetch(platform["handle"])
        except Exception as err:  # noqa: BLE001 - any failure falls back to saved numbers
            print(f"{name}: live fetch failed ({err}), using saved numbers")
            continue
        for key in ("solved", "contests"):
            if result.get(key) is not None:
                platform[key] = result[key]
        days |= result["days"]
        live.append(name)
        print(f"{name}: live, {platform['solved']} solved, {platform['contests']} contests")

    # A streak never shrinks, so the saved record is kept unless the live days beat it.
    cfg["longest_streak"] = max(cfg["longest_streak"], longest_run(days))

    CARD.write_text(render(cfg, live, today), encoding="utf-8")
    patch_impact(sum(cfg[p]["solved"] for p in ("leetcode", "codechef", "codeforces")))
    DATA.write_text(json.dumps(cfg, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {CARD.name}")


if __name__ == "__main__":
    main()
