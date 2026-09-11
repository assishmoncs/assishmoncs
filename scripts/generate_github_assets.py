import json
import os
import urllib.request
import datetime as dt
from collections import Counter, defaultdict

OWNER = os.environ.get("GITHUB_REPOSITORY", "assishmoncs/assishmoncs").split("/")[0]
TOKEN = os.environ.get("GITHUB_TOKEN", "")
HEADERS = {"Authorization": f"Bearer {TOKEN}", "Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28"}

LANG_COLORS = {
    "JavaScript": "#f1e05a",
    "Python": "#3572A5",
    "CSS": "#563d7c",
    "TypeScript": "#3178c6",
    "Kotlin": "#A97BFF",
    "HTML": "#e34c26",
    "C": "#555555",
    "C++": "#f34b7d",
    "Go": "#00ADD8",
    "Java": "#b07219",
    "Shell": "#89e051",
    "Rust": "#dea584",
    "Swift": "#F05138",
    "PHP": "#4F5D95",
}

def esc(value):
    return (str(value).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;"))

def gql(query, variables):
    body = json.dumps({"query": query, "variables": variables}).encode()
    req = urllib.request.Request("https://api.github.com/graphql", data=body, headers={**HEADERS, "Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(req, timeout=30) as r:
        result = json.load(r)
    if result.get("errors"):
        raise RuntimeError(result["errors"])
    return result["data"]

def generate_github_stats_card(total_contrib, commits, repos_count, stars, followers, width=490, height=185):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="GitHub Overview Metrics">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#0d1117"/>
      <stop offset="100%" stop-color="#161b22"/>
    </linearGradient>
  </defs>
  <rect width="100%" height="100%" rx="16" fill="url(#bgGrad)" stroke="#30363d" stroke-width="1.2"/>
  
  <!-- Header -->
  <g transform="translate(24, 28)">
    <circle cx="6" cy="6" r="6" fill="#58a6ff" opacity="0.9"/>
    <text x="20" y="10" fill="#58a6ff" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif" font-size="13" font-weight="700" letter-spacing="1">GITHUB METRICS</text>
  </g>
  
  <g transform="translate(376, 18)">
    <rect width="90" height="22" rx="11" fill="#1f6feb" fill-opacity="0.15" stroke="#388bfd" stroke-opacity="0.35" stroke-width="1"/>
    <text x="45" y="15" text-anchor="middle" fill="#58a6ff" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif" font-size="11" font-weight="600">OVERVIEW</text>
  </g>

  <!-- Metric 1: Total Contributions -->
  <g transform="translate(24, 52)">
    <rect width="214" height="54" rx="10" fill="#0d1117" stroke="#21262d" stroke-width="1"/>
    <rect x="0" y="0" width="4" height="54" rx="2" fill="#58a6ff"/>
    <text x="16" y="22" fill="#8b949e" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif" font-size="11" font-weight="500">Total Contributions</text>
    <text x="16" y="44" fill="#f0f6fc" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif" font-size="20" font-weight="700">{total_contrib:,}</text>
    <text x="198" y="38" text-anchor="end" fill="#58a6ff" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif" font-size="16">📊</text>
  </g>

  <!-- Metric 2: Total Commits -->
  <g transform="translate(252, 52)">
    <rect width="214" height="54" rx="10" fill="#0d1117" stroke="#21262d" stroke-width="1"/>
    <rect x="0" y="0" width="4" height="54" rx="2" fill="#3fb950"/>
    <text x="16" y="22" fill="#8b949e" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif" font-size="11" font-weight="500">Total Commits</text>
    <text x="16" y="44" fill="#f0f6fc" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif" font-size="20" font-weight="700">{commits:,}</text>
    <text x="198" y="38" text-anchor="end" fill="#3fb950" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif" font-size="16">🔨</text>
  </g>

  <!-- Metric 3: Public Repositories -->
  <g transform="translate(24, 114)">
    <rect width="214" height="54" rx="10" fill="#0d1117" stroke="#21262d" stroke-width="1"/>
    <rect x="0" y="0" width="4" height="54" rx="2" fill="#bc8cff"/>
    <text x="16" y="22" fill="#8b949e" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif" font-size="11" font-weight="500">Public Repositories</text>
    <text x="16" y="44" fill="#f0f6fc" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif" font-size="20" font-weight="700">{repos_count}</text>
    <text x="198" y="38" text-anchor="end" fill="#bc8cff" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif" font-size="16">📦</text>
  </g>

  <!-- Metric 4: Stars & Followers -->
  <g transform="translate(252, 114)">
    <rect width="214" height="54" rx="10" fill="#0d1117" stroke="#21262d" stroke-width="1"/>
    <rect x="0" y="0" width="4" height="54" rx="2" fill="#d29922"/>
    <text x="16" y="22" fill="#8b949e" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif" font-size="11" font-weight="500">Stars &amp; Community</text>
    <text x="16" y="44" fill="#f0f6fc" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif" font-size="18" font-weight="700">{stars} ★  •  {followers} 👥</text>
    <text x="198" y="38" text-anchor="end" fill="#d29922" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif" font-size="16">✨</text>
  </g>
</svg>'''

def generate_streak_card(current_streak, longest_streak, total_contrib, width=490, height=185):
    day_str = "Day" if current_streak == 1 else "Days"
    longest_day_str = "Day" if longest_streak == 1 else "Days"
    bar_fill = min(178, max(24, int(178 * current_streak / max(1, longest_streak))))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="Contribution Streak">
  <defs>
    <linearGradient id="streakBgGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#0d1117"/>
      <stop offset="100%" stop-color="#161b22"/>
    </linearGradient>
    <linearGradient id="fireGrad" x1="0" y1="1" x2="0" y2="0">
      <stop offset="0%" stop-color="#f85149"/>
      <stop offset="100%" stop-color="#ff7b72"/>
    </linearGradient>
  </defs>
  <rect width="100%" height="100%" rx="16" fill="url(#streakBgGrad)" stroke="#30363d" stroke-width="1.2"/>
  
  <!-- Header -->
  <g transform="translate(24, 28)">
    <circle cx="6" cy="6" r="6" fill="#ff7b72" opacity="0.9"/>
    <text x="20" y="10" fill="#ff7b72" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif" font-size="13" font-weight="700" letter-spacing="1">CONTRIBUTION STREAK</text>
  </g>
  
  <g transform="translate(366, 18)">
    <rect width="100" height="22" rx="11" fill="#f85149" fill-opacity="0.15" stroke="#f85149" stroke-opacity="0.35" stroke-width="1"/>
    <text x="50" y="15" text-anchor="middle" fill="#ff7b72" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif" font-size="11" font-weight="600">🔥 ACTIVE</text>
  </g>

  <!-- Left Main Card: Current Streak -->
  <g transform="translate(24, 52)">
    <rect width="214" height="116" rx="12" fill="#0d1117" stroke="#21262d" stroke-width="1"/>
    <rect x="0" y="0" width="4" height="116" rx="2" fill="url(#fireGrad)"/>
    <text x="18" y="28" fill="#8b949e" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif" font-size="11" font-weight="600" letter-spacing="0.5">CURRENT STREAK</text>
    <text x="18" y="68" fill="#f0f6fc" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif" font-size="34" font-weight="800">{current_streak} <tspan font-size="20" font-weight="600" fill="#8b949e">{day_str}</tspan></text>
    <rect x="18" y="86" width="178" height="6" rx="3" fill="#21262d"/>
    <rect x="18" y="86" width="{bar_fill}" height="6" rx="3" fill="#f85149"/>
    <text x="18" y="106" fill="#3fb950" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif" font-size="11" font-weight="500">● Consistent Contributions</text>
  </g>

  <!-- Right Top Card: Longest Streak -->
  <g transform="translate(252, 52)">
    <rect width="214" height="54" rx="10" fill="#0d1117" stroke="#21262d" stroke-width="1"/>
    <rect x="0" y="0" width="4" height="54" rx="2" fill="#d29922"/>
    <text x="16" y="22" fill="#8b949e" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif" font-size="11" font-weight="500">Longest Streak</text>
    <text x="16" y="44" fill="#f0f6fc" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif" font-size="19" font-weight="700">{longest_streak} {longest_day_str}</text>
    <text x="198" y="38" text-anchor="end" fill="#d29922" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif" font-size="16">🏆</text>
  </g>

  <!-- Right Bottom Card: Total Contributions in Year -->
  <g transform="translate(252, 114)">
    <rect width="214" height="54" rx="10" fill="#0d1117" stroke="#21262d" stroke-width="1"/>
    <rect x="0" y="0" width="4" height="54" rx="2" fill="#3fb950"/>
    <text x="16" y="22" fill="#8b949e" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif" font-size="11" font-weight="500">Past 365 Days Volume</text>
    <text x="16" y="44" fill="#f0f6fc" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif" font-size="19" font-weight="700">{total_contrib} Contribs</text>
    <text x="198" y="38" text-anchor="end" fill="#3fb950" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif" font-size="16">⚡</text>
  </g>
</svg>'''

def generate_top_langs_card(top_langs, width=490, height=185):
    bar_width = 442
    bar_x = 24
    bar_y = 50
    bar_h = 8
    
    segments_svg = []
    current_x = bar_x
    for i, (name, pct) in enumerate(top_langs):
        color = LANG_COLORS.get(name, "#58a6ff")
        seg_w = (pct / 100.0) * bar_width
        rx = 4 if i == 0 or i == len(top_langs) - 1 else 0
        segments_svg.append(f'<rect x="{current_x:.1f}" y="{bar_y}" width="{seg_w:.1f}" height="{bar_h}" fill="{color}" rx="{rx}"/>')
        current_x += seg_w
    
    items_svg = []
    col1 = [top_langs[i] for i in range(len(top_langs)) if i % 2 == 0]
    col2 = [top_langs[i] for i in range(len(top_langs)) if i % 2 == 1]
    
    for col, start_x in [(col1, 24), (col2, 252)]:
        y_pos = 78
        for name, pct in col:
            color = LANG_COLORS.get(name, "#58a6ff")
            items_svg.append(f'''
    <g transform="translate({start_x}, {y_pos})">
      <circle cx="6" cy="6" r="5" fill="{color}"/>
      <text x="18" y="10" fill="#f0f6fc" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif" font-size="12" font-weight="600">{esc(name)}</text>
      <rect x="110" y="3" width="60" height="6" rx="3" fill="#21262d"/>
      <rect x="110" y="3" width="{max(4, int(60 * pct / 50.0))}" height="6" rx="3" fill="{color}"/>
      <text x="214" y="10" text-anchor="end" fill="#8b949e" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif" font-size="11" font-weight="500">{pct:.1f}%</text>
    </g>''')
            y_pos += 34

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="Top Languages Breakdown">
  <defs>
    <linearGradient id="langsBgGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#0d1117"/>
      <stop offset="100%" stop-color="#161b22"/>
    </linearGradient>
  </defs>
  <rect width="100%" height="100%" rx="16" fill="url(#langsBgGrad)" stroke="#30363d" stroke-width="1.2"/>
  
  <!-- Header -->
  <g transform="translate(24, 28)">
    <circle cx="6" cy="6" r="6" fill="#58a6ff" opacity="0.9"/>
    <text x="20" y="10" fill="#58a6ff" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif" font-size="13" font-weight="700" letter-spacing="1">TOP LANGUAGES</text>
  </g>
  
  <text x="466" y="32" text-anchor="end" fill="#8b949e" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif" font-size="11" font-weight="500">BY REPOSITORY SIZE</text>

  <!-- Segmented Language Bar -->
  <g>
    <rect x="{bar_x}" y="{bar_y}" width="{bar_width}" height="{bar_h}" rx="4" fill="#21262d"/>
    {''.join(segments_svg)}
  </g>

  <!-- Language Grid -->
  {''.join(items_svg)}
</svg>'''

def main():
    if not TOKEN:
        print("No GITHUB_TOKEN provided, skipping live API fetch.")
        return

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
    top_langs_raw = langs.most_common(6)
    top_langs = [(name, amount / total_bytes * 100) for name, amount in top_langs_raw]

    commits = data["contributionsCollection"]["totalCommitContributions"]
    total_contrib = data["contributionsCollection"]["contributionCalendar"]["totalContributions"]
    followers = data["followers"]["totalCount"]
    repos_count = len(repos)

    # Streak calculation
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

    os.makedirs("assets", exist_ok=True)
    with open("assets/github-stats.svg", "w", encoding="utf-8") as f:
        f.write(generate_github_stats_card(total_contrib, commits, repos_count, stars, followers))

    with open("assets/streak.svg", "w", encoding="utf-8") as f:
        f.write(generate_streak_card(cur, longest, total_contrib))

    with open("assets/top-langs.svg", "w", encoding="utf-8") as f:
        f.write(generate_top_langs_card(top_langs))

    # Weekly contribution activity chart
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
    with open("assets/activity.svg", "w", encoding="utf-8") as f:
        f.write("\n".join(svg))

    print(f"Generated assets: contributions={total_contrib}, commits={commits}, repos={repos_count}, stars={stars}, followers={followers}")

if __name__ == "__main__":
    main()
