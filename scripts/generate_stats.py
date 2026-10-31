#!/usr/bin/env python3
"""Generate the live profile cards (stats, languages, contribution heatmap) as SVG.

Reads public data from the GitHub GraphQL API, so there is no third-party stats
service to rate-limit or go down. Standard library only.

Usage
    GH_LOGIN=your-username GH_TOKEN=ghp_xxx python scripts/generate_stats.py --out assets
    python scripts/generate_stats.py --sample --out assets     # offline preview with fake data

In GitHub Actions both variables are provided by the workflow.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import random
import sys
import urllib.request
from collections import defaultdict
from html import escape
from pathlib import Path

API = "https://api.github.com/graphql"

QUERY = """
query($login: String!) {
  user(login: $login) {
    followers { totalCount }
    pullRequests { totalCount }
    repositories(ownerAffiliations: OWNER, isFork: false, privacy: PUBLIC, first: 100) {
      totalCount
      nodes {
        stargazerCount
        languages(first: 10, orderBy: {field: SIZE, direction: DESC}) {
          edges { size node { name color } }
        }
      }
    }
    contributionsCollection {
      totalCommitContributions
      totalPullRequestContributions
      contributionCalendar {
        totalContributions
        weeks { contributionDays { contributionCount date } }
      }
    }
  }
}
"""

CSS = """
  :root {
    --card: #FFFFFF; --ink: #1F2937; --mute: #6B7280; --acc: #7C3AED; --line: #DDD6FE;
    --l0: #F1F5F9; --l1: #DDD6FE; --l2: #C4B5FD; --l3: #8B5CF6; --l4: #6D28D9;
  }
  @media (prefers-color-scheme: dark) {
    :root {
      --card: #0D1117; --ink: #F9FAFB; --mute: #9CA3AF; --acc: #A78BFA; --line: #30363D;
      --l0: #161B22; --l1: #3B2A7A; --l2: #5B3FD1; --l3: #8B5CF6; --l4: #C4B5FD;
    }
  }
  .sans { font-family: -apple-system, "Segoe UI", Helvetica, Arial, sans-serif; }
  .mono { font-family: "JetBrains Mono", "SFMono-Regular", Consolas, "Liberation Mono", monospace; }
  .in { animation: in .7s ease both; }
  @keyframes in { from { opacity: 0; transform: translateY(8px); } to { opacity: 1; transform: none; } }
  .cell { animation: pop .5s ease both; }
  @keyframes pop { from { opacity: 0; } to { opacity: 1; } }
  .l0 { fill: var(--l0); } .l1 { fill: var(--l1); } .l2 { fill: var(--l2); }
  .l3 { fill: var(--l3); } .l4 { fill: var(--l4); }
  @media (prefers-reduced-motion: reduce) { .in, .cell { animation: none; } }
