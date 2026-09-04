import json
import os
import urllib.request
import datetime as dt
from collections import Counter, defaultdict

OWNER = os.environ.get("GITHUB_REPOSITORY", "assishmoncs/assishmoncs").split("/")[0]
TOKEN = os.environ["GITHUB_TOKEN"]
HEADERS = {"Authorization": f"Bearer {TOKEN}", "Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28"}


def api(path):
    req = urllib.request.Request("https://api.github.com" + path, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def gql(query, variables):
    body = json.dumps({"query": query, "variables": variables}).encode()
    req = urllib.request.Request("https://api.github.com/graphql", data=body, headers={**HEADERS, "Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(req, timeout=30) as r:
        result = json.load(r)
    if result.get("errors"):
        raise RuntimeError(result["errors"])
    return result["data"]


def esc(value):
    return (str(value).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;"))


def card(title, value, subtitle, width=490, height=170):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
<rect width="100%" height="100%" rx="16" fill="#0d1117" stroke="#30363d"/>
<text x="28" y="38" fill="#58a6ff" font-family="Arial,Helvetica,sans-serif" font-size="15" font-weight="700">{esc(title)}</text>
<text x="28" y="92" fill="#f0f6fc" font-family="Arial,Helvetica,sans-serif" font-size="40" font-weight="700">{esc(value)}</text>
<text x="28" y="132" fill="#8b949e" font-family="Arial,Helvetica,sans-serif" font-size="14">{esc(subtitle)}</text>
</svg>'''

query = '''query($login:String!) {
  user(login:$login) {
    followers { totalCount }
    repositories(first:100, ownerAffiliations:OWNER, privacy:PUBLIC, isFork:false) {
      totalCount
      nodes {
        name
        stargazerCount
        languages(first:10, orderBy:{field:SIZE, direction:DESC}) {
          edges { size node { name } }
        }
      }
    }
    contributionsCollection {
      totalCommitContributions
      contributionCalendar {
        totalContributions
        weeks { contributionDays { date contributionCount } }
      }
    }
  }
}'''

data = gql(query, {"login": OWNER})["user"]
repos = data["repositories"]["nodes"]
calendar = [d for w in data["contributionsCollection"]["contributionCalendar"]["weeks"] for d in w["contributionDays"]]

stars = sum(r["stargazerCount"] for r in repos)
langs = Counter()
for repo in repos:
    for edge in repo["languages"]["edges"]:
        langs[edge["node"]["name"]] += edge["size"]
total_bytes = sum(langs.values()) or 1
top_langs = langs.most_common(6)
commits = data["contributionsCollection"]["totalCommitContributions"]
total_contrib = data["contributionsCollection"]["contributionCalendar"]["totalContributions"]
followers = data["followers"]["totalCount"]

os.makedirs("assets", exist_ok=True)
open("assets/github-stats.svg", "w", encoding="utf-8").write(card("GITHUB ACTIVITY", f"{total_contrib}", f"contributions in the last year  •  {repos and len(repos) or 0} public repositories"))

# Top languages card
W, H = 490, 170
svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
       '<rect width="100%" height="100%" rx="16" fill="#0d1117" stroke="#30363d"/>',
       '<text x="28" y="38" fill="#58a6ff" font-family="Arial,Helvetica,sans-serif" font-size="15" font-weight="700">TOP LANGUAGES</text>']
y = 62
for name, amount in top_langs:
    pct = amount / total_bytes * 100
    svg.append(f'<text x="28" y="{y}" fill="#f0f6fc" font-family="Arial,Helvetica,sans-serif" font-size="13">{esc(name)}</text>')
    svg.append(f'<text x="448" y="{y}" text-anchor="end" fill="#8b949e" font-family="Arial,Helvetica,sans-serif" font-size="12">{pct:.1f}%</text>')
    svg.append(f'<rect x="108" y="{y-10}" width="310" height="8" rx="4" fill="#21262d"/>')
    svg.append(f'<rect x="108" y="{y-10}" width="{max(4, 310*pct/100):.1f}" height="8" rx="4" fill="#58a6ff"/>')
    y += 19
svg.append('</svg>')
open("assets/top-langs.svg", "w", encoding="utf-8").write("\n".join(svg))

# Weekly contribution activity chart.
last_year = sorted(calendar, key=lambda x: x["date"])[-365:]
weeks = defaultdict(int)
for day in last_year:
    d = dt.date.fromisoformat(day["date"])
    monday = d - dt.timedelta(days=d.weekday())
    weeks[monday.isoformat()] += day["contributionCount"]
weekly = sorted(weeks.items())[-52:]
max_week = max([v for _, v in weekly] or [1])
W, H = 960, 230
svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
       '<rect width="100%" height="100%" rx="16" fill="#0d1117" stroke="#30363d"/>',
       '<text x="28" y="34" fill="#f0f6fc" font-family="Arial,Helvetica,sans-serif" font-size="15" font-weight="700">CONTRIBUTION ACTIVITY</text>',
       '<text x="28" y="56" fill="#8b949e" font-family="Arial,Helvetica,sans-serif" font-size="12">weekly contribution volume • last 52 weeks</text>']
chart_x, chart_y, bar_w, gap, chart_h = 28, 82, 14, 4, 100
for i, (week, count) in enumerate(weekly):
    h = 4 if count == 0 else 8 + (count / max_week) * (chart_h - 8)
    x = chart_x + i * (bar_w + gap)
    y = chart_y + chart_h - h
    svg.append(f'<rect x="{x}" y="{y:.1f}" width="{bar_w}" height="{h:.1f}" rx="4" fill="#58a6ff" opacity="{0.25 + 0.75*(count/max_week if max_week else 0):.2f}"/>')
    if i % 8 == 0:
        svg.append(f'<text x="{x}" y="210" fill="#8b949e" font-family="Arial,Helvetica,sans-serif" font-size="10">{esc(week[5:7])}/{esc(week[8:])}</text>')
svg.append(f'<text x="{W-28}" y="34" text-anchor="end" fill="#8b949e" font-family="Arial,Helvetica,sans-serif" font-size="12">{total_contrib} total • {commits} commits • {stars} stars • {followers} followers</text>')
svg.append('</svg>')
open("assets/activity.svg", "w", encoding="utf-8").write("\n".join(svg))

# Simple contribution streak calculation.
counts = {d["date"]: d["contributionCount"] for d in calendar}
today = dt.date.today()
cur = 0
cursor = today
while counts.get(cursor.isoformat(), 0) > 0:
    cur += 1
    cursor -= dt.timedelta(days=1)
if cur == 0:
    cursor = today - dt.timedelta(days=1)
while counts.get(cursor.isoformat(), 0) > 0:
    cur += 1
    cursor -= dt.timedelta(days=1)
longest = 0
run = 0
for d in sorted(counts):
    if counts[d] > 0:
        run += 1
        longest = max(longest, run)
    else:
        run = 0
open("assets/streak.svg", "w", encoding="utf-8").write(card("CONTRIBUTION STREAK", f"{cur} days", f"current streak  •  longest: {longest} days"))

print(f"Generated assets: contributions={total_contrib}, commits={commits}, repos={len(repos)}, stars={stars}, followers={followers}")