"""


def fetch(login: str, token: str) -> dict:
    body = json.dumps({"query": QUERY, "variables": {"login": login}}).encode()
    req = urllib.request.Request(
        API,
        data=body,
        headers={"Authorization": f"bearer {token}", "Content-Type": "application/json", "User-Agent": "profile-cards"},
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        payload = json.load(resp)
    if payload.get("errors") or not payload.get("data", {}).get("user"):
        raise SystemExit(f"GitHub API error: {payload.get('errors') or 'user not found'}")
    return payload["data"]["user"]


def sample_user() -> dict:
    rng = random.Random(7)
    start = dt.date.today() - dt.timedelta(days=370)
    start -= dt.timedelta(days=(start.weekday() + 1) % 7)  # back to Sunday
    days = []
    d = start
    while d <= dt.date.today():
        n = rng.choice([0, 0, 0, 1, 2, 3, 5, 8]) if d.weekday() < 5 else rng.choice([0, 0, 0, 1, 2])
        days.append({"contributionCount": n, "date": d.isoformat()})
        d += dt.timedelta(days=1)
    weeks = [{"contributionDays": days[i : i + 7]} for i in range(0, len(days), 7)]
    langs = [("Python", "#3572A5", 520), ("C++", "#f34b7d", 310), ("JavaScript", "#f1e05a", 240),
             ("TypeScript", "#3178c6", 90), ("HTML", "#e34c26", 60), ("CSS", "#563d7c", 40)]
    node = {"stargazerCount": 12,
            "languages": {"edges": [{"size": s, "node": {"name": n, "color": c}} for n, c, s in langs]}}
    return {
        "followers": {"totalCount": 24},
        "pullRequests": {"totalCount": 9},
        "repositories": {"totalCount": 18, "nodes": [node]},
        "contributionsCollection": {
            "totalCommitContributions": 412,
            "totalPullRequestContributions": 9,
            "contributionCalendar": {
                "totalContributions": sum(x["contributionCount"] for x in days),
                "weeks": weeks,
            },
        },
    }


def flatten_days(user: dict) -> list[dict]:
    weeks = user["contributionsCollection"]["contributionCalendar"]["weeks"]
    return [d for w in weeks for d in w["contributionDays"]]


def streaks(days: list[dict]) -> tuple[int, int]:
    longest = run = 0
    for d in days:
        run = run + 1 if d["contributionCount"] > 0 else 0
        longest = max(longest, run)
    # current streak: walk back from the last day, forgiving a zero for today
    current = 0
    trail = list(days)
    if trail and trail[-1]["contributionCount"] == 0:
        trail.pop()
    for d in reversed(trail):
        if d["contributionCount"] > 0:
            current += 1
        else:
            break
    return current, longest


def wrap(width: int, height: int, title: str, inner: str) -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" role="img" aria-label="{escape(title)}">\n'
        f"  <title>{escape(title)}</title>\n  <style>{CSS}</style>\n"
        f'  <rect x="1" y="1" width="{width - 2}" height="{height - 2}" rx="16" fill="var(--card)" stroke="var(--line)" stroke-width="2" />\n'
        f"{inner}\n</svg>\n"
    )


def stats_svg(user: dict, today: str) -> str:
    cc = user["contributionsCollection"]
    days = flatten_days(user)
    current, longest = streaks(days)
    stars = sum(n["stargazerCount"] for n in user["repositories"]["nodes"])
    items = [
        (user["repositories"]["totalCount"], "public repos"),
        (stars, "stars earned"),
        (user["followers"]["totalCount"], "followers"),
        (cc["totalCommitContributions"], "commits, last year"),
        (cc["totalPullRequestContributions"], "pull requests, last year"),
        (f"{current} / {longest}", "streak: now / longest"),
    ]
    out = ['  <text x="32" y="46" class="sans" font-size="18" font-weight="700" fill="var(--ink)">GitHub, by the numbers</text>',
           '  <rect x="32" y="56" width="40" height="4" rx="2" fill="var(--acc)" />']
    for i, (value, label) in enumerate(items):
        col, row = i % 3, i // 3
        x = 32 + col * 184
        y = 108 + row * 66
        out.append(
            f'  <g class="in" style="animation-delay:{0.08 * i:.2f}s">'
            f'<text x="{x}" y="{y}" class="sans" font-size="30" font-weight="800" fill="var(--acc)">{escape(str(value))}</text>'
            f'<text x="{x}" y="{y + 22}" class="sans" font-size="12.5" fill="var(--mute)">{escape(label)}</text></g>'
        )
    out.append(f'  <text x="548" y="236" class="mono" font-size="10.5" fill="var(--mute)" text-anchor="end">updated {today} UTC</text>')
    return wrap(580, 250, "GitHub statistics", "\n".join(out))


def langs_svg(user: dict) -> str:
    totals: dict[str, int] = defaultdict(int)
    colors: dict[str, str] = {}
    for repo in user["repositories"]["nodes"]:
        for edge in repo["languages"]["edges"]:
            name = edge["node"]["name"]
            totals[name] += edge["size"]
            colors[name] = edge["node"]["color"] or "#7C3AED"
    ranked = sorted(totals.items(), key=lambda kv: kv[1], reverse=True)[:6]
    grand = sum(v for _, v in ranked) or 1
    out = ['  <text x="32" y="46" class="sans" font-size="18" font-weight="700" fill="var(--ink)">Top languages</text>',
           '  <rect x="32" y="56" width="40" height="4" rx="2" fill="var(--acc)" />',
           '  <defs><clipPath id="bar"><rect x="32" y="84" width="516" height="14" rx="7" /></clipPath></defs>',
           '  <g clip-path="url(#bar)">']
    x = 32.0
    for name, size in ranked:
        w = 516 * size / grand
        out.append(f'    <rect x="{x:.1f}" y="84" width="{w + 0.5:.1f}" height="14" fill="{escape(colors[name])}" />')
        x += w
    out.append("  </g>")
    for i, (name, size) in enumerate(ranked):
        col, row = i % 2, i // 2
        cx = 32 + col * 270
        cy = 136 + row * 32
        pct = 100 * size / grand
        out.append(
            f'  <g class="in" style="animation-delay:{0.08 * i:.2f}s">'
            f'<circle cx="{cx + 6}" cy="{cy - 4}" r="6" fill="{escape(colors[name])}" />'
            f'<text x="{cx + 20}" y="{cy}" class="sans" font-size="14" font-weight="600" fill="var(--ink)">{escape(name)}</text>'
            f'<text x="{cx + 240}" y="{cy}" class="mono" font-size="13" fill="var(--mute)" text-anchor="end">{pct:.1f}%</text></g>'
        )
    if not ranked:
        out.append('  <text x="32" y="140" class="sans" font-size="14" fill="var(--mute)">No public repositories with code yet.</text>')
    return wrap(580, 250, "Top languages by code size", "\n".join(out))


def heatmap_svg(user: dict) -> str:
    cal = user["contributionsCollection"]["contributionCalendar"]
    weeks = cal["weeks"]
    peak = max((d["contributionCount"] for w in weeks for d in w["contributionDays"]), default=0) or 1
    size, gap, x0, y0 = 17, 4, 70, 70
    out = [f'  <text x="32" y="40" class="sans" font-size="18" font-weight="700" fill="var(--ink)">'
           f'{cal["totalContributions"]} contributions in the last year</text>']
    for r, label in ((1, "Mon"), (3, "Wed"), (5, "Fri")):
        out.append(f'  <text x="32" y="{y0 + r * (size + gap) + 13}" class="mono" font-size="10.5" fill="var(--mute)">{label}</text>')
    last_month = None
    for wi, week in enumerate(weeks):
        x = x0 + wi * (size + gap)
        first = week["contributionDays"][0]["date"]
        month = dt.date.fromisoformat(first).strftime("%b")
        if month != last_month and wi < len(weeks) - 2:
            out.append(f'  <text x="{x}" y="{y0 - 10}" class="mono" font-size="10.5" fill="var(--mute)">{month}</text>')
            last_month = month
        for di, day in enumerate(week["contributionDays"]):
            n = day["contributionCount"]
            level = 0 if n == 0 else min(4, 1 + int(3 * n / peak))
            out.append(
                f'  <rect class="cell l{level}" x="{x}" y="{y0 + di * (size + gap)}" width="{size}" height="{size}" rx="4" '
                f'style="animation-delay:{wi * 14}ms"><title>{n} on {day["date"]}</title></rect>'
            )
    lx = 1200 - 32 - 5 * (size + gap) - 70
    out.append(f'  <text x="{lx}" y="230" class="mono" font-size="10.5" fill="var(--mute)" text-anchor="end">less</text>')
    for i in range(5):
        out.append(f'  <rect class="l{i}" x="{lx + 8 + i * (size + gap)}" y="217" width="{size}" height="{size}" rx="4" />')
    out.append(f'  <text x="{lx + 8 + 5 * (size + gap) + 4}" y="230" class="mono" font-size="10.5" fill="var(--mute)">more</text>')
    return wrap(1200, 250, "Contribution heatmap for the last year", "\n".join(out))


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", default="assets", help="output folder (default: assets)")
    ap.add_argument("--sample", action="store_true", help="use fake data, no network or token needed")
    args = ap.parse_args()

    if args.sample:
        user = sample_user()
    else:
        login, token = os.environ.get("GH_LOGIN"), os.environ.get("GH_TOKEN")
        if not login or not token:
            sys.exit("Set GH_LOGIN and GH_TOKEN, or run with --sample.")
        user = fetch(login, token)

    today = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d")
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    (out / "stats.svg").write_text(stats_svg(user, today), encoding="utf-8")
    (out / "langs.svg").write_text(langs_svg(user), encoding="utf-8")
    (out / "heatmap.svg").write_text(heatmap_svg(user), encoding="utf-8")
    print(f"wrote stats.svg, langs.svg, heatmap.svg to {out}/")


if __name__ == "__main__":
    main()
